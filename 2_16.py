import os
cryptopals_2_10 = __import__('2_10')


key = os.urandom(16)
iv = os.urandom(16)


def sanitize_data(data):
    keywords = {
        '=': '%61',
        '%': '%37',
        ';': '%59'
    }
    for k, v in keywords.items():
        data = data.replace(k, v)
    return data


def retrieve_token(data):
    prefix = 'comment1=cooking%20MCs;userdata='
    suffix = ';comment2=%20like%20a%20pound%20of%20bacon'
    data = sanitize_data(data)
    return cryptopals_2_10.aes_128_cbc_encrypt(bytes(prefix + data + suffix, 'ascii'), key, iv)


def auth(token):
     return b';admin=true;' in cryptopals_2_10.aes_128_cbc_decrypt(token, key, iv)


def discover_block_size(enc_oracle):
    init_size = len(enc_oracle(''))
    pad = 'a'
    while init_size == len(enc_oracle(pad)):
        pad += 'a'

    return len(enc_oracle(pad)) - init_size


def discover_prefix_size(enc_oracle, block_size):
    c0 = enc_oracle('a')
    c1 = enc_oracle('b')

    diff_idx = [i for i in range(len(c0)) if c0[i] != c1[i]][0]

    prefix_size = 0
    for i in range(1, block_size + 1):
        c0 = enc_oracle('a'*i + 'b')
        c1 = enc_oracle('a'*i + 'c')
        if c0[diff_idx:diff_idx + block_size] == c1[diff_idx: diff_idx + block_size]:
            prefix_size = diff_idx + (block_size - i)
    return prefix_size


def main():
    block_size = discover_block_size(retrieve_token)
    prefix_size = discover_prefix_size(retrieve_token, block_size)
    print(prefix_size)
    payload = '?admin?true?'
    payload = payload + 'a'*(block_size - len(payload))
    payload = list(retrieve_token(payload))
    payload[prefix_size - block_size] ^= ord('?') ^ ord(';')
    payload[prefix_size - block_size + len('?admin?true')] ^= ord('?') ^ ord(';')
    payload[prefix_size - block_size + len('?admin')] ^= ord('?') ^ ord('=')
    print(cryptopals_2_10.aes_128_cbc_decrypt(bytes(payload), key, iv))
    print(auth(bytes(payload)))


if __name__ == "__main__":
    main()
