import base64
import hashlib
from math import ceil
from aes import AES
import random as random
import struct
import os
from rsa import RSA 
dice = random.SystemRandom()



# key = b'2b7e151628aed2a6abf7158809cf4f3c'
iv = b'\xe5\xc8!\x8e@\xc6\xc3\xf2FH)s\xed{\x0f\x12'
# encrypted_text = AES(key).encrypt_ctr(b'Pedro de torrres maschio', iv)
# print(AES(key).decrypt_ctr(encrypted_text, iv))



pedro = RSA()
gabigue = RSA()

with open('entrada.txt', 'r', encoding='utf-8') as f:
    plaintext = f.read()

aes_key = dice.getrandbits(128) 



print("Plaintext: " + plaintext)
plaintext = bytes(plaintext, 'utf-8')

key = aes_key.to_bytes(16, 'big')
key = b'\x16&g\xd3\x10\x7f\xf1r2\xe6}\x8ca\x97\xbc#'
print('AES key: ' + hex(int.from_bytes(key, 'big')))

file_hash = hashlib.sha3_256(plaintext)
print('File hash: ' + file_hash.hexdigest())

aes = AES(key)


# This works
# encrypted_file = aes.encrypt_ctr(plaintext, iv)
# print('encrypted_file')
# print(encrypted_file)

# de = aes.decrypt_ctr(encrypted_file, iv)
# print('decrypted_file')
# print(de)







print("aes_key")
aes_key = int.from_bytes(key, 'big')
print(aes_key)

aes_ciphered_key = pedro.oaep_cipher(key, gabigue.public_key)

print("aes_ciphered_key")
print(aes_ciphered_key.to_bytes(aes_ciphered_key.bit_length(), 'big'))


aes_de_oaep_key = gabigue.cipher_or_decipher(aes_ciphered_key, gabigue.private_key)
print("aes_de_oaep_key")
print(aes_de_oaep_key)
aes_deciphered_key = gabigue.oaep_decipher(aes_de_oaep_key.to_bytes(aes_ciphered_key.bit_length(), 'big'))
print("AES DECIPHERED")
print(int.from_bytes(aes_deciphered_key, 'big'))









aes_ciphered_key = pedro.cipher_or_decipher(int.from_bytes(key, 'big'), gabigue.public_key)
print("AES KEY CIPHERED")
print(hex(aes_ciphered_key))

file_ciphered_hash = pedro.cipher_or_decipher(int.from_bytes(file_hash.digest(), 'big'), gabigue.public_key)
print("FILE HASH CIPHERED")
print(hex(file_ciphered_hash))


aes_deciphered_key = gabigue.cipher_or_decipher(aes_ciphered_key, gabigue.private_key)
print("AES KEY DECIPHERED")
print(hex(aes_deciphered_key))

file_deciphered_hash = gabigue.cipher_or_decipher(file_ciphered_hash, gabigue.private_key)
print("FILE HASH DECIPHERED")
print(hex(file_deciphered_hash))










# while True:
#     print("SUPER SIGNATURE CIPHER")
#     print("1. Cifrar com AES CTR")
#     print("2. Decifrar com AES CTR")
#     print("Escolha: ", end='')
#     option = int(input())

#     if option == 1:
#         print("Informe o nome do arquivo a ser cifrado: (.txt) ")
#         file_name = input()

#         with open(file_name, 'r', encoding='utf-8') as f:
#             plaintext = f.read()

#         key = dice.getrandbits(128)
#         print("AES key: " + hex(key))
#         key = key.to_bytes(16, 'big')
#         aes = AES(key)    

#         plaintext = bytes(plaintext, 'utf-8')
        
#         encrypted_file = base64.b64encode(aes.encrypt_ctr(plaintext, iv))

        
#         with open('key.bin', 'wb') as f:
#             f.write(base64.b64encode(key))
#         with open('message.bin', 'wb') as f:
#             f.write(encrypted_file)
        

#     else:
#         with open('key.bin', 'rb') as f:
#             key = f.read()
#             key = base64.b64decode(key)
#         with open('message.bin', 'rb') as f:
#             message = f.read()
#             message = base64.b64decode(message)

#         aes = AES(key)     
#         decrypted_file = aes.decrypt_ctr(message, iv)

#         print(decrypted_file)

#         break