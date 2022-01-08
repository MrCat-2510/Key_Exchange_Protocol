import rsa
import random
from save_import_key import *

def create_key():
    #Alice
    Alice_public_key, Alice_private_key = rsa.newkeys(512)

    #Bob
    Bob_public_key, Bob_private_key = rsa.newkeys(512)

    #Trent 
    Trent_public_key, Trent_private_key = rsa.newkeys(512)

    #Malice 
    Malice_public_key, Malice_private_key = rsa.newkeys(512)


    # Alice export key 
    export_public_key(Alice_public_key.save_pkcs1("PEM"),"key/Alice_public_key.pem")
    export_private_key(Alice_private_key.save_pkcs1("PEM"),"key/Alice_private_key.pem")

    # Bob export key
    export_public_key(Bob_public_key.save_pkcs1("PEM"),"key/Bob_public_key.pem")
    export_private_key(Bob_private_key.save_pkcs1("PEM"),"key/Bob_private_key.pem")

    # Trent export key
    export_public_key(Trent_public_key.save_pkcs1("PEM"),"key/Trent_public_key.pem")
    export_private_key(Trent_private_key.save_pkcs1("PEM"),"key/Trent_private_key.pem")

    # Malice export key
    export_public_key(Malice_public_key.save_pkcs1("PEM"),"key/Malice_public_key.pem")
    export_private_key(Malice_private_key.save_pkcs1("PEM"),"key/Malice_private_key.pem")

    print("Export Complete")