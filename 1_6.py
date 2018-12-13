#Break repeating-key XOR
from base64 import b64decode
import os
cryptopals_1_3 = __import__('1_3')

file_path = os.path.expanduser('~/Downloads/6.txt')


def main():
    with open(file_path, 'r') as f:
        data = f.read()
    data = b64decode(data)
    edit_distance = {}
    for keysize in range(2,40):
        batches = [data[i*keysize:(i+1)*keysize] for i in range((len(data) + keysize - 1)//keysize)]
        dist = 0
        rounds = 3
        for batch_idx in range(rounds):
            dist += hamming_dist(batches[batch_idx], batches[batch_idx + 1])
        edit_distance[keysize] = dist / (keysize * rounds)

    sorted_keysizes = sorted(edit_distance, key=edit_distance.get)

    for keysize in sorted_keysizes[:3]:
        blocks = []
        for idx in range(keysize):
            blocks.append(data[idx::keysize])
        key = ''
        for b in blocks:
            k, _ = cryptopals_1_3.solve_single_key_xor(b)
            key += k
        print(keysize, key)
        key = key.encode() * len(data)
        plaintext = xor_bytes(data, key)
        print(plaintext)


def hamming_dist(s1, s2):
    b1 = s1
    b2 = s2
    diff = ''.join(list(map(lambda x, y: format(x ^ y, 'b'), b1, b2)))
    return diff.count('1')


def xor_bytes(b1, b2):
    return bytes(list(map(lambda x, y: x ^ y, b1, b2)))


if __name__ == "__main__":
    main()
