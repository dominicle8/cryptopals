cryptopals_2_10 = __import__('2_10')


def valid_padding(plaintext):
    cryptopals_2_10.PKCS7_unpad(plaintext)
    return True


def main():
    padded_text = 'ICE ICE BABY\x04\x04\x04\x04'.encode('ascii')
    print(valid_padding(padded_text))
    bad_padded_text = 'ICE ICE BABY\x05\x05\x05\x05'.encode('ascii')
    valid_padding(bad_padded_text)


if __name__ == "__main__":
    main()