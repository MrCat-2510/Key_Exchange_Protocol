from Trent import *
from save_import_key import *
import random

def Key_Exchange_Protocol(sender_name, receiver_name, log):
    Trent = check_user('Trent')
    sender = check_user(sender_name)
    receiver = check_user(receiver_name)
    # Step 1
    log.append("\n/--------------------------------------Step 1--------------------------------------\ \n")
    message = str(sender['name']) + "," + str(receiver['name'])
    encrypted_message = encrypt_message(message,Trent['public_key'])
    log.append("{} sends to Trent:\n{}".format(sender['name'],encrypted_message))
    log.append("\n\----------------------------------Step 1 Completed---------------------------------/\n")

    # Step 2
    log.append("\n/--------------------------------------Step 2--------------------------------------\ \n")
    message_response, response = request_public_key(encrypted_message)
    log.append(message_response)
    log.append("Trent sends to {}: \n{}".format(sender['name'],response))
    log.append("\n\----------------------------------Step 2 Completed---------------------------------/\n")

    #Step 3
    log.append("\n/--------------------------------------Step 3--------------------------------------\ \n")
    decrypt_response = decrypt_message(response[1],sender['private_key'])
    log.append("{} decrypted response from Trent:\n1. Public Key of {}:\n{}\n2.{}".format(sender['name'],decrypt_response,response[0],decrypt_response))
    if decrypt_response == receiver['name']:
        log.append("{} verify {} complete".format(sender['name'],receiver['name']))
    ## Sender create nonce and message
    N_A = random.randint(100,10000)
    log.append("{} create nonce: {}".format(sender['name'],N_A))
    Sender_message_Receiver = str(N_A) + "," + sender['name']
    Sender_encrypted_message_Receiver = encrypt_message(Sender_message_Receiver, response[0])
    log.append("{} sends to {}:\n{}".format(sender['name'],receiver['name'],Sender_encrypted_message_Receiver))
    log.append("\n\----------------------------------Step 3 Completed---------------------------------/\n")

    #Step 4
    log.append("\n/--------------------------------------Step 4--------------------------------------\ \n")
    Receiver_decrypted_message = decrypt_message(Sender_encrypted_message_Receiver, receiver['private_key']).split(',')
    log.append("{} decrypted from {}:\n{}".format(receiver['name'],sender['name'],Receiver_decrypted_message))
    if sender['name'] == Receiver_decrypted_message[1]:
        log.append("{} verify {} complete".format(receiver['name'],Receiver_decrypted_message[1]))

    ## Receiver request to Trent
    Receiver_message = str(receiver['name']) + "," + str(sender['name'])
    Receiver_encrypted_message = encrypt_message(Receiver_message,Trent['public_key'])
    log.append("{} send to Trent:\n{}".format(receiver['name'],Receiver_encrypted_message))
    log.append("\n\----------------------------------Step 4 Completed---------------------------------/\n")

    #Step 5
    log.append("\n/--------------------------------------Step 5--------------------------------------\ \n")
    receiver_message_response, receiver_response = request_public_key(Receiver_encrypted_message)
    log.append(receiver_message_response)
    log.append("Trent sends to {}: \n{}".format(receiver['name'],receiver_response))
    log.append("\n\----------------------------------Step 5 Completed---------------------------------/\n")

    #Step 6
    log.append("\n/--------------------------------------Step 6--------------------------------------\ \n")
    Receiver_decrypt_response = decrypt_message(receiver_response[1],receiver['private_key'])
    log.append("{} decrypted response from Trent:\nPublic Key of {}:\n{}\n{}".format(receiver['name'],Receiver_decrypt_response,receiver_response[0],Receiver_decrypt_response))
    if Receiver_decrypt_response == sender['name']:
        log.append("{} verify {} complete".format(receiver['name'],sender['name']))
    ## Receiver create nonce and message
    N_B = random.randint(100,10000)
    log.append("{} create nonce: {}".format(receiver['name'],N_B))
    Receiver_message_Sender = Receiver_decrypted_message[0] + ","+ str(N_B)
    Receiver_encrypted_message_Sender = encrypt_message(Receiver_message_Sender, receiver_response[0])
    log.append("{} sends to {}:\n{}".format(receiver['name'],sender['name'],Receiver_encrypted_message_Sender))
    log.append("\n\----------------------------------Step 6 Completed---------------------------------/\n")

    #Step 7
    log.append("\n/--------------------------------------Step 7--------------------------------------\ \n")
    Sender_decrypted_message = decrypt_message(Receiver_encrypted_message_Sender, sender['private_key']).split(",")
    log.append("{} decrypt message from {}:\n{}".format(sender['name'],receiver['name'],Sender_decrypted_message))
    if int(Sender_decrypted_message[0]) == N_A:
        log.append("{} verify {}'s nonce complete".format(sender['name'],sender['name']))

    Alice_response_message = encrypt_message(Sender_decrypted_message[1],response[0])
    log.append("{} response {}:\n{}".format(sender['name'],receiver['name'],Alice_response_message))
    log.append("\n\----------------------------------Step 7 Completed---------------------------------/\n")

    #Step 8
    log.append("\n/--------------------------------------Step 8--------------------------------------\ \n")
    Receiver_decrypted_response = decrypt_message(Alice_response_message, receiver['private_key'])
    if int(Receiver_decrypted_response) == N_B:
        log.append("{} verify {}'s nonce complete".format(receiver['name'],receiver['name']))
    log.append("\n\----------------------------------Step 8 Completed---------------------------------/\n")

    log.append("Now {} and {} share their private nonces: [{},{}]".format(sender['name'], receiver['name'],N_A,N_B))

    return log, N_A, N_B

class Attack_Key_Exchange_Protocol():
    def __init__(self, sender_name, receiver_name,attack = False):
        self.Trent = check_user('Trent')
        self.sender = check_user(sender_name)
        self.receiver = check_user(receiver_name)
        self.attack = attack
    
    def sender(self):
        return self.sender
    def receiver(self):
        return self.receiver
    def is_attack(self):
        return self.attack
    def sender_request_to_Trent(self, log):
            # Step 1
        log.append("\n/--------------------------------------Step 1--------------------------------------\ \n")
        message = str(self.sender['name']) + "," + str(self.receiver['name'])
        encrypted_message = encrypt_message(message,Trent['public_key'])
        log.append("{} sends to Trent:\n{}".format(self.sender['name'],encrypted_message))
        log.append("\n\----------------------------------Step 1 Completed---------------------------------/\n")

        # Step 2
        log.append("\n/--------------------------------------Step 2--------------------------------------\ \n")
        log.append("Trent receiver message from {}: {}".format(self.sender['name'],encrypted_message))
        message_response, response = request_public_key(encrypted_message)
        log.append(message_response)
        log.append("Trent sends to {}: \n{}".format(self.sender['name'],response))
        log.append("\n\----------------------------------Step 2 Completed---------------------------------/\n")
        #Step 3
        log.append("\n/--------------------------------------Step 3--------------------------------------\ \n")
        log.append("{} receive response from Trent: {}".format(self.sender['name'],response))
        self.decrypt_response = decrypt_message(response[1],self.sender['private_key'])
        log.append("{} decrypted response from Trent:\n1. Public Key of {}:\n=>{}\n2. {}".format(self.sender['name'],self.decrypt_response,response[0],self.decrypt_response))
        if self.decrypt_response == self.receiver['name']:
            log.append("{} verify {} complete".format(self.sender['name'],self.receiver['name']))

        self.response = response

        return log
    
    def sender_request_to_receiver(self,N_A, log):
        #  N_A = random.randint(100,10000)
        log.append("{} create nonce: {}".format(self.sender['name'],N_A))
        Sender_message_Receiver = str(N_A) + "," + self.sender['name']
        log.append("{} create message: {}".format(self.sender['name'],Sender_message_Receiver))
        Sender_encrypted_message_Receiver = encrypt_message(Sender_message_Receiver, self.response[0])
        log.append("{} encrypted message by {} public_key".format(self.sender['name'],self.decrypt_response))
        log.append("{} sends to {}:\n{}".format(self.sender['name'],self.receiver['name'],Sender_encrypted_message_Receiver))
        log.append("\n\----------------------------------Step 3 Completed---------------------------------/\n")
        self.N_A = N_A
        return log,Sender_encrypted_message_Receiver
    
    def receiver_request_to_Trent(self,log,Sender_encrypted_message_Receiver,attack=False):
        if attack ==True:
            log.append("\n/-------------------------------------Step 4 5-------------------------------------\ \n")
            log.append("{} receiver Alice message: {}".format(self.sender['name'],Sender_encrypted_message_Receiver))
            Trent_decrypted_message = decrypt_message(Sender_encrypted_message_Receiver, self.sender['private_key'])
            log.append("{} decrypted message: {}".format(self.sender['name'], Trent_decrypted_message))

            Trent_encrypted_message = encrypt_message(Trent_decrypted_message, self.response[0])

            log.append("{} encrypted message by {} public key {}".format(self.sender['name'], self.decrypt_response,self.response[0]))
            log.append("Alice ({}) send to {}: {}".format(self.sender['name'],self.decrypt_response, Trent_encrypted_message))
            self.sender = check_user("Alice(Malice)")
            log.append("\n\---------------------------------Step 4 5 Completed--------------------------------/\n")
            return log, Trent_encrypted_message
        else:
            #Step 4
            log.append("\n/--------------------------------------Step 4--------------------------------------\ \n")
            log.append("{} receive message from {}:\n{}".format(self.receiver['name'],self.sender['name'],Sender_encrypted_message_Receiver))
            self.Receiver_decrypted_message = decrypt_message(Sender_encrypted_message_Receiver, self.receiver['private_key']).split(',')
            log.append("{} decrypted from {}: {}".format(self.receiver['name'],self.sender['name'],self.Receiver_decrypted_message))
            if self.sender['name'] == self.Receiver_decrypted_message[1] or self.sender['name']=="Alice(Malice)":
                log.append("{} verify {} complete".format(self.receiver['name'],self.Receiver_decrypted_message[1]))

            ## Receiver request to Trent
            # Receiver_message = str(self.receiver['name']) + "," + str(self.sender['name'])
            self.N_A = self.Receiver_decrypted_message[0]
            Receiver_message = str(self.receiver['name']) + "," + str(self.Receiver_decrypted_message[1])
            log.append("{} create message: {}".format(self.receiver['name'], Receiver_message))
            Receiver_encrypted_message = encrypt_message(Receiver_message,Trent['public_key'])
            log.append("{} send to Trent:\n{}".format(self.receiver['name'],Receiver_encrypted_message))
            log.append("\n\----------------------------------Step 4 Completed---------------------------------/\n")

            #Step 5
            log.append("\n/--------------------------------------Step 5--------------------------------------\ \n")
            receiver_message_response, self.receiver_response = request_public_key(Receiver_encrypted_message)
            log.append(receiver_message_response)
            log.append("Trent sends to {}: \n{}".format(self.receiver['name'],self.receiver_response))
            log.append("\n\----------------------------------Step 5 Completed---------------------------------/\n")

            #Step 6
            log.append("\n/--------------------------------------Step 6--------------------------------------\ \n")
            self.Receiver_decrypt_response = decrypt_message(self.receiver_response[1],self.receiver['private_key'])
            log.append("{} decrypted response from Trent:\n1.Public Key of {}:\n =>{}\n2. {}".format(self.receiver['name'],self.Receiver_decrypt_response,self.receiver_response[0],self.Receiver_decrypt_response))
            if self.Receiver_decrypt_response == self.sender['name']:
                log.append("{} verify {} complete".format(self.receiver['name'],self.sender['name']))

            return log
    
    def receiver_request_to_sender(self, N_B, log):
        ## Receiver create nonce and message
        # N_B = random.randint(100,10000)
        log.append("{} create nonce: {}".format(self.receiver['name'],N_B))
        Receiver_message_Sender = self.Receiver_decrypted_message[0] + ","+ str(N_B)
        log.append("{} encrypted message by {} public_key".format(self.receiver['name'],self.Receiver_decrypt_response))
        Receiver_encrypted_message_Sender = encrypt_message(Receiver_message_Sender, self.receiver_response[0])
        log.append("{} sends to {}:\n{}".format(self.receiver['name'],self.sender['name'],Receiver_encrypted_message_Sender))
        log.append("\n\----------------------------------Step 6 Completed---------------------------------/\n")
        self.N_B = N_B
        return log, Receiver_encrypted_message_Sender
    
    def sender_response_to_receiver(self,log,Receiver_encrypted_message_Sender):

        #Step 7
        log.append("\n/--------------------------------------Step 7--------------------------------------\ \n")
        log.append("{} receive message from {}: \n{}".format(self.sender['name'],self.receiver['name'],Receiver_encrypted_message_Sender))

        Sender_decrypted_message = decrypt_message(Receiver_encrypted_message_Sender, self.sender['private_key']).split(",")
        log.append("{} decrypt message from {}:{}".format(self.sender['name'],self.receiver['name'],Sender_decrypted_message))
        if int(Sender_decrypted_message[0]) == self.N_A:
            log.append("{} verify {}'s nonce complete".format(self.sender['name'],self.sender['name']))
        log.append("{} encrypted response by {} public_key".format(self.sender['name'],self.decrypt_response))
        Sender_response_message = encrypt_message(Sender_decrypted_message[1],self.response[0])
        log.append("{} send response {}:\n{}".format(self.sender['name'],self.receiver['name'],Sender_response_message))
        self.N_B = int(Sender_decrypted_message[1])
        log.append("\n\----------------------------------Step 7 Completed---------------------------------/\n")

        return log, Sender_response_message

    def receiver_response_to_sender(self,log, Sender_response_message, attack=False):
        if attack == True:
            Receiver_decrypted_response = decrypt_message(Sender_response_message, self.sender['private_key'])
            log.append("Malice decrypted message \nEncrypted: {}\nto\nDecrypted: {}".format(Sender_response_message,Receiver_decrypted_response))
            Trent_encrypted_response = encrypt_message(Receiver_decrypted_response,self.response[0])
            log.append("Malice encrypted message by public key of {}".format(self.decrypt_response))
            log.append("Alice(Malice) encrypted message to {}:\n=>{}".format(self.receiver['name'], Trent_encrypted_response))
            return log,Trent_encrypted_response
        else:
            #Step 8
            log.append("\n/--------------------------------------Step 8--------------------------------------\ \n")
            Receiver_decrypted_response = decrypt_message(Sender_response_message, self.receiver['private_key'])
            log.append("Receiver decrypted message \nEncrypted: {}\nto\nDecrypted: {}".format(Sender_response_message,Receiver_decrypted_response))
            if int(Receiver_decrypted_response) == int(self.N_B):
                log.append("{} verify {}'s nonce complete".format(self.receiver['name'],self.receiver['name']))
            else:
                log.append("Verify Fail")
            log.append("\n\----------------------------------Step 8 Completed---------------------------------/\n")
            log.append("Now {} and {} share their private nonces: [{},{}]".format(self.sender['name'], self.receiver['name'],self.N_A,self.N_B))

            return log
    

    
