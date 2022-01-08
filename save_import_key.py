import rsa

def export_public_key(public_key, filename):
    with open(filename,"wb") as file:
        file.write(public_key)
        file.close()

def export_private_key(private_key, filename):
    with open(filename,"wb") as file:
        file.write(private_key)
        file.close()

def import_public_key(filename):
    with open(filename, mode='rb') as publicfile:
        keydata = publicfile.read()
    return rsa.PublicKey.load_pkcs1(keydata, 'PEM')

def import_private_key(filename):
    with open(filename, mode='rb') as privatefile:
        keydata = privatefile.read()
    return rsa.PrivateKey.load_pkcs1(keydata)

def encrypt_message(message, public_key):
    try:
        enmessage = rsa.encrypt(message.encode(),public_key)
        return enmessage
    except:
        return None
        
def decrypt_message(message, private_key):
    try:
        demessage = rsa.decrypt(message,private_key).decode()
        return demessage
    except:
        return None