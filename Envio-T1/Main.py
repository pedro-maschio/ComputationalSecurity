from Cipher import Cipher
from Attack import Attack

def readFile(filename):
    lines = []
    with open(filename) as f:
        lines = f.readlines()

    output = ""
    for s in lines:
        output += s

    return output

def main():
    c = Cipher()
    a = Attack()
    
    while True:
        print("CIPHER PROGRAM")

        print("1. To cipher message")
        print("2. To decipher message")
        print("3. To break ciphered message")
        print('4. Exit')
        print("Option: ", end='')
    
        option = int(input())

        if option != 4:
            print('Read from file or from stdin (1 for file, 2 for stdin): ', end='')
            read_option = int(input())

            if(read_option == 1):
                print('Insert the filename: ', end ='')
                filename = input()
                message = readFile(filename)
            else:
                print('Insert the message: ')
                message = input()

        if option == 1 or option == 2:
            print("Insert the key: ", end='')
            key = input()

            if option == 1:
                operation = 'C'
                output_text = "Ciphered message: "
            else:
                operation = 'D'
                output_text = "Deciphered message: "

            print("\n\n" + output_text)
            print(c.cipher_or_decipher(message, key, operation), end='\n\n')
        elif option == 3:
            print("Is it in portuguese or english? (1 for pt-BR, 2 for en): ", end='')
            language = int(input())

            if  language == 1:
                language = 'pt-BR'
            else:
                language = 'en'

            result = a.break_ciphertext(message, language)

            print("\n\nKEY: " + result['key'])
            print("MESSAGE: " + result['message'] + "\n\n")

            print("Is it what you expected (1 for yes, 2 for no): ", end='')
            repeat = int(input())

            if repeat == 2:
                print('Choose a key length: ', end='')
                key_l = int(input())

                result = a.break_ciphertext(message, language, key_l)

                print("\n\nKEY: " + result['key'])
                print("MESSAGE: " + result['message'] + "\n\n")

        else:
            break

main()


