def PKCS7_pad(data, block_size):
    padding = block_size - (len(data) % block_size)
    assert padding <= 255
    return data + (chr(padding)*padding).encode()

