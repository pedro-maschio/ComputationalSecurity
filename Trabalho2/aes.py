# Base implementation: https://blog.nindalf.com/posts/implementing-aes/
# https://github.com/boppreh/aes/blob/master/aes.py
from pydoc import plain
import random
from constants import Constants
from utils import byte_array_to_matrice, generate_key, byte_array_to_matrice

dice = random.SystemRandom()


class AES:


    ''' Inicializa o AES com a dada chave'''
    def __init__(self, key, rounds=10):
        self.rounds = rounds
        self.key_matrices = self.expand_key(key)
        

    '''
        Recebe a chave e a expande
    '''
    def expand_key(self, key):
        key_columns = byte_array_to_matrice(key) 
        iteration_size = len(key) // 4 # 4 words for AES-128 (this one), 6 words for AES-192, and 8 words for AES-256. word = 32 bits
        i = 1
        
        while len(key_columns) < (self.rounds + 1) * 4:
            word = list(key_columns[-1])
            
            if len(key_columns) % iteration_size == 0: # perform the operation at every 'row'
                word.append(word.pop(0)) # left shift
               
                word = [Constants.sbox[b] for b in word] # pass through s box

                # we only XOR the first byte, other bytes of rcon are all 0
                word[0] ^= Constants.r_con[i]
                
                i += 1
            elif len(key) == 32 and len(key_columns) % iteration_size == 4:
                word = [Constants.sbox[b] for b in word]

            word = bytes(x^y for x, y in zip(word, key_columns[-iteration_size]))
            key_columns.append(word)

        retorno = [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]
        
        return retorno


    '''
        Criptografa um único bloco de 16 bytes de texto e retorna uma matriz 4-4.
    '''
    def encrypt(self, plaintext):
        keyi = 0

        plaintext = byte_array_to_matrice(plaintext)
        
        plaintext = self.add_key(plaintext, self.key_matrices[0])
        keyi += 4
   
        for i in range(1, self.rounds): 
            plaintext = self.sub_bytes(plaintext)
            plaintext = self.shift_rows(plaintext)
            if i != self.rounds-1: # the last round doesn't have mix_cols step
                plaintext = self.mix_cols(plaintext)
            plaintext = self.add_key(plaintext, self.key_matrices[i]) # we use only 16 bytes from the key expansion
            keyi += 4
            
        
        return bytes(sum(plaintext, [])) # converts the 4x4 matrix to 16-byte array

    def divide_in_blocks(self, plaintext, block_size=16):
        while len(plaintext) % block_size != 0:
            # PKCS#7: we fill the last n blocks with n bytes of value n https://stackoverflow.com/questions/13572253/what-kind-of-padding-should-aes-use
            padding_len = (16 - (len(plaintext) % 16))
            # actually we are filling with zeroes now
            padding = bytes([0] * padding_len)
            plaintext = plaintext + padding
        retorno = [plaintext[i:i+16] for i in range(0, len(plaintext), block_size)] 
        
        return retorno

    def increment_iv(self, iv):
        saida = list(iv)

        for i in reversed(range(len(saida))):
            if saida[i] == 0xFF:
                saida[i] = 0 # we can't increment more than FF
            else:
                saida[i] += 1
                break 
        return bytes(saida)

    def xor_bytes(self, a, b):
        """ Returns a new byte array with the elements xor'ed. """
        return bytes(i^j for i, j in zip(a, b))


    #  https://www.gurutechnologies.net/blog/aes-ctr-encryption-in-c/
    def encrypt_ctr(self, plaintext: bytes, iv: bytes):
        
        blocks = []
        temp = iv 

        for block in self.divide_in_blocks(plaintext):
            # In CTR mode encrypt we XOR the block message with Initializing Vector (iv)
           
            blk = self.xor_bytes(block, self.encrypt(temp))
            blocks.append(blk)
            temp = self.increment_iv(temp)
        return b''.join(blocks)

    '''
        Decrifra uma mensagem em modo CTR, o código é igual ao criptografia.
    '''
    def decrypt_ctr(self, ciphertext: bytes, iv: bytes):
        
        blocks = []
        temp = iv 

        for block in self.divide_in_blocks(ciphertext):
            # In CTR mode encrypt we XOR the block message with Initializing Vector (iv)
            blk = self.xor_bytes(block, self.encrypt(temp))
            blocks.append(blk)
            temp = self.increment_iv(temp)
        return b''.join(blocks)


    '''
        Recebe o estado e faz o XOR com a chave.
    '''
    def add_key(self, state: bytes, key):
        for i in range(4):
            for j in range(4):
                state[i][j] ^= key[i][j]
        return state

    '''
        Substitui os bytes do estado atual pelos bytes da S box
    '''
    def sub_bytes(self, state):
        for i in range(4):
            for j in range(4):
                state[i][j] = Constants.sbox[state[i][j]]
        return state

    '''
        Aplica a operação de inversão 
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
        Uma operação feita nas colunas que envolve a multiplicação e adição no campo de Galois
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