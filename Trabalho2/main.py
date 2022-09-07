from aes import AES
import random as random
dice = random.SystemRandom()

key = b'2b7e151628aed2a6abf7158809cf4f3c'
aes = AES(key, 'teste')



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