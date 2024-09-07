from tqdm import tqdm
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import datetime
 
KEY_DIR = "key"  
DATA_DIR = "encryptedfiles  
 
def decrypt_large_file(file_name):
    # Assuming all files are encoded in UTF-8
    encoding = "utf-8"

    # Read the file from the get directory
    with open(f"{DATA_DIR}/{file_name}", "r", encoding=encoding) as f:
        # Process the file line by line
        for line in iter(f.readline, ""):
            encrypted_json = json.loads(line)

            # Load the RSA private key for each key number
 
    # 4. Load the RSA private key for each key number
    keys = {}
    for key_number, encrypted_text in encrypted_json.items():
        with open(f"{KEY_DIR}/priv{key_number}.pem", "r") as f:
            key = RSA.import_key(f.read())
        keys[key_number] = key
 
    # 8. Decrypt each encrypted character with the corresponding key and combine the plaintext
    decrypted_text = ""
    for key_number, encrypted_text in tqdm(encrypted_json.items(), desc="Decrypting"):
        try:
            cipher = PKCS1_OAEP.new(keys[key_number])
            decrypted_char = cipher.decrypt(bytes.fromhex(encrypted_text)).decode("utf-8")
            decrypted_text += decrypted_char
        except ValueError as e:
            print(f"[ERROR] Decryption failed for key {key_number}\nError code: {e}")
 
    return decrypted_text
 
if __name__ == "__main__":
    file_name = input("Enter the number in front of the .encrypted file in the get directory: ") + ".encrypted"

    decrypted_text = decrypt_large_file(file_name)
    print(f"\n\n[INFO] Decrypted text: {decrypted_text}")
