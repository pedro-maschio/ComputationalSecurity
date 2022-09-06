# Base implementation: https://blog.nindalf.com/posts/implementing-aes/
# https://github.com/boppreh/aes/blob/master/aes.py
import random
from aes.constants import Constants 
dice = random.SystemRandom()


class AES:


    def generate_key(self):
        self.key = dice.getrandbits(128)



        
    def encrypt(self, state, expkey, rounds=10):
        keyi = 0
        state = self.add_key(state, expkey[keyi:keyi+4])
        keyi += 4

        for i in range(rounds):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_cols(state)
            state = self.add_key(state, expkey[keyi:keyi+4]) # we use only 16 bytes from the key expansion
            keyi += 4

        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_key(state, expkey[keyi:keyi+4])

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
            state[i] = self.shift_left(state[i], i)
        return state

    def inverse_shift_rows(self, state: bytes):
        for i in range(1, 4):
            state[i] = self.shift_right(state[i], i)
        return state

    def shift_left(self, state_row, shifts):
        return state_row[shifts:] + state_row[:shifts]

    def shift_right(self, state_row, shifts):
        return state_row[-shifts:] + state_row[:-shifts]


    '''
        For each column, apply the galois multiplication accordingly
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