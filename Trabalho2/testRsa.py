import multiprocessing
import random as random
import threading

from utils import calc_num_bytes


dice = random.SystemRandom()
from rsa import RSA


def one_test():
    pedro = RSA()
    gabigue = RSA()
    aes_key = dice.getrandbits(128) 
    key = aes_key.to_bytes(16, 'big')
    aes_ciphered_key = pedro.oaep_cipher(key, gabigue.public_key)
    aes_ciphered_oaep_key = gabigue.cipher_or_decipher(aes_ciphered_key, gabigue.private_key) # we uncipher

    l = threading.Lock()
    
    l.acquire()
    print("aes_ciphered_oaep_key: ", end='')
    print(hex(aes_ciphered_oaep_key))
    l.release()
    
    aes_deciphered_key = gabigue.oaep_decipher(aes_ciphered_oaep_key.to_bytes(calc_num_bytes(aes_ciphered_key), 'big'))
    
    l.acquire()
    print("aes_deciphered_key")
    print(hex(int.from_bytes(aes_deciphered_key, 'big')))
    l.release()
    
    l.acquire()
    with open('saidas.txt', 'a') as f:
        f.write(hex(aes_key) + ' == ' + hex(int.from_bytes(aes_deciphered_key, 'big')) + ' = ' + str(hex(aes_key) == hex(int.from_bytes(aes_deciphered_key, 'big'))) + '\n')
    l.release()

processes = []
for i in range(20):
    p = multiprocessing.Process(target=one_test)
    processes.append(p)
    p.start()

for process in processes:
    process.join()