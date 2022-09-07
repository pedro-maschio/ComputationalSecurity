
plaintext = "1234567891"
padding_len = (16 - (len(plaintext) % 16))
padding = bytes([padding_len] * padding_len)

print(padding)