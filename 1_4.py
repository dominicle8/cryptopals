#Detect single-character XOR
import codecs
import re
cryptopals_1_3 = __import__('1_3')


def main():
    messages = {}

    with open('4.txt') as txt:
        for line in txt:
            line = line.rstrip()
            for i in range(256):
                encrypted_msg = codecs.decode(line, 'hex')
                decrypted_msg = cryptopals_1_3.decrypt_msg(encrypted_msg, i)

                chi2 = cryptopals_1_3.chi_squared(decrypted_msg)
                temp = re.sub(r'[^a-zA-Z0-9_ \n]', '', decrypted_msg)
                if chi2 != 0 and len(temp) == len(decrypted_msg):
                    messages[(decrypted_msg, chr(i))] = chi2

    ranked_messages = sorted(messages.items(), key=lambda x: x[1])

    for msg in ranked_messages:
        print(msg)


if __name__ == "__main__":
    main()
