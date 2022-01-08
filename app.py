from flask import Flask, Blueprint, redirect, url_for, render_template, request, redirect, session,flash

from key import create_key
create_key()

from Trent import *
from save_import_key import *
from exchange import Key_Exchange_Protocol,Attack_Key_Exchange_Protocol
import random

app = Flask(__name__)
app.secret_key = "Access Control"
# Login Page
@app.route("/", methods = ['GET','POST'])
def home():
    log = []
    sender = None
    receiver = None
    if request.method == 'POST':
        if "form1" in request.form:
            if request.form.get('sender') != request.form.get('receiver'):
                log, N_A, N_B = Key_Exchange_Protocol(str(request.form.get('sender')),str(request.form.get('receiver')),log)
                flash("Exchange Completed")
            else:
                log.append("ERROR")
                flash("Can not exchange between same user!!!")
        
        
    return render_template("index.html",sender=sender,receiver=receiver,log=log)

@app.route("/attack",methods=["GET", "POST"])
def attack():
    log1 = []
    log2 = []
    log3 = []
    log4 = []
    sender = None
    receiver = None
    if request.method == 'POST':
        if "form2" in request.form:
            if request.form.get('sender') != request.form.get('receiver') != request.form.get('attacker'):
                sender_name = request.form.get('sender')
                receiver_name = request.form.get('receiver')
                attacker_name = request.form.get('attacker')
                # Create two exchange protocol
                Exchange_Protocol1 = Attack_Key_Exchange_Protocol(sender_name,attacker_name)
                Exchange_Protocol2 = Attack_Key_Exchange_Protocol(attacker_name,receiver_name,True)

                # Sender request to Trent
                log1 = Exchange_Protocol1.sender_request_to_Trent(log1)
                log2 = Exchange_Protocol2.sender_request_to_Trent(log2)
                
                # Sender request to Receiver
                N_A = random.randint(100,10000)
                log1, Sender_encrypted_message_Receiver = Exchange_Protocol1.sender_request_to_receiver(N_A,log1)

                # Receiver request to Trent

                log1, Trent_encrypted_message = Exchange_Protocol2.receiver_request_to_Trent(log1,Sender_encrypted_message_Receiver,True)
                log2 = Exchange_Protocol2.receiver_request_to_Trent(log2,Trent_encrypted_message)

                # Receiver request to Sender
                N_B = random.randint(100,10000)
                # log1,Receiver_encrypted_message_Sender1 = Exchange_Protocol1.receiver_request_to_sender(N_B,log1)
                log1.append("\n\----------------------------------Step 6 Completed---------------------------------/\n")
                log2,Receiver_encrypted_message_Sender2 = Exchange_Protocol2.receiver_request_to_sender(N_B, log2)

                # Sender response to Receiver
                log3,Sender_response_message = Exchange_Protocol1.sender_response_to_receiver(log3,Receiver_encrypted_message_Sender2)
                log3 = Exchange_Protocol1.receiver_response_to_sender(log3, Sender_response_message)
                log1.extend(log3)
                
                log4, Trent_encrypted_response = Exchange_Protocol2.receiver_response_to_sender(log4, Sender_response_message, True)
                log2.extend(log4)
                log2 = Exchange_Protocol2.receiver_response_to_sender(log2,Trent_encrypted_response,False)

                flash("Exchange Completed")
                flash("Exchange Completed")
            else:
                log1.append("ERROR")
                log2.append("ERROR")
                flash("Can not exchange between same user!!!")
    return render_template("attack.html",sender=sender,receiver=receiver,log1=log1,log2=log2)

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True, port=1522)