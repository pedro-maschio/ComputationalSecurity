import base64
from email.mime import base
import hashlib
import sys
from aes import AES
from rsa import RSA
import random

from utils import calc_num_bytes 
dice = random.SystemRandom()

def main(file_name):
    if len(file_name) != 1:
        exit(1)
    
    # Geramos os objetos que representam as pessoas que vão se comunicar
    pedro = RSA()
    gabriel = RSA()

    aes_key = dice.getrandbits(128).to_bytes(16, 'big')
    iv = dice.getrandbits(128).to_bytes(16, 'big')

    aes = AES(aes_key)

    with open(file_name[0], 'rb') as f:
        file = f.read()

    file_hash1 = hashlib.sha3_256(file).digest()

    print('Hash do arquivo lido: ' + file_hash1.hex())
    print('Chave utilizada para criptografá-lo: ' + aes_key.hex())

    # Criptografamos o arquivo com o AES
    file_encrypted = aes.encrypt_ctr(file, iv)

    print("MENSAGEM CIFRADA: ")
    print(str(file_encrypted))

    # Criptografamos a chave do AES com o RSA
    aes_key_encrypted = pedro.oaep_cipher(aes_key, gabriel.public_key)

    # Criptografamos o hash do arquivo com o RSA também
    file_hash1_encrypted = pedro.oaep_cipher(file_hash1, gabriel.public_key)
    
    # Codificamos em Base 64 e salvamos os arquivos
    file_hash1_b64 = base64.b64encode(file_hash1_encrypted.to_bytes(calc_num_bytes(file_hash1_encrypted), 'big'))
    file_encrypted_b64 = base64.b64encode(file_encrypted)
    aes_key_encrypted_b64 = base64.b64encode(aes_key_encrypted.to_bytes(calc_num_bytes(aes_key_encrypted), 'big'))

    with open('hash.bin', 'wb') as f:
        f.write(file_hash1_b64)
    with open('message.bin', 'wb') as f:
        f.write(file_encrypted_b64)
    with open('key.bin', 'wb') as f:
        f.write(aes_key_encrypted_b64)

    input('Arquivo criptografado, pressione enter para continuar')


    # Abrimos os arquivos
    with open('hash.bin', 'rb') as f:
        hash_received = base64.b64decode(f.read())
    with open('message.bin', 'rb') as f:
        message_received = base64.b64decode(f.read())
    with open('key.bin', 'rb') as f:
        key_received = base64.b64decode(f.read())
    
    # Decodificamos o hash do arquivo e a chave do AES com o RSA
    hash_received_decrypted = gabriel.cipher_or_decipher(int.from_bytes(hash_received, 'big'), gabriel.private_key)
    hash_received_decrypted_and_unpadded = gabriel.oaep_decipher(hash_received_decrypted.to_bytes(calc_num_bytes(hash_received_decrypted)+1, 'big'))

    key_received_decrypted = gabriel.cipher_or_decipher(int.from_bytes(key_received, 'big'), gabriel.private_key)
    key_received_decrypted_and_unpadded = gabriel.oaep_decipher(key_received_decrypted.to_bytes(calc_num_bytes(key_received_decrypted)+1, 'big'))

    # Decodificamos a mensagem com o AES
    aes.key_matrices = aes.expand_key(key_received_decrypted_and_unpadded)
    message_received_decrypted = aes.decrypt_ctr(message_received, iv)
    for i in reversed(message_received_decrypted):
        if i == 0:
            message_received_decrypted = message_received_decrypted[:(len(message_received_decrypted)-1)]

    new_hash = hashlib.sha3_256(message_received_decrypted).hexdigest()


    print("MENSAGEM DECIFRADA: ")
    print(message_received_decrypted)

    # Verificamos a assinatura da mensagem (comparamos o hash que foi enviado com o hash do arquivo descriptografado)
    if hash_received_decrypted_and_unpadded.hex() == new_hash:
        print("Assinatura correta!!")
    else:
        print("Assinatura incorreta, arquivo adulterado!!")

    




main(sys.argv[1:])