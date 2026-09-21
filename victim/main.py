import pathlib
from victim.file import File


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

