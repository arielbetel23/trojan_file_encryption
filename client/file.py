class File:
    def __init__(self, name, path, size):
        self.name = name
        self.path = path
        self.size = size

    def __str__(self):
        return f"File(name='{self.name}', path='{self.path}', size={self.size} bytes)"