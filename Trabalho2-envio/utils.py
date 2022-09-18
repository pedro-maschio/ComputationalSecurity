import random as random
dice = random.SystemRandom()

'''
    Gera uma chave de 128-bits e a converte para uma matriz 4x4.
'''
def generate_key():
    k = dice.getrandbits(128)
    key = []
    for i in range(128//8):
        if i % 4 == 0:
            key.append([k & 0xff]) # get the last byte from the k
            k >>= 8
        else:
            key[-1].append(k & 0xff)
    return key

'''
    Convert the key (16-byte array) to a 4x4 byte matrix
'''
def byte_array_to_matrice(key):
    return [list(key[i:i+4]) for i in range(0, len(key), 4)]

def bytes_xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def calc_num_bytes(n: int):
    cnt = 0 

    while n != 0:
        n >>= 8
        cnt += 1
    return cnt

