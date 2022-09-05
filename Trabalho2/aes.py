import random 
dice = random.SystemRandom()

class AES:


    def generate_key(self):
        self.key = dice.getrandbits(128)



    def add_key(self, state, key):
        for i in range(4):
            state[i] ^= key[i]
        
    def encrypt(self, state, expkey, rounds=10):
        keyi = 0
        self.add_key(state, expkey[keyi:keyi+4])
        keyi += 4


    def sub_bytes(self, state):
        for i in range(len(state)):
            state[i] = sub_word(state[i])