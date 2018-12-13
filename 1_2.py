#Fixed XOR
import codecs

def fixed_xor(buffer1, buffer2):
    assert(len(buffer1) == len(buffer2))

    return hex(int(buffer1, 16) ^ int(buffer2, 16))



buffer1 = '1c0111001f010100061a024b53535009181c'
buffer2 = '686974207468652062756c6c277320657965'

print(fixed_xor(buffer1, buffer2))