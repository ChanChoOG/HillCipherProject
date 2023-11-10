import numpy as np

def char_to_num(char):
    return ord(char) - ord('A')

def num_to_char(num):
    return chr((num % 26) + ord('A'))

def create_key_matrix(key):
    matrix = []
    for char in key:
        matrix.append(char_to_num(char))
    return np.array(matrix).reshape(3, 3)

def decrypt_block(block, key_matrix):
    # Calculate the modular inverse of the key matrix
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = pow(det, -1, 26)
    adjoint = np.round(np.linalg.inv(key_matrix) * det).astype(int)
    inverse_matrix = (det_inv * adjoint) % 26

    decrypted_text = ''
    for i in range(0, len(block), 3):
        vector = np.array([char_to_num(char) for char in block[i:i+3]])
        decrypted_vector = np.dot(vector, inverse_matrix) % 26
        decrypted_text += ''.join(num_to_char(num) for num in decrypted_vector)
    return decrypted_text

def main():
    key = 'WELOVEBAC'
    key_matrix = create_key_matrix(key)

    encrypted_text = input('Enter the encrypted text: ').upper()

    decrypted_text = decrypt_block(encrypted_text, key_matrix)
    print('Decrypted:', decrypted_text)

if __name__ == '__main__':
    main()
