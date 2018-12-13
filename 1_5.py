#Detect repeating-key XOR
from itertools import cycle

KEY = 'ICE'
MSG = 'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'


def main():
    print(xor_encrypt(MSG, KEY))


def xor_encrypt(msg, key):
    return ''.join('{0:02x}'.format(ord(m) ^ ord(k)) for m,k in zip(msg, cycle(key)))


if __name__ == "__main__":
    main()
