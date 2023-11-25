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
    det = int(np.round(np.linalg.det(key_matrix)))
    if np.gcd(det, 26) != 1:
        raise ValueError("The key matrix is not invertible in modulo 26 arithmetic.")

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
    print("Welcome to the Hill Cipher Decryption Program!")
    print("-------------------------------------------------")

    while True:
        key = input('Enter the key used for encryption (Up to 9 characters): ').upper()

        if len(key) <= 9:
            key += 'X' * (9 - len(key))  # Fill the key with 'X's if it's too short
            break
        else:
            print("Invalid key. The key must be 9 characters or less.")

    key_matrix = create_key_matrix(key)

    while True:
        print("\nMenu:")
        print("1. Decrypt a message")
        print("2. Exit")
        choice = input("Enter your choice (1-2): ")

        if choice == "1":
            encrypted_text = input('\nEnter the encrypted text: ').upper()
            decrypted_text = decrypt_block(encrypted_text, key_matrix)
            print(f"\nDecrypted Message: {decrypted_text}")

            # Summary
            print("\nSummary:")
            print(f"Key: {key}")
            print(f"Encrypted Text: {encrypted_text}")
            print(f"Decrypted Text: {decrypted_text}")

        elif choice == "2":
            print("\nExiting the decryption program.")
            break

        else:
            print("\nInvalid choice. Please enter 1 or 2.")

if __name__ == '__main__':
    main()
