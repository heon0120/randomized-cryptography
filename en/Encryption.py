import json
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import datetime

KEY_DIR = "key"  # 고정된 키 디렉토리 이름
SAVE_DIR = "encryptedfile"  # 암호화 결과 저장 디렉토리 이름
SAVE_FORMAT = "%Y%m%d%H%M%S.encrypted"

def encrypt(text):

    # 1~15 사이의 랜덤한 키 번호 목록을 생성
    key_numbers = random.sample(range(1, 101), len(text))

    # 각 키 번호에 해당하는 RSA 공개 키를 로드
    keys = {}
    for key_number in key_numbers:
        with open(f"{KEY_DIR}/pub{key_number}.pem", "r") as f:
            key = RSA.import_key(f.read())
            keys[key_number] = key

    # 각 문자를 랜덤한 키로 암호화하고 JSON 데이터에 저장
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
    text = input("암호화할 평문을 입력하세요: ")

    encrypted_json = encrypt(text)

    # 현재 시간을 기반으로 파일 이름을 생성
    now = datetime.datetime.now()
    filename = now.strftime(SAVE_FORMAT)

    save_encrypted_data(encrypted_json, filename)
    print(f"\n\n[INFO {now}] 암호화 결과를 {SAVE_DIR}/{filename} 파일에 저장했습니다.")
