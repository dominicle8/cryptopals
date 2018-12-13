from Crypto.Cipher import AES


class MalformedPaddingException(Exception):
    pass

def PKCS7_pad(data, block_size):
    padding = block_size - (len(data) % block_size)
    assert padding <= 255
    return data + (chr(padding)*padding).encode()


def PKCS7_unpad(data):
    padding = data[-1]
    suffix = data[-padding:]
    if len(set(suffix)) != 1:
        raise MalformedPaddingException
    return data[:len(data) - padding]


def aes_128_ecb_encrypt(data, key, padding=True):
    cipher = AES.new(key, AES.MODE_ECB)
    if padding:
        data = PKCS7_pad(data, AES.block_size)
    return cipher.encrypt(data)


def aes_128_ecb_decrypt(data, key, padding=True):
    cipher = AES.new(key, AES.MODE_ECB)
    if padding:
        data = PKCS7_unpad(data)
    return cipher.decrypt(data)


def xor_bytes(b1, b2):
    return bytes(list(map(lambda x, y: x ^ y, b1, b2)))


def aes_128_cbc_encrypt(data, key, iv):
    plaintext = PKCS7_pad(data, AES.block_size)
    ciphertext = b''
    prev_block = iv
    for i in range(0, len(plaintext), AES.block_size):
        block = aes_128_ecb_encrypt(xor_bytes(plaintext[i:i + AES.block_size], prev_block), key, False)
        ciphertext += block
        prev_block = block
    return ciphertext


def aes_128_cbc_decrypt(ciphertext, key, iv):
    plaintext = b''
    prev_block = iv
    for i in range(0, len(ciphertext), AES.block_size):
        block = xor_bytes(aes_128_ecb_decrypt(ciphertext[i:i + AES.block_size], key, False), prev_block)
        plaintext += block
        prev_block = ciphertext[i:i + AES.block_size]
    plaintext = PKCS7_unpad(plaintext)
    return plaintext


