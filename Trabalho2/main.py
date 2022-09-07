from aes import AES
import random as random
import os 
dice = random.SystemRandom()



key = b'2b7e151628aed2a6abf7158809cf4f3c'
iv = b'\xe5\xc8!\x8e@\xc6\xc3\xf2FH)s\xed{\x0f\x12'
encrypted_text = AES(key).encrypt_ctr(b'00112233445566778899aabbccddeeff', iv)

print(AES(key).decrypt_ctr(encrypted_text, iv))


# while True:
#     print("SUPER SIGNATURE CIPHER")
#     print("1. Cifrar com AES")
#     print("Escolha: ", end='')
#     option = int(input())

#     if option == 1:
#         print("Informe o nome do arquivo a ser cifrado: ")
#         file_name = input()

#         with open(file_name, 'rb') as f:
#             aes = AES(dice.getrandbits(128))    

#             byte = f.read(1) # read one byte at a time
#             while byte:
#                 # use byte
#                 pass
#     else:
#         break