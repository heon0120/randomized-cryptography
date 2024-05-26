from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
import datetime as time

# 사용자가 지정한 디렉토리 경로로 함수 호출
private_key_directory = input("개인키저장 디렉토리를 입력하세요:")
public_key_directory = input("공개키저장 디렉토리를 입력하세요:")
now = time.datetime.now()
print ("[INFO " + str(now) + "]" "공개키 디렉토리" + private_key_directory + "와, 개인키 디렉토리" + public_key_directory + "에 키파일 100쌍의 키를 생성합니다.")
def create_rsa_key_pairs(private_key_dir, public_key_dir, key_size=8192, key_pairs_num=100):
    if not os.path.exists(private_key_dir):
        os.makedirs(private_key_dir)
    if not os.path.exists(public_key_dir):
        os.makedirs(public_key_dir)

    for i in range(1, key_pairs_num + 1):
        # RSA 키 쌍 생성
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # 개인 키 저장
        private_key_path = os.path.join(private_key_dir, f"priv{i}.pem")
        print("=================================" + str(i) + "=================================")
        print ("[INFO " + str(now) + "] " + "개인키" + str(i) +"번 생성됨.")
        with open(private_key_path, "wb") as private_file:
            private_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        # 공개 키 저장
        public_key_path = os.path.join(public_key_dir, f"pub{i}.pem")
        print ("[INFO " + str(now) + "] " + "공개키" + str(i) +"번 생성됨.")
        with open(public_key_path, "wb") as public_file:
            public_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )



create_rsa_key_pairs(private_key_directory, public_key_directory)