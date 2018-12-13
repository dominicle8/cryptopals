import os
import base64
cryptopals_2_10 = __import__('2_10')


key = os.urandom(16)
appendix = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')


def encryption_oracle(data):
    return cryptopals_2_10.aes_128_ecb_encrypt(data + appendix, key)


def discover_block_size(enc_oracle):
    init_size = len(enc_oracle(b''))
    pad = b'a'
    while init_size == len(enc_oracle(pad)):
        pad += b'a'

    return len(enc_oracle(pad)) - init_size


def decrypt_byte(partial_payload, block_size, enc_oracle):
    buffer_size = (block_size - (len(partial_payload) + 1)) % block_size
    buffer = bytes([ord('A')]*buffer_size)
    cipher_text = enc_oracle(buffer)

    decrypted_byte = b''
    for i in range(256):
        guess = enc_oracle(buffer + partial_payload + bytes([i]))

        if guess[:(buffer_size + len(partial_payload) + 1)] == cipher_text[:(buffer_size + len(partial_payload) + 1)]:
            decrypted_byte = bytes([i])
            break

    return decrypted_byte


def main():
    block_size = discover_block_size(encryption_oracle)
    payload_size = len(encryption_oracle(b''))

    payload = b''
    for i in range(payload_size):
        payload += decrypt_byte(payload, block_size, encryption_oracle)

    print(cryptopals_2_10.PKCS7_unpad(payload))


if __name__ == "__main__":
    main()
