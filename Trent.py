import rsa
from save_import_key import *
# Alice
Alice = {
    "name": "Alice",
    "public_key_name": "Alice",
    "private_key_name": "Alice",
    "public_key":import_public_key("key/Alice_public_key.pem"),
    "private_key": import_private_key("key/Alice_private_key.pem")
}
#Bob
Bob = {
    "name": "Bob",
    "public_key_name": "Bob",
    "private_key_name": "Bob",
    "public_key": import_public_key("key/Bob_public_key.pem"),
    "private_key": import_private_key("key/Bob_private_key.pem")
}
#Malice
Malice ={
    "name":"Malice",
    "public_key_name": "Malice",
    "private_key_name": "Malice",
    "public_key": import_public_key("key/Malice_public_key.pem"),
    "private_key" : import_private_key("key/Malice_private_key.pem")
}
#Trent
Trent ={
    "name":"Trent",
    "public_key_name": "Trent",
    "private_key_name": "Trent",
    "public_key": import_public_key("key/Trent_public_key.pem"),
    "private_key" : import_private_key("key/Trent_private_key.pem")
}
# Malice_Attack
Malice_attack ={
    "name": "Alice(Malice)",
    "public_key_name": "Alice",
    "private_key_name": "Malice",
    "public_key":import_public_key("key/Malice_public_key.pem"),
    "private_key" : import_private_key("key/Malice_private_key.pem")
}
def request_public_key(request):
    try:
        decrypted_request = decrypt_message(request,Trent["private_key"]).split(',')
        send_user = check_user(decrypted_request[0])
        request_user = check_user(decrypted_request[1])
        text = "Trent decrypt request from {}: {}".format(send_user['name'],decrypted_request)

        return text, [request_user['public_key'],rsa.encrypt(request_user['name'].encode(),send_user['public_key'])]
    except:
        return None, None


def check_user(name, attack=False):
    users = [Alice, Bob, Trent, Malice, Malice_attack]
    try:
        for user in users:
            if user['name'] == name:
                    return user
        
    except:
        return None 
        
