from email.mime import base
from random import randrange
import string 

class Cipher:

    def cipher_or_decipher(self, message, key, operation):
        message_length = len(message)
        key_length = len(key)
        message = ''.join(character.lower() for character in message if character.isalpha())

        if message_length <= 0 or key_length <= 0 or key_length <= message_length:
            return "NULL_MSG"

        cipher_text = ""
        num_special = 0

        for i in range(len(message)):
            caracter_ord = ord(message[i])
            special_character = False
            
            if operation == 'C':
                if message[i] >= 'A' and message[i] <= 'Z':
                    ciphered_character = chr((caracter_ord + ord(key[(i-num_special)%len(key)]))%26 + ord('A'))
                else: 
                    special_character = True
            else:
                if message[i] >= 'A' and message[i] <= 'Z':
                    ciphered_character = chr((caracter_ord - ord(key[(i-num_special)%len(key)]))%26 + ord('A'))
                else:
                    special_character = True

            if not special_character:
                cipher_text += ciphered_character
            else:
                num_special += 1
                cipher_text += message[i]

        return cipher_text


class Attack:

    def breakCiphertext(self, cipherText, language='pt-BR'):
        cipherText = ''.join(character.lower() for character in cipherText if character.isalpha())
        matchingsList = self.find_matchings(cipherText) # 10 is the max key length we are considering

        max_key_length =  matchingsList.index(max(matchingsList[:10]))+1 # max key len is 10
        print(max_key_length)
        testGroups = self.groups(cipherText, max_key_length)
        frequencyAnalysis = self.frequency_analysis(testGroups, language)


    def frequency_analysis(self, groupFrequencies, language):
        key_len = len(groupFrequencies)

        baseFrequencies = []
        if language == 'pt-BR':
            with open('freq_pt_br.txt') as f:
                baseFrequencies = f.readlines()
        else:
            with open('freq_en.txt') as f:
                baseFrequencies = f.readlines()   

        baseFrequencies = list(map(float, baseFrequencies))


        for i in range(key_len):
            max = self.get_max_frequency(baseFrequencies, groupFrequencies[i])


    def get_max_frequency(self, baseFrequencies, frequencies):
        letter = 0
        prev_max = 0
        for i in range(26):
            res = 0 
            for j in range(26):
                res += baseFrequencies[j]*frequencies[j]

            if res >= prev_max:
                prev_max = res 
                letter = i

            frequencies = self.shiftLeft(frequencies, 1)

        print(chr(letter+ord('a')), end='')
        print()


    def shiftLeft(self, lista, numShifts):
        return lista[numShifts:] + lista[:numShifts]

    def groups(self, cipherText, key_length):
        frequencies = []
        for i in range(key_length):
            frequencies.append([0]*26)


        for i in range(len(cipherText)):
            frequencies[i%key_length][ord(cipherText[i])-ord('a')] += 1


        for i in range(key_length):
            for j in range(26):
                frequencies[i][j] /= 26
        
   
        return frequencies
        

    def find_matchings(self, cipherText):
        matching_numbers = []

        for i in range(1, len(cipherText)):
            match_count = 0
            temp = i
            for j in range(len(cipherText)):
                if cipherText[j] == cipherText[temp] and cipherText[j] != ' ' and cipherText[temp] != ' ':
                    match_count += 1
                temp += 1
                if temp >= len(cipherText):
                    break
            matching_numbers.append(match_count)

        return matching_numbers




c = Cipher()
a = Attack()


#ciphered_text = "CVJTNAFENMCDMKBXFSTKLHGSOJWHOFUISFYFBEXEINFIMAYSSDYYIJNPWTOKFRHWVWTZFXHLUYUMSGVDURBWBIVXFAFMYFYXPIGBHWIFHHOJBEXAUNFIYLJWDKNHGAOVBHHGVINAULZFOFUQCVFBYNFTYGMMSVGXCFZFOKQATUIFUFERQTEWZFOKMWOJYLNZBKSHOEBPNAYTFKNXLBVUAXCXUYYKYTFRHRCFUYCLUKTVGUFQBESWYSSWLBYFEFZVUWTRLLNGIZGBMSZKBTNTSLNNMDPMYMIUBVMTLOBJHHFWTJNAUFIZMBZLIVHMBSUWLBYFEUYFUFENBRVJVKOLLGTVUZUAOJNVUWTRLMBATZMFSSOJQXLFPKNAULJCIOYVDRYLUJMVMLVMUKBTNAMFPXXJPDYFIJFYUWSGVIUMBWSTUXMSSNYKYDJMCGASOUXBYSMCMEUNFJNAUFUYUMWSFJUKQWSVXXUVUFFBPWBCFYLWFDYGUKDRYLUJMFPXXEFZQXYHGFLACEBJBXQSTWIKNMORNXCJFAIBWWBKCMUKIVQTMNBCCTHLJYIGIMSYCFVMURMAYOBJUFVAUZINMATCYPBANKBXLWJJNXUJTWIKBATCIOYBPPZHLZJJZHLLVEYAIFPLLYIJIZMOUDPLLTHVEVUMBXPIBBMSNSCMCGONBHCKIVLXMGCRMXNZBKQHODESYTVGOUGTHAGRHRMHFREYIJIZGAUNFZIYZWOUYWQZPZMAYJFJIKOVFKBTNOPLFWHGUSYTLGNRHBZSOPMIYSLWIKBANYUOYAPWZXHVFUQAIATYYKYKPMCEYLIRNPCDMEIMFGWVBBMUPLHMLQJWUGSKQVUDZGSYCFBSWVCHZXFEXXXAQROLYXPIUKYHMPNAYFOFHXBSWVCHZXFEXXXAIRPXXGOVHHGGSVNHWSFJUKNZBESHOKIRFEXGUFVKOLVJNAYIVVMMCGOFZACKEVUMBATVHKIDMVXBHLIVWTJAUFFACKHCIKSFPKYQNWOLUMYVXYYKYAOYYPUKXFLMBQOFLACKPWZXHUFJYGZGSTYWZGSNBBWZIVMNZXFIYWXWBKBAYJFTIFYKIZMUIVZDINLFFUVRGSSBUGNGOPQAILIFOZBZFYUWHGIRHWCFIZMWYSUYMAUDMIYVYAWVNAYTFEYYCLPWBBMVZZHZUHMRWXCFUYYVIENFHPYSMKBTMOIZWAIXZFOLBSMCHHNOJKBMBATZXXJSSKNAULBJCLFWXDSUYKUCIOYJGFLMBWHFIWIXSFGXCZBMYMBWTRGXXSHXYKZGSDSLYDGNBXHAUJBTFDQCYTMWNPWHOFUISMIFFVXFSVFRNA"

lista = []
with open('entrada.txt') as f:
    lista = f.readlines()

teste = ""
for s in lista:
    teste += s
a.breakCiphertext(teste, 'en')



# a.breakCiphertext(teste, 'en')