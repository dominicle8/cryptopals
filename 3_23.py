import random
cryptopals_3_21 = __import__('3_21')


def untemper_right(y, y_diff):
    result = y
    mask = ((1 << y_diff) - 1) << (32 - y_diff)
    prev_bits = 0

    while mask > 0:
        result ^= prev_bits
        curr_bits = result & mask
        mask >>= y_diff
        prev_bits = curr_bits >> y_diff

    return result


def untemper_left(y, y_diff, c):
    result = y
    mask = (1 << y_diff) - 1
    prev_bits = 0

    while (mask & 0xffffffff) > 0:
        result ^= prev_bits & c
        curr_bits = result & mask
        mask <<= y_diff
        prev_bits = curr_bits << y_diff

    return result


def clone_mt(target_mt):
    mt = [0]*cryptopals_3_21.MT19937.N

    for i in range(cryptopals_3_21.MT19937.N):
        tap = target_mt.extract_number()
        tap = untemper_right(tap, cryptopals_3_21.MT19937.L)
        tap = untemper_left(tap, cryptopals_3_21.MT19937.T, cryptopals_3_21.MT19937.C)
        tap = untemper_left(tap, cryptopals_3_21.MT19937.S, cryptopals_3_21.MT19937.B)
        tap = untemper_right(tap, cryptopals_3_21.MT19937.U)
        mt[i] = tap

    mt_clone = cryptopals_3_21.MT19937(0)
    mt_clone.mt = mt
    return mt_clone


def main():
    seed = random.randint(0, 2**32 - 1)
    mt_orig = cryptopals_3_21.MT19937(seed)
    mt_clone = clone_mt(mt_orig)

    for i in range(100):
        print(mt_orig.extract_number())
        print(mt_clone.extract_number())


if __name__ == "__main__":
    main()
