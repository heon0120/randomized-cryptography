from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# Function call with user-specified directory paths
private_key_directory = input("Enter the private key storage directory:")
public_key_directory = input("Enter the public key storage directory:")
print("[INFO] Generating 100 pairs of keys in public key directory " + private_key_directory + " and private key directory " + public_key_directory + ".")


def create_rsa_key_pairs(private_key_dir, public_key_dir, key_size=8192, key_pairs_num=100):
    if not os.path.exists(private_key_dir):
        os.makedirs(private_key_dir)
    if not os.path.exists(public_key_dir):
        os.makedirs(public_key_dir)

    for i in range(1, key_pairs_num + 1):
        # Generate RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Save private key
        private_key_path = os.path.join(private_key_dir, f"priv{i}.pem")
        print("=================================" + str(i) + "=================================")
        print("[INFO] Private key " + str(i) + " generated.")
        with open(private_key_path, "wb") as private_file:
            private_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        # Save public key
        public_key_path = os.path.join(public_key_dir, f"pub{i}.pem")
        print("[INFO] Public key " + str(i) + " generated.")
        with open(public_key_path, "wb") as public_file:
            public_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )


create_rsa_key_pairs(private_key_directory, public_key_directory)
