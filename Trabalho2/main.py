import base64
from email.mime import base
from aes import AES
import random as random
import os 
dice = random.SystemRandom()



# key = b'2b7e151628aed2a6abf7158809cf4f3c'
iv = b'\xe5\xc8!\x8e@\xc6\xc3\xf2FH)s\xed{\x0f\x12'
# encrypted_text = AES(key).encrypt_ctr(b'Pedro de torrres maschio', iv)
# print(AES(key).decrypt_ctr(encrypted_text, iv))


while True:
    print("SUPER SIGNATURE CIPHER")
    print("1. Cifrar com AES CTR")
    print("2. Decifrar com AES CTR")
    print("Escolha: ", end='')
    option = int(input())

    if option == 1:
        print("Informe o nome do arquivo a ser cifrado: (.txt) ")
        file_name = input()

        with open(file_name, 'r', encoding='utf-8') as f:
            plaintext = f.read()

        key = dice.getrandbits(128)
        print("AES key: " + hex(key))
        key = key.to_bytes(16, 'big')
        aes = AES(key)    

        plaintext = bytes(plaintext, 'utf-8')
        
        encrypted_file = base64.b64encode(aes.encrypt_ctr(plaintext, iv))

        
        with open('key.bin', 'wb') as f:
            f.write(base64.b64encode(key))
        with open('message.bin', 'wb') as f:
            f.write(encrypted_file)
        

    else:
        with open('key.bin', 'rb') as f:
            key = f.read()
            key = base64.b64decode(key)
        with open('message.bin', 'rb') as f:
            message = f.read()
            message = base64.b64decode(message)

        aes = AES(key)     
        decrypted_file = aes.decrypt_ctr(message, iv)

        print(decrypted_file)

        break