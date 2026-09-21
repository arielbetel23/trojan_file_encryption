import socket
import rsa
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization



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
