import numpy as np

def char_to_num(char):
    return ord(char) - ord('A')

def num_to_char(num):
    return chr(num + ord('A'))

def create_key_matrix(key):
    matrix = []
    for char in key:
        matrix.append(char_to_num(char))
    return np.array(matrix).reshape(3, 3)

def encrypt_block(block, key_matrix):
    encrypted_text = ''
    for i in range(0, len(block), 3):
        vector = np.array([char_to_num(char) for char in block[i:i+3]])
        encrypted_vector = np.dot(vector, key_matrix) % 26
        encrypted_text += ''.join(num_to_char(num) for num in encrypted_vector)
    return encrypted_text

def main():

    key = input('Enter the key you want to use: (Up to 9 characters)').upper()
        #if key == '


    key_matrix = create_key_matrix(key)

    while True:
        plaintext = input('Enter the plaintext (up to 9 characters) or type "exit" to quit: ').upper()
        
        if plaintext == "EXIT":
            print("Exiting the program.")
            break

        if len(plaintext) > 9:
            plaintext = plaintext[:9]
        elif len(plaintext) < 9:
            plaintext += 'X' * (9 - len(plaintext))

        encrypted_text = encrypt_block(plaintext, key_matrix)
        print('Encrypted:', encrypted_text)

if __name__ == '__main__':
    main()
