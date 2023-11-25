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

def encrypt_block(block, key_matrix):
    encrypted_text = ''
    for i in range(0, len(block), 3):
        vector = np.array([char_to_num(char) for char in block[i:i+3]])
        encrypted_vector = np.dot(vector, key_matrix) % 26
        encrypted_text += ''.join(num_to_char(num) for num in encrypted_vector)
    return encrypted_text

def main():
    print("Welcome to the Hill Cipher Encryption Program!")
    print("-------------------------------------------------")

    while True:
        key = input('Enter the key you want to use (Up to 9 characters): ').upper()

        if len(key) <= 9:
            key += 'X' * (9 - len(key))  # Fill the key with 'X's if it's too short
            break
        else:
            print("Invalid key. The key must be 9 characters or less.")

    key_matrix = create_key_matrix(key)

    while True:
        print("\nMenu:")
        print("1. Encrypt a message")
        print("2. Exit")
        choice = input("Enter your choice (1-2): ")

        if choice == "1":
            plaintext = input('\nEnter the plaintext (up to 9 characters): ').upper()
            if len(plaintext) > 9:
                plaintext = plaintext[:9]
            elif len(plaintext) < 9:
                plaintext += 'X' * (9 - len(plaintext))

            encrypted_text = encrypt_block(plaintext, key_matrix)
            print(f"\nEncrypted Message: {encrypted_text}")

            # Summary
            print("\nSummary:")
            print(f"Key: {key}")
            print(f"Original Plaintext: {plaintext}")
            print(f"Encrypted Text: {encrypted_text}")

        elif choice == "2":
            print("\nExiting the encryption program.")
            break

        else:
            print("\nInvalid choice. Please enter 1 or 2.")

if __name__ == '__main__':
    main()
