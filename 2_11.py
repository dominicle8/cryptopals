import os
from random import randint
cryptopals_2_10 = __import__('2_10')

def generate_aes_key():
    return os.urandom(16)


def encryption_oracle(data):
    key = generate_aes_key()
    prefix = os.urandom(randint(5, 10))
    suffix = os.urandom(randint(5, 10))
    plaintext = prefix + data + suffix
    block_mode = randint(0, 1)

    if block_mode == 0:
        ciphertext = cryptopals_2_10.aes_128_ecb_encrypt(plaintext, key)
    else:
        iv = generate_aes_key()
        ciphertext = cryptopals_2_10.aes_128_cbc_encrypt(plaintext, key, iv)

    return ciphertext, block_mode


def guess_mode():
    data = bytes([0x42] * 100)
    ciphertext, blockmode = encryption_oracle(data)

    n = 16
    blocks = [ciphertext[i:i + n] for i in range(0, len(ciphertext), n)]

    guess = 0 if len(blocks) != len(set(blocks)) else 1

    print('Guessed {} when block mode was {}. {}'.format(guess, blockmode, guess == blockmode))


def main():
    for i in range(100):
        guess_mode()


if __name__ == "__main__":
    main()