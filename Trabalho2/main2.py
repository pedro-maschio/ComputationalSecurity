from rsa import RSA
import hashlib

pedro = RSA()
gabigue = RSA()

file_hash = hashlib.sha3_256()

print(pedro.private_key)
print(pedro.public_key)

print(gabigue.private_key)
print(gabigue.public_key)