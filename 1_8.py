import os
import codecs


def main():
    file_path = os.path.expanduser('~/Downloads/8.txt')
    with open(file_path, 'r') as f:
        data = f.read()
    data = data.split('\n')

    unique_blocks = {}

    for line in data:
        ciphertext = codecs.decode(line, 'hex_codec')
        n = 16
        chunks = [ciphertext[i*n:(i+1)*n] for i in range((len(ciphertext) + n - 1)//n)]
        chunks = set(chunks)
        if len(chunks):
            unique_blocks[line] = len(chunks)

    print(min(unique_blocks, key=unique_blocks.get))


if __name__ == "__main__":
    main()
