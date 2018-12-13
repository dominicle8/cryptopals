from base64 import b64decode
cryptopals_2_10 = __import__('2_10')

def aes_128_ctr_encrypt(data, key, nonce):
    nonce = nonce.to_bytes(8, byteorder='little')
    keystream = bytes()
    for i in range(len(data)):
        block = nonce + i.to_bytes(8, byteorder='little')
        keystream += cryptopals_2_10.aes_128_ecb_encrypt(block, key, False)
    return cryptopals_2_10.xor_bytes(data, keystream)


def aes_128_ctr_decrypt(data, key, nonce):
    return aes_128_ctr_encrypt(data, key, nonce)


def main():
    ciphertext = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    data = b64decode(ciphertext)
    key = "YELLOW SUBMARINE"
    nonce = 0
    plaintext = aes_128_ctr_decrypt(data, key, nonce)
    print(plaintext)


if __name__ == "__main__":
    main()
