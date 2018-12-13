import random
import time
cryptopals_3_21 = __import__('3_21')


def main():
    time.sleep(random.randint(4, 10))
    rand_seed = int(time.time())
    print(rand_seed)
    target_mt = cryptopals_3_21.MT19937(rand_seed)

    time.sleep(random.randint(4, 10))
    curr_time = int(time.time())
    start_time = curr_time - 100
    expected_value = target_mt.extract_number()
    for seed in range(start_time, curr_time):
        guess_mt = cryptopals_3_21.MT19937(seed)
        if guess_mt.extract_number() == expected_value:
            print(seed)


if __name__ == "__main__":
    main()
