import os
import base64
import sys
cryptopals_2_10 = __import__('2_10')


key = os.urandom(16)
prefix = os.urandom(int.from_bytes(os.urandom(1), sys.byteorder))
appendix = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')


def encryption_oracle(data):
    return cryptopals_2_10.aes_128_ecb_encrypt(prefix + data + appendix, key)


def discover_prefix_size(enc_oracle, block_size):
    c0 = enc_oracle(b'')
    c1 = enc_oracle(b'a')

    prefix_size = 0
    for i in range(0, len(c1), block_size):
        if c0[i:i + block_size] != c1[i:i + block_size]:
            prefix_size = i
            break

    for i in range(block_size):
        c3 = b'b' * (2 * block_size + i)
        cipher_text = enc_oracle(c3)

        if discover_repeating_blocks(cipher_text, block_size):
            if i != 0:
                prefix_size = prefix_size + block_size - i
            break

    return prefix_size


def discover_repeating_blocks(cipher_text, block_size):
    repeating_blocks = False
    for j in range(0, len(cipher_text) - 1, block_size):
        if cipher_text[j:j + block_size] == cipher_text[j + block_size:j + 2*block_size]:
            repeating_blocks = True
    return repeating_blocks


def discover_block_size(enc_oracle):
    init_size = len(enc_oracle(b''))
    pad = b'a'
    while init_size == len(enc_oracle(pad)):
        pad += b'a'

    return len(enc_oracle(pad)) - init_size


def decrypt_byte(partial_payload, block_size, prefix_size, enc_oracle):
    buffer_size = (block_size - prefix_size - (len(partial_payload) + 1)) % block_size
    buffer = bytes([ord('A')]*buffer_size)
    cipher_text = enc_oracle(buffer)

    decrypted_byte = b''
    for i in range(256):
        guess = enc_oracle(buffer + partial_payload + bytes([i]))

        if guess[:(buffer_size + prefix_size + len(partial_payload) + 1)] == cipher_text[:(buffer_size + prefix_size + len(partial_payload) + 1)]:
            decrypted_byte = bytes([i])
            break

    return decrypted_byte


def main():
    block_size = discover_block_size(encryption_oracle)
    prefix_size = discover_prefix_size(encryption_oracle, block_size)
    payload_size = len(encryption_oracle(b'')) - prefix_size

    payload = b''
    for i in range(payload_size):
        payload += decrypt_byte(payload, block_size, prefix_size, encryption_oracle)

    print(cryptopals_2_10.PKCS7_unpad(payload))


if __name__ == "__main__":
    main()
