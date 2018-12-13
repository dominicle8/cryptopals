import os
cryptopals_2_10 = __import__('2_10')


def profile_parser(profile):
    parameters = profile.split('&')
    return {k: v for k, v in [tuple(param.split('=')) for param in parameters]}


def profile_for(email):
    sanitized_email = email.replace('=', '').replace('&', '')
    user_obj = {
        'email': sanitized_email,
        'uid': '10',
        'role': 'user'
    }

    return '&'.join([k + '=' + v for k, v in user_obj.items()])


def main():
    key = os.urandom(16)
    profile_payload = profile_for('a'*10 + 'admin' + 'a'*11).encode('ascii')
    encrypted_profile = cryptopals_2_10.aes_128_ecb_encrypt(profile_payload, key)
    prefix_payload = profile_for('a'*13).encode('ascii')
    prefix = cryptopals_2_10.aes_128_ecb_encrypt(prefix_payload, key)

    payload = prefix[:32] + encrypted_profile[16:32]

    profile = profile_parser(cryptopals_2_10.aes_128_ecb_decrypt(payload, key).decode('ascii'))
    print(profile['role'])


if __name__ == "__main__":
    main()