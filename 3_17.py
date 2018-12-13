import os
import random
from base64 import b64decode
from Crypto.Cipher import AES
cryptopals_2_10 = __import__('2_10')
cryptopals_2_15 = __import__('2_15')


plaintexts = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
]

key = os.urandom(16)


def generate_cipher(plaintext):
    data = b64decode(plaintext)
    iv = os.urandom(16)
    return cryptopals_2_10.aes_128_cbc_encrypt(data, key, iv), iv


def padding_oracle(ciphertext, iv):
    try:
        cryptopals_2_10.aes_128_cbc_decrypt(ciphertext, key, iv)
        valid_padding = True
    except cryptopals_2_10.MalformedPaddingException:
        valid_padding = False
    return valid_padding


def decrypt_block(prev_block, curr_block, last_block=False):
    guess_block = [0] * AES.block_size
    for pad_size in range(1, 17):
        for guess in range(256):
            guess_block[-pad_size] = guess
            pad = bytes([0]*(AES.block_size - pad_size) + [pad_size]*pad_size)
            payload = cryptopals_2_10.xor_bytes(bytes(guess_block), pad)
            payload = cryptopals_2_10.xor_bytes(prev_block, payload)
            valid_padding = padding_oracle(curr_block, payload)
            if last_block and pad_size < 16:
                pad = [0] * AES.block_size
                pad[-(pad_size + 1)] = 16
                payload = cryptopals_2_10.xor_bytes(bytes(pad), payload)
                valid_padding = padding_oracle(curr_block, payload)
            if valid_padding:
                break

    return guess_block


def main():
    plain_text = random.choice(plaintexts)
    print(b64decode(plain_text))
    cipher_text, iv = generate_cipher(plain_text)

    prev_block = iv


    result = []
    for i in range(0, len(cipher_text), AES.block_size):
        block = cipher_text[i:i + AES.block_size]
        last_block = i == ((len(cipher_text) - AES.block_size))
        curr_block = decrypt_block(prev_block, block, last_block)
        print(bytes(curr_block))
        prev_block = block

        result += curr_block

    print(cryptopals_2_10.PKCS7_unpad(bytes(result)))


if __name__ == "__main__":
    main()
