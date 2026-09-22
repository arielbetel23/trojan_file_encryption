import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding



class File:
    def __init__(self, name, path, size):
        self.name = name
        self.path = path
        self.size = size

    def __str__(self):
        return f"File(name='{self.name}', path='{self.path}', size={self.size} bytes)"


    def encrypt_chunk(self, chunk, key):
        if not hasattr(self, '_encryptor'):
            self._iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(self._iv))
            self._encryptor = cipher.encryptor()
            self._padder = padding.PKCS7(128).padder()

            padded_chunk = self._padder.update(chunk)
            return self._iv + self._encryptor.update(padded_chunk)

        padded_chunk = self._padder.update(chunk)
        return self._encryptor.update(padded_chunk)


    def finish_encryption(self):
        if hasattr(self, '_encryptor'):
            padded_chunk = self._padder.finalize()
            result = self._encryptor.update(padded_chunk) + self._encryptor.finalize()
            del self._encryptor
            del self._padder
            return result
        return b""


    def encrypt_file(self, key):
        temp_path = self.path + ".tmp"

        with open(self.path, "rb") as in_file, open(temp_path, "wb") as out_file:
            while True:
                chunk = in_file.read(8192)
                if not chunk:
                    break

                encrypted_bytes = self.encrypt_chunk(chunk, key)
                out_file.write(encrypted_bytes)

            final_bytes = self.finish_encryption()
            out_file.write(final_bytes)

        os.remove(self.path)
        os.rename(temp_path, self.path)