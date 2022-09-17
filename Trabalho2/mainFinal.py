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

    # Criptografamos a chave do AES com o RSA
    aes_key_encrypted = pedro.oaep_cipher(aes_key, gabriel.public_key)
    print(file_hash1)

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
    hash_received_decrypted = gabriel.oaep_decipher(hash_received)
    key_received_decrypted = gabriel.oaep_decipher(key_received)

    # Decodificamos a mensagem com o AES
    aes.key_matrices = aes.expand_key(key_received_decrypted)
    message_received_decrypted = aes.decrypt_ctr(message_received, iv)

    new_hash = hashlib.sha3_256(message_received_decrypted)
    # Verificamos a assinatura da mensagem (comparamos o hash que foi enviado com o hash do arquivo descriptografado)
    print(new_hash.digest())
    print(hash_received_decrypted.hex())


    print(message_received_decrypted)




main(sys.argv[1:])