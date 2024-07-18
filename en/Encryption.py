import json
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import datetime

KEY_DIR = "key"  # Fixed key directory name
SAVE_DIR = "encryptedfile"  # Encrypted result save directory name
SAVE_FORMAT = "%Y%m%d%H%M%S.encrypted"


def encrypt(text):

    # Generate a random list of key numbers between 1 and 15
    key_numbers = random.sample(range(1, 101), len(text))

    # Load the RSA public key corresponding to each key number
    keys = {}
    for key_number in key_numbers:
        with open(f"{KEY_DIR}/pub{key_number}.pem", "r") as f:
            key = RSA.import_key(f.read())
            keys[key_number] = key

    # Encrypt each character with a random key and store it in JSON data
    encrypted_data = {}
    for i, char in enumerate(text):
        key_number = key_numbers[i]
        cipher = PKCS1_OAEP.new(keys[key_number])
        encrypted_data[str(key_number)] = cipher.encrypt(char.encode("utf-8")).hex()

    return json.dumps(encrypted_data)


def save_encrypted_data(encrypted_json, filename):

    with open(f"{SAVE_DIR}/{filename}", "w") as f:
        f.write(encrypted_json)


if __name__ == "__main__":
    text = input("Enter the plaintext to encrypt: ")

    encrypted_json = encrypt(text)

    now = datetime.datetime.now()
    filename = now.strftime(SAVE_FORMAT)

    save_encrypted_data(encrypted_json, filename)
    print(f"\n\n[INFO] Encrypted result saved to {SAVE_DIR}/{filename}.")
