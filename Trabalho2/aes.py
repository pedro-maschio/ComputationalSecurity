# Base implementation: https://blog.nindalf.com/posts/implementing-aes/
# https://github.com/boppreh/aes/blob/master/aes.py
import random
from constants import Constants
from utils import convert_key, generate_key

dice = random.SystemRandom()


class AES:

    ''' Initialize the AES object with the given key'''
    def __init__(self, key, message, rounds=10):
        self.rounds = rounds
        self.round_keys = self.__expand_key(key)
        
        

    '''
        Receives a 4x4-byte matrix (the key)
        and returns a list of matrices
    '''
    def __expand_key(self, key):
        key_columns = convert_key(key) 
        
        iteration_size = len(key) // 4 # 4 words for AES-128 (this one), 6 words for AES-192, and 8 words for AES-256. word = 32 bits
        
        i = 1
        
        while len(key_columns) < (self.rounds + 1) * 4:
            word = list(key_columns[-1])
            
            if len(key_columns) % iteration_size == 0: # perform the operation at every 'row'
                word.append(word.pop(0)) # left shift
               
                word = [Constants.sbox[b] for b in word] # amp through s box

                # we only XOR the first byte, other bytes of rcon are all 0
                word[0] ^= Constants.r_con[i]
                
                i += 1
            elif len(key) == 32 and len(key_columns) % iteration_size == 4:
                # Run word through S-box in the fourth iteration when using a
                # 256-bit key.
                word = [Constants.sbox[b] for b in word]

            word = bytes(x^y for x, y in zip(word, key_columns[-iteration_size]))
            
            
            key_columns.append(word)
        retorno = [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]
        print(retorno)
        return retorno


    def encrypt(self, state, expkey, rounds=10):
        keyi = 0
        state = self.add_key(state, expkey[keyi:keyi+4])
        keyi += 4

        for i in range(rounds-1): 
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            
            if i != rounds-1: # the last round doesn't have mix_cols step
                state = self.mix_cols(state)
            state = self.add_key(state, expkey[keyi:keyi+4]) # we use only 16 bytes from the key expansion
            keyi += 4

    '''
        Receives the sate and XOR it against the key
    '''
    def add_key(self, state: bytes, key):
        for i in range(4):
            for j in range(4):
                state[i][j] ^= key[i][j]
        

    '''
        Substitutes the bytes from the state by the respective byte from 
        the S Box.
    '''
    def sub_bytes(self, state):
        for i in range(4):
            for j in range(4):
                state[i][j] = Constants.sbox[state[i][j]]
        return state

    '''
        Applies the invertion of the operation performed in sub_bytes
    '''
    def inverse_sub_bytes(self, state: bytes):
        for i in range(4):
            for j in range(4):
                state[i][j] = Constants.invertsbox[state[i][j]]
        return state

    def shift_rows(self, state: bytes):
        for i in range(1, 4):
            state[i] = self.__shift_left(state[i], i)
        return state

    def inverse_shift_rows(self, state: bytes):
        for i in range(1, 4):
            state[i] = self.__shift_right(state[i], i)
        return state

    def __shift_left(self, state_row, shifts):
        return state_row[shifts:] + state_row[:shifts]

    def __shift_right(self, state_row, shifts):
        return state_row[-shifts:] + state_row[:-shifts]


    '''
        A column-wise operation that involves multiplication and addition in the galois field
    '''
    def mix_cols(self, state):
        for i in range(4):
            col = self.__mix_column(state, i)
            for j in range(4):
                state[j][i] = col[j]
        return state

    def inverse_mix_cols(self, state):
        for i in range(4):
            col = self.__inverse_mix_column(state, i)
            for j in range(4):
                state[j][i] = col[j]
        return state

    def __mix_column(self, state, i):
        c0 = Constants.galoismult2[state[0][i]] ^ Constants.galoismult3[state[1][i]] ^ state[2][i] ^ state[3][i]
        c1 = state[0][i] ^ Constants.galoismult2[state[1][i]] ^ Constants.galoismult3[state[2][i]] ^ state[3][i]
        c2 = state[0][i] ^ state[1][i] ^ Constants.galoismult2[state[2][i]]  ^ Constants.galoismult3[state[3][i]]
        c3 = Constants.galoismult3[state[0][i]] ^ state[1][i] ^ state[2][i] ^ Constants.galoismult2[state[3][i]]

        return [c0, c1, c2, c3]

    def __inverse_mix_column(self, state, i):
        c0 = Constants.galoismult14[state[0][i]] ^ Constants.galoismult11[state[1][i]] ^ Constants.galoismult13[state[2][i]] ^ Constants.galoismult9[state[3][i]]  
        c1 = Constants.galoismult9[state[0][i]] ^ Constants.galoismult14[state[1][i]] ^ Constants.galoismult11[state[2][i]] ^ Constants.galoismult13[state[3][i]]
        c2 = Constants.galoismult13[state[0][i]] ^ Constants.galoismult9[state[1][i]] ^ Constants.galoismult14[state[2][i]] ^ Constants.galoismult11[state[3][i]]
        c3 = Constants.galoismult11[state[0][i]] ^ Constants.galoismult13[state[1][i]] ^ Constants.galoismult9[state[2][i]] ^ Constants.galoismult14[state[3][i]]

        return [c0, c1, c2, c3]