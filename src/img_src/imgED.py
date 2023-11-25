import numpy as np
from PIL import Image
import os


def char_to_num(char):
    return ord(char) - ord('A')

def create_key_matrix(key):
    matrix = []
    for char in key:
        matrix.append(char_to_num(char))
    return np.array(matrix).reshape(3, 3)

def load_image(path):
    return Image.open(path).convert('L')  # Convert to grayscale

def save_image(image, path):
    image.save(path)

def process_image(image, key_matrix, mode='encrypt'):
    image_array = np.array(image)
    processed_image_array = np.zeros_like(image_array)

    # Ensure the block size matches the key matrix size
    block_size = key_matrix.shape[0]

    for i in range(0, image_array.shape[0], block_size):
        for j in range(0, image_array.shape[1], block_size):
            block = image_array[i:i+block_size, j:j+block_size]
            if block.shape != (block_size, block_size):
                continue  # Skip incomplete blocks
            if mode == 'encrypt':
                processed_block = encrypt_block(block, key_matrix)
            else:
                processed_block = decrypt_block(block, key_matrix)
            processed_image_array[i:i+block_size, j:j+block_size] = processed_block

    return Image.fromarray(processed_image_array)

def encrypt_block(block, key_matrix):
    return (np.dot(block, key_matrix) % 256).astype(np.uint8)

def decrypt_block(block, key_matrix):
    # Calculate the modular inverse of the key matrix in mod 256
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = pow(det, -1, 256)
    adjoint = np.round(np.linalg.inv(key_matrix) * det).astype(int)
    inverse_matrix = (det_inv * adjoint) % 256

    return (np.dot(block, inverse_matrix) % 256).astype(np.uint8)

# Example usage
def main():
    key = "WELOVEBAC"  # key
    key_matrix = create_key_matrix(key)

    det = int(np.round(np.linalg.det(key_matrix)))
    if np.gcd(det, 256) != 1:
        print("The key matrix is not suitable for decryption (determinant is not invertible under modulo 256).")
        return

    # Adjust the paths
    original_image_path = '../../images/original/cypherMachine.png'
    encrypted_image_path = '../../images/encrypted/encryptedCypherMachine.png'
    decrypted_image_path = '../../images/decrypted/decryptedCypherMachine.png'

    # Encrypt with multiple passes
    original_image = load_image(original_image_path)
    encrypted_image = original_image
    for _ in range(2):  # Number of encryption passes
        encrypted_image = process_image(encrypted_image, key_matrix, mode='encrypt')
    save_image(encrypted_image, encrypted_image_path)

    # Decrypt
    encrypted_image = load_image(encrypted_image_path)
    decrypted_image = encrypted_image
    for _ in range(2):  # Number of decryption passes (should match encryption passes)
        decrypted_image = process_image(decrypted_image, key_matrix, mode='decrypt')
    save_image(decrypted_image, decrypted_image_path)

if __name__ == "__main__":
    main()

