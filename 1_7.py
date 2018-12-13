from Crypto.Cipher import AES
from base64 import b64decode
import os


def main():
    key = 'YELLOW SUBMARINE'
    cipher = AES.new(key, AES.MODE_ECB)
    file_path = os.path.expanduser('~/Downloads/7.txt')
    with open(file_path, 'r') as f:
        data = f.read()

    data = b64decode(data)
    msg = cipher.decrypt(data).decode('utf-8')
    print(msg)


if __name__ == "__main__":
    main()
