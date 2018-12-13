from base64 import b64decode
import os
cryptopals_2_10 = __import__('2_10')
cryptopals_3_18 = __import__('3_18')
cryptopals_3_19 = __import__('3_19')


def main():
    plain_texts = []
    with open('20.txt') as txt:
        for line in txt:
            plain_texts.append(b64decode(line))

    key = os.urandom(16)
    nonce = 0
    cipher_texts = [cryptopals_3_18.aes_128_ctr_encrypt(x, key, nonce) for x in plain_texts]
    keystream = cryptopals_3_19.crack_ctr_fixed_nonce(cipher_texts)

    for text in cipher_texts:
        print(cryptopals_2_10.xor_bytes(text, keystream))


if __name__ == "__main__":
    main()
