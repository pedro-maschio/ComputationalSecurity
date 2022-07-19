class Cipher:

    def cipher_or_decipher(self, message, key, operation):
        message_length = len(message)
        key_length = len(key)
        message = ''.join(character.lower() for character in message if character.isascii())
        key = key.lower()
   

        if message_length <= 0 or key_length <= 0 or message_length < key_length:
            return "NULL_MSG"

        cipher_text = ""
        num_special = 0

        for i in range(len(message)):
            caracter_ord = ord(message[i]) - ord('a')
            special_character = False

            if operation == 'C':
                if message[i].isalpha():
                    ciphered_character = chr((caracter_ord + ord(key[(i-num_special)%len(key)]) - ord('a'))%26 + ord('a'))
                else: 
                    special_character = True
            else:
                if message[i].isalpha():
                    ciphered_character = chr((caracter_ord - (ord(key[(i-num_special)%len(key)]) - ord('a')))%26 + ord('a'))
                else:
                    special_character = True
            

            if not special_character:
                cipher_text += ciphered_character
            else:
                num_special += 1
                cipher_text += message[i]

        return cipher_text