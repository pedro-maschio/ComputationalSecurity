class Cipher:

   
    def cipher_or_decipher(self, key, message, operation):
        message_length = len(message)
        key_length = len(key)

        if message_length <= 0 or key_length <= 0:
            return "NULL_MSG"

        cipher_text = ""

        i = 0
        for caracter in message:
            if i >= key_length:
                i = 0

            caracter_ord = ord(caracter)
            caracter_key = ord(key[i])

            if operation == 'C':
                ciphered_caracter = chr((caracter_ord + caracter_key)%26+ord('A'))
            else:
                ciphered_caracter = chr((caracter_ord - caracter_key)%26+ord('A'))
            cipher_text += ciphered_caracter

            i += 1
        return cipher_text


c = Cipher()

print(c.cipher_or_decipher("PEDRO", "JOAOANTONIO", 'C'))
print(c.cipher_or_decipher("PEDRO", "YSDFOCXREWD", 'D'))