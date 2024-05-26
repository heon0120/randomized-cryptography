import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import datetime
KEY_DIR = "key"  # 고정된 키 디렉토리 이름
DATA_DIR = "encryptedfile"  # 암호화된 JSON 데이터 파일이 있는 디렉토리 이름
now = datetime.datetime.now()
def decrypt_large_file(file_name):


  # 모든 파일을 UTF-8로 인코딩된 것으로 가정함
  encoding = "utf-8"

  # get 디렉토리에서 파일을 읽기
  with open(f"{DATA_DIR}/{file_name}", "r", encoding=encoding) as f:
    # 파일을 조각별로 읽어 처리
    for line in iter(f.readline, ""):
      encrypted_json = json.loads(line)

      # 각 키 번호에 해당하는 RSA 개인 키를 로드
      keys = {}
      for key_number, encrypted_text in encrypted_json.items():
        with open(f"{KEY_DIR}/priv{key_number}.pem", "r") as f:
          key = RSA.import_key(f.read())
          keys[key_number] = key

      # 암호화된 문자를 각 키로 해석하고 평문을 조합
      decrypted_text = ""
      for key_number, encrypted_text in encrypted_json.items():
        try:
          cipher = PKCS1_OAEP.new(keys[key_number])
          decrypted_char = cipher.decrypt(bytes.fromhex(encrypted_text)).decode("utf-8")
          decrypted_text += decrypted_char
          progress = int(key_number) / len(encrypted_json) * 100
          print(f"\r복호화 중... {min(progress, 100):.0f}% [{'-' * int(min(progress, 100) / 2)}]", end="")
        except ValueError as e:
          print(f"[ERROR {now}] 키 {key_number}에 대한 복호화 실패 \n에러코드: {e}")

  return decrypted_text

if __name__ == "__main__":
  file_name = input("get 디렉토리 내 .encrypted 파일 앞 번호를 입력하세요: ") + ".encrypted"

  decrypted_text = decrypt_large_file(file_name)
  print(f"\n\n[INFO {now}] 해석된 평문: {decrypted_text}")

