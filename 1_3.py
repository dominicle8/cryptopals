#single-byte XOR cipher
import codecs
import collections


english_freq = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]
letters = [chr(c) for c in range(ord('a'), ord('z') + 1)]
expected_freq = dict(zip(letters, english_freq))
expected_freq[' '] = .13000


def main():
    s = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    encrypted_msg = codecs.decode(s, 'hex')
    key, _ = solve_single_key_xor(encrypted_msg)
    print(key)


def solve_single_key_xor(encrypted_msg):
    messages = {}
    for i in range(256):
        decrypted_msg = decrypt_msg(encrypted_msg, i)
        #chi2 = chi_squared(decrypted_msg)
        #if chi2 != 0:
        #    messages[(decrypted_msg, chr(i))] = chi2
        messages[(decrypted_msg, chr(i))] = sum([expected_freq.get(c, 0) for c in decrypted_msg.lower()])

    ranked_messages = sorted(messages.items(), key=lambda x: x[1], reverse=True)
    return ranked_messages[0][0][1], ranked_messages[0][0][0]

def decrypt_msg(msg, key):
    decrypted_msg = [chr(a ^ key) for a in msg]
    return ''.join(decrypted_msg)


def chi_squared(msg):
    character_count = collections.Counter([c for c in msg.lower() if (c >= 'a' and c <= 'z')])

    length = sum(character_count.values())
    result = 0
    for character, count in character_count.items():
        observed_frequency = count/length
        result += ((observed_frequency - expected_freq[character])**2)/expected_freq[character]
    return result


if __name__ == "__main__":
    main()