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
        self.e = 65537
        self.d = egcd(self.e, self.phi)[1] 

        if(self.d < 0):
            self.d += self.phi
        
        
        self.private_key = [self.n, self.d] 
        self.public_key = [self.n, self.e]

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
        

    def oaep_cipher(self, message: bytes, key: List[int], label: str = "") -> int:
        mLen = len(message) # tamanho da mensagem que estamos recebendo (em bytes)
        hLen = 32 # tamanho do hash em bytes (256 bits)
        k = 256 # tamanho da saída em bytes (são 2048 bits)

        if mLen > k - 2*hLen - 2:
            return "mensagem muito grande"
        lHash = hashlib.sha3_256(bytes(label, 'utf-8')).digest()
        paddingString = (0).to_bytes(k - mLen - 2*hLen - 2, 'big')

        db = lHash + paddingString + (1).to_bytes(1, 'big') + message

        seed = dice.getrandbits(256).to_bytes(hLen, 'big')
        dbMask = self.mgf1(seed, k - hLen - 1)
        maskedDb = bytes_xor(db, dbMask)
        seedMask = self.mgf1(maskedDb, hLen)
        maskedSeed = bytes_xor(seed, seedMask)


        em = (0).to_bytes(1, "big") + maskedSeed + maskedDb

        return self.cipher_or_decipher(int.from_bytes(em, 'big'), key)


    def oaep_decipher(self, ciphertext: bytes, label: str = "") -> bytes:
        
        hLen = 32 
        k = 256
        if k < 2*hLen + 2:
            raise Exception("erro na descriptografação k >= 2*hLen + 2")
        if k != len(ciphertext):
            raise Exception("a mensagem deve ter tamanho k = {:d}, tamanho recebido = {:d}".format(k, len(ciphertext)))

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
        padd = db[hLen:]
        for i in padd:
            if i == 1:
                break 
            idx += 1

        return padd[idx+1:]


    '''
        Converte um inteiro x para uma representação em string de bytes de tamanho xLen
    '''
    def I2OSP(self, x: int, xLen: int = 4):
        return x.to_bytes(xLen, 'big')

    def mgf1(self, mfgSeed: bytes, maskLen: int):
        t = b""
        i = 0 
        while(len(t) < maskLen):
            c = self.I2OSP(i, 4)
            t = t + hashlib.sha3_256(mfgSeed + c).digest()
            i += 1
        return t[:maskLen]
        
