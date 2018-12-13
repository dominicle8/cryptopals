import random
import struct
import os
import sys
import time
cryptopals_2_10 = __import__('2_10')
cryptopals_3_21 = __import__('3_21')


def mt19937_encrypt(seed, plain_text):
    key_stream = b''
    mt = cryptopals_3_21.MT19937(seed)
    while len(key_stream) < len(plain_text):
        key_stream += struct.pack('>L', mt.extract_number())

    return cryptopals_2_10.xor_bytes(plain_text, key_stream)


def mt19937_decypt(seed, cipher_text):
    return mt19937_encrypt(seed, cipher_text)


def mt19937_brute_force(known_text, cipher_text):
    return [seed for seed in range(2**16) if known_text in mt19937_decypt(seed, cipher_text)]


def mt19937_generate_token():
    seed = int(time.time())
    mt = cryptopals_3_21.MT19937(seed)
    return mt.extract_number()


def mt19937_validate_token(token, time_delta):
    seed = int(time.time())
    valid_token = any(cryptopals_3_21.MT19937(seed + delta).extract_number() == token for delta in range(-time_delta, time_delta))
    return valid_token



def main():
    seed = random.randint(0, 2**16 - 1)
    plain_text = bytes([ord('A')]*14)
    rand_prefix = os.urandom(int.from_bytes(os.urandom(1), sys.byteorder))


    cipher_text = mt19937_encrypt(seed, rand_prefix + plain_text)

    seed_guesses = mt19937_brute_force(plain_text, cipher_text)
    print(seed, seed_guesses)

    token = mt19937_generate_token()
    valid_token = mt19937_validate_token(token, 100)
    print(valid_token)

    mt = cryptopals_3_21.MT19937(0)
    print(mt19937_validate_token(mt.extract_number(), 100))


if __name__ == "__main__":
    main()
