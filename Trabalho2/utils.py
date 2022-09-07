import random as random
dice = random.SystemRandom()

'''
    Generate a 128-bit key and converts it to a 4x4-byte matrix
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

