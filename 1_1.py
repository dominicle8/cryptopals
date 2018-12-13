import codecs

#convert hex to base64

hex_string = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
s = codecs.decode(hex_string, 'hex')
b64 = codecs.encode(s, 'base64')

print(b64)