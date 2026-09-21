import pathlib
from victim.file import File
import socket

#def connect_to_Ariel(ip, port):



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
    #ip ="192.168.1.188"
    # port = 8080
    # sock = connect_to_Ariel(ip, port)




if __name__ == "__main__":
    main()