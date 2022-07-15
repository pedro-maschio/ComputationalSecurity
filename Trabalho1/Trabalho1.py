from random import randrange
import string 

class Cipher:

    def cipher_or_decipher(self, message, key, operation):
        message_length = len(message)
        key_length = len(key)
        message = ''.joing(character.lower() for character in message if character.isalpha())

        if message_length <= 0 or key_length <= 0:
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
        matchingsList = self.find_matchings(cipherText) # 10 is the max key length we are considering

        l =  matchingsList.index(max(matchingsList))+1
        
        for guessedKeyLength in range(1, l):
            key = []
            for i in range(0, guessedKeyLength):
                percentages = self.make_percentages(cipherText, i, guessedKeyLength)
                max_percentage = self.get_max_percentage(percentages, language) + 1
                key.append(max_percentage)

            res = ""
            for i in key:
                res += chr(i+64)
            print(res)

    def get_max_percentage(self, percentages, language):

        baseFrequencies = []
        if language == 'pt-BR':
            with open('freq_pt_br.txt') as f:
                baseFrequencies = f.readlines()
        else:
            with open('freq_en.txt') as f:
                baseFrequencies = f.readlines()   
        baseFrequencies = list(map(float, baseFrequencies))
        
        totalList = []
        for i in range(26):
            total = 0 
            for j in range(26):
                total += percentages[j]*baseFrequencies[j]
            totalList.append(total)
            percentages = percentages[1:] + percentages[:1]
   
        return totalList.index(max(totalList))

            

    def make_percentages(self, cipherText, keyLength, keyGuess):
        alphabet = string.ascii_uppercase
        frequencies = {character:0 for character in alphabet}

        # Contamos as frequencias em "Batches" de tamanho keyGuess
        for x in range(len(cipherText)):
            if x % keyGuess == keyLength:
                if cipherText[x] in alphabet:
                    frequencies[cipherText[x]] += 1 

        percentages = []

        for character in alphabet:
            percentages.append(frequencies[character]/len(cipherText))
        return percentages

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