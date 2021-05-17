import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from os import path
from os import urandom
from cryptography.fernet import Fernet
key = b''

if path.isfile("key.key"): # check if the key is exist

    file = open('key.key', 'rb')  # Open the file as wb to read bytes
    key = file.read()  # The key will be type bytes
    file.close()
    print("Your key has been successfuly imported \n\n")
    
    

else:
    new_key()
    
    
def new_key():
    global key
    password_provided = input("Enter your masterkey password: ")  # This is input in the form of a string
    
    password = password_provided.encode()  # Convert to type bytes
    salt = urandom(16)  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once

    file = open('key.key', 'wb')  # Open the file as wb to write bytes
    file.write(key)  # The key is type bytes still
    file.close()

    print("Key has been saved",key)



def encrypting(message):
    global key
    message = message.encode() # turn it to bytes

    f = Fernet(key)
    encrypted = f.encrypt(message)  # Encrypt the bytes. The returning object is of type bytes
    encrypted = str(encrypted)
    return encrypted[1:len(encrypted)]



def decrypting(message):# turn it to bytes
    global key
    try:
        encrypted = message.encode()
        print(encrypted)
        f = Fernet(key)
        decrypted = f.decrypt(encrypted)  # Decrypt the bytes. The returning object is of type bytes
        print("Decrypting successfuly \n\n")
        decrypted = str(decrypted)
        

        return decrypted[2:len(decrypted)-1]
    except Exception as e:
        print("Invalid Key - Unsuccessfully decrypted")
        
        
   
        
while True:
    choice = str(input("Do you want to 'encrypt' or 'decrypt' ?: "))
    if choice == "encrypt" or choice == "en":
        message = input("Type the message that you want to encypt: ")
        print(f"Key for word '{message}' is {encrypting(message)}")

        
    if choice == "decrypt" or choice == "de":
        encrypted_key = input("Enter the encrypted key must in '....': ")

        print(decrypting(encrypted_key))
