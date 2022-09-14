from typing import List
from utils import bytes_xor
import hashlib
from math import ceil
from re import M
from rsa_key import get_key
from egcd import egcd
import random 
dice = random.SystemRandom()

class RSA:
    def __init__(self):
        self.p, self.q = self.get_keys()
        self.n = self.p * self.q
        self.phi = (self.p-1)*(self.q-1)
        self.e = self.generateE(self.phi)
        self.d = egcd(self.e, self.phi)[1] # https://crypto.stackexchange.com/questions/5889/calculating-rsa-private-exponent-when-given-public-exponent-and-the-modulus-fact

        
        self.private_key = [self.n, self.d] 
        self.public_key = [self.n, self.e]
    
    def generateE(self, phi):
        while True:
            possibleE = dice.randrange(3, phi)
            if egcd(possibleE, phi)[0] == 1: # egcd[1] == gcd
                return possibleE 

    def get_keys(self):
        p = get_key()
        q = get_key()

        while p == q:
            q = get_key()
        return (p, q)


    '''
        Cifra ou decifra uma mensagem
    '''
    def cipher_or_decipher(self, message: int, key: List[int]):
        return pow(message, key[1], key[0])
        

    # https://www.rfc-editor.org/rfc/rfc8017#section-7.1
    def oaep_cipher(self, message: bytes, label: str = "") -> bytes:
        mLen = len(message) # tamanho da mensagem que estamos recebendo (em bytes)
        hLen = 32 # tamanho do hash em bytes (256 bits)
        k = 256 # tamanho da saída em bytes (são 2048 bits)

        if mLen > k - 2*hLen - 2:
            return "message too long"
        lHash = hashlib.sha3_256(bytes(label, 'utf-8')).digest()
        paddingString = (0).to_bytes(k - mLen - 2*hLen - 2, 'big')

        db = lHash + paddingString + bytes(0x1) + message

        seed = dice.getrandbits(hLen*8).to_bytes(hLen, 'big')
        dbMask = self.mgf1(seed, k - hLen - 1)
        maskedDb = bytes_xor(db, dbMask)
        seedMask = self.mgf1(maskedDb, hLen)
        maskedSeed = bytes_xor(seed, seedMask)

        return bytes(0x0) + maskedSeed + maskedDb

    # https://www.rfc-editor.org/rfc/rfc8017#section-7.1.2
    def oaep_decipher(self, ciphertext: bytes, label: str = "") -> bytes:
        hLen = 32 
        k = 256
        if k < 2*hLen + 2:
            return "decryption error"

        em = ciphertext

        Y = em[0]
        maskedSeed = em[1: hLen+1]
        maskedDB = em[-(k-hLen-1):]
        seedMask = self.mgf1(maskedDB, hLen)
        seed = bytes_xor(maskedSeed, seedMask)
        dbMask = self.mgf1(seed, k - hLen - 1)
        db = bytes_xor(maskedDB, dbMask)
        lHash = db[:hLen]

        idx = 0
        for i in db[hLen:]:
            idx += 1
            if i == 1:
                break 
        return db[idx:] # is the message


        

    # https://www.rfc-editor.org/rfc/rfc8017#section-4.1

    '''
        Converte um inteiro x para uma representação em string de bytes de tamanho xLen
    '''
    def I2OSP(self, x: int, xLen: int = 4):
        return x.to_bytes(4, 'big')

    # https://www.rfc-editor.org/rfc/rfc8017#appendix-B
    def mgf1(self, mfgSeed: bytes, maskLen: int):
        t = b""
        hLen = 32

        for i in range(ceil(maskLen / hLen)):
            c = self.I2OSP(i, 4)
            t = t + hashlib.sha3_256(mfgSeed + c).digest()
        return t[:maskLen]
        
