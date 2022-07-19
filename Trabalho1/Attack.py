import Cipher

class Attack:

    def breakCiphertext(self, cipherText, language='pt-BR', key_len=None):
        cipherTextTemp = cipherText
        cipherText = ''.join(character.lower() for character in cipherText if (character.isascii() and character.isalpha()))
        matchingsList = self.find_matchings(cipherText) # 10 is the max key length we are considering

        if key_len == None:
            key_len =  matchingsList.index(max(matchingsList[:10]))+1 # max key len is 10
        testGroups = self.groups(cipherText, key_len)
        key = self.frequency_analysis(testGroups, language)
        
        c = Cipher()
        return {'key': key, 'message': c.cipher_or_decipher(cipherTextTemp, key, 'D')}


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

        key = ""
        for i in range(key_len):
            max = self.get_max_frequency_letter(baseFrequencies, groupFrequencies[i])
            key += max
        return key

    def get_max_frequency_letter(self, baseFrequencies, frequencies):
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
        return chr(letter+ord('a'))



    def shiftLeft(self, lista, numShifts):
        return lista[numShifts:] + lista[:numShifts]

    def groups(self, cipherText, key_length):
        frequencies = []
        for i in range(key_length):
            frequencies.append([0]*26)


        for i in range(len(cipherText)):
            if cipherText[i].isalpha():
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
                if cipherText[j] == cipherText[temp] and cipherText[j].isalpha() and cipherText[temp].isalpha():
                    match_count += 1
                temp += 1
                if temp >= len(cipherText):
                    break
            matching_numbers.append(match_count)

        return matching_numbers