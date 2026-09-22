import socket
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def save_rsa_key_pair(private_pem: bytes, public_pem: bytes, storage_dir: str = "secured_sessions") -> int:
    path = Path(storage_dir)
    path.mkdir(exist_ok=True)

    existing_keys = list(path.glob("session_*.pem"))
    counter = len(existing_keys) + 1

    file_path = path / f"session_{counter}.pem"

    combined_keys = f"{private_pem.decode('utf-8').strip()}\n\n{public_pem.decode('utf-8').strip()}\n"

    file_path.write_text(combined_keys)

    return counter


def append_data_to_latest_file(aes_key_bytes: bytes, client_name: str, storage_dir: str = "secured_sessions") -> None:
    path = Path(storage_dir)
    if not path.exists():
        return

    existing_keys = list(path.glob("session_*.pem"))
    if not existing_keys:
        return

    latest_file = max(existing_keys, key=lambda f: f.stat().st_mtime)

    encoded_aes_key = base64.b64encode(aes_key_bytes).decode("utf-8")

    append_content = f"\n-----BEGIN CLIENT NAME-----\n{client_name}\n-----END CLIENT NAME-----\n\n-----BEGIN AES KEY-----\n{encoded_aes_key}\n-----END AES KEY-----\n"

    with latest_file.open("a", encoding="utf-8") as file:
        file.write(append_content)

    new_file_path = path / f"{latest_file.stem}_{client_name}.pem"
    latest_file.rename(new_file_path)


def connect_to_client(host: str, port: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    client_socket, _ = server_socket.accept()
    return client_socket, server_socket


def decrypt_aes_key(encrypted_aes_key_bytes: bytes, rsa_private_key_object) -> bytes:
    aes_key_bytes = rsa_private_key_object.decrypt(
        encrypted_aes_key_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return aes_key_bytes


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

    RSA_public_key = RSA_private_key.public_key()
    public_pem = RSA_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    save_rsa_key_pair(private_pem, public_pem)

    client_socket.send(public_pem)

    received_data = client_socket.recv(4096)

    name_bytes, encrypted_AES_key = received_data.split(b"||", 1)
    client_name = name_bytes.decode("utf-8")

    print(f"Connected to client: {client_name}")

    client_socket.close()
    server_socket.close()

    decrypted_AES_key = decrypt_aes_key(encrypted_AES_key, RSA_private_key)
    append_data_to_latest_file(decrypted_AES_key, client_name)


if __name__ == "__main__":
    main()