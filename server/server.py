from typing import Any
import socket
#import rsa
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
from pathlib import Path




def save_rsa_private_key(private_key_content: str | bytes, storage_dir: str = "rsa_keys") -> int:
    path = Path(storage_dir)
    path.mkdir(exist_ok=True)

    existing_keys = list(path.glob("private_key_*.pem"))
    counter = len(existing_keys) + 1

    file_path = path / f"private_key_{counter}.pem"

    if isinstance(private_key_content, str):
        file_path.write_text(private_key_content)
    else:
        file_path.write_bytes(private_key_content)

    return counter

def connect_to_client(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    client_socket, client_address = server_socket.accept()
    return client_socket, server_socket

def main():
    print("starting main....")
    host = '0.0.0.0'
    port = 8080
    client_socket, server_socket = connect_to_client(host, port)

    print("client connected")

    RSA_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_pem = RSA_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    save_rsa_private_key(private_pem)

    RSA_public_key = RSA_private_key.public_key()
    public_pem = RSA_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    client_socket.send(public_pem)



if __name__ == "__main__":
    main()
