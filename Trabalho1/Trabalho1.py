from random import randrange
import string 

class Cipher:

    def cipher_or_decipher(self, message, key, operation):
        message_length = len(message)
        key_length = len(key)

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
        matchingsList = self.find_matchings(cipherText)[:10] # 10 is the max key length we are considering
        
        guessedKeyLength =  matchingsList.index(max(matchingsList))+1

        
        key = []
        for i in range(guessedKeyLength):
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
                if cipherText[j] == cipherText[temp]:
                    match_count += 1
                temp += 1
                if temp >= len(cipherText):
                    break
            matching_numbers.append(match_count)

        return matching_numbers




c = Cipher()
a = Attack()


ciphered_text = "CVJTNAFENMCDMKBXFSTKLHGSOJWHOFUISFYFBEXEINFIMAYSSDYYIJNPWTOKFRHWVWTZFXHLUYUMSGVDURBWBIVXFAFMYFYXPIGBHWIFHHOJBEXAUNFIYLJWDKNHGAOVBHHGVINAULZFOFUQCVFBYNFTYGMMSVGXCFZFOKQATUIFUFERQTEWZFOKMWOJYLNZBKSHOEBPNAYTFKNXLBVUAXCXUYYKYTFRHRCFUYCLUKTVGUFQBESWYSSWLBYFEFZVUWTRLLNGIZGBMSZKBTNTSLNNMDPMYMIUBVMTLOBJHHFWTJNAUFIZMBZLIVHMBSUWLBYFEUYFUFENBRVJVKOLLGTVUZUAOJNVUWTRLMBATZMFSSOJQXLFPKNAULJCIOYVDRYLUJMVMLVMUKBTNAMFPXXJPDYFIJFYUWSGVIUMBWSTUXMSSNYKYDJMCGASOUXBYSMCMEUNFJNAUFUYUMWSFJUKQWSVXXUVUFFBPWBCFYLWFDYGUKDRYLUJMFPXXEFZQXYHGFLACEBJBXQSTWIKNMORNXCJFAIBWWBKCMUKIVQTMNBCCTHLJYIGIMSYCFVMURMAYOBJUFVAUZINMATCYPBANKBXLWJJNXUJTWIKBATCIOYBPPZHLZJJZHLLVEYAIFPLLYIJIZMOUDPLLTHVEVUMBXPIBBMSNSCMCGONBHCKIVLXMGCRMXNZBKQHODESYTVGOUGTHAGRHRMHFREYIJIZGAUNFZIYZWOUYWQZPZMAYJFJIKOVFKBTNOPLFWHGUSYTLGNRHBZSOPMIYSLWIKBANYUOYAPWZXHVFUQAIATYYKYKPMCEYLIRNPCDMEIMFGWVBBMUPLHMLQJWUGSKQVUDZGSYCFBSWVCHZXFEXXXAQROLYXPIUKYHMPNAYFOFHXBSWVCHZXFEXXXAIRPXXGOVHHGGSVNHWSFJUKNZBESHOKIRFEXGUFVKOLVJNAYIVVMMCGOFZACKEVUMBATVHKIDMVXBHLIVWTJAUFFACKHCIKSFPKYQNWOLUMYVXYYKYAOYYPUKXFLMBQOFLACKPWZXHUFJYGZGSTYWZGSNBBWZIVMNZXFIYWXWBKBAYJFTIFYKIZMUIVZDINLFFUVRGSSBUGNGOPQAILIFOZBZFYUWHGIRHWCFIZMWYSUYMAUDMIYVYAWVNAYTFEYYCLPWBBMVZZHZUHMRWXCFUYYVIENFHPYSMKBTMOIZWAIXZFOLBSMCHHNOJKBMBATZXXJSSKNAULBJCLFWXDSUYKUCIOYJGFLMBWHFIWIXSFGXCZBMYMBWTRGXXSHXYKZGSDSLYDGNBXHAUJBTFDQCYTMWNPWHOFUISMIFFVXFSVFRNA"
testPortuguese = "O AMOR  PACIENTE O AMOR  BONDOSO NO INVEJA NO SE VANGLORIA NO SE ORGULHA NO MALTRATA NO PROCURA SEUS INTERESSES NO SE IRA FACILMENTE NO GUARDA RANCOR O AMOR NO SE ALEGRA COM A INJUSTIA MAS SE ALEGRA COM A VERDADE TUDO SOFRE TUDO CR TUDO ESPERA TUDO SUPORTA NO FUI EU QUE ORDENEI A VOC SEJA FORTE E CORAJOSO NO SE APAVORE NEM DESANIME POIS O SENHOR O SEU DEUS ESTAR COM VOC POR ONDE VOC ANDAR PORQUE SOU EU QUE CONHEO OS PLANOS QUE TENHO PARA VOCS DIZ O SENHOR PLANOS DE FAZLOS PROSPERAR E NO DE CAUSAR DANO PLANOS DE DAR A VOCS ESPERANA E UM FUTURO NO SE AMOLDEM AO PADRO DESTE MUNDO MAS TRANSFORMEMSE PELA RENOVAO DA SUA MENTE PARA QUE SEJAM CAPAZES DE EXPERIMENTAR E COMPROVAR A BOA AGRADVEL E PERFEITA VONTADE DE DEUS ENTO PEDRO APROXIMOUSE DE JESUS E PERGUNTOU SENHOR QUANTAS VEZES DEVEREI PERDOAR A MEU IRMO QUANDO ELE PECAR CONTRA MIM AT SETE VEZES JESUS RESPONDEU EU DIGO A VOC NO AT SETE MAS AT SETENTA VEZES SETE VOCS OREM ASSIM PAI NOSSO QUE ESTS NOS CUS SANTIFICADO SEJA O TEU NOME VENHA O TEU REINO SEJA FEITA A TUA VONTADE ASSIM NA TERRA COMO NO CU DNOS HOJE O NOSSO PO DE CADA DIA PERDOA AS NOSSAS DVIDAS ASSIM COMO PERDOAMOS AOS NOSSOS DEVEDORES E NO NOS DEIXES CAIR EM TENTAO MAS LIVRANOS DO MAL PORQUE TEU  O REINO O PODER E A GLRIA PARA SEMPRE AMM"
testPortugueseCipher = c.cipher_or_decipher(testPortuguese, 'JOAO', 'C')
# print(c.cipher_or_decipher(ciphered_text, 'JOAO', 'D'))
# print(a.grid_generator(ciphered_text))
# print(a.coincidence_finder(ciphered_text, a.grid_generator(ciphered_text)))

a.breakCiphertext(testPortugueseCipher)