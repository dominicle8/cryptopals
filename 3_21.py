import random

class MT19937:
    W, N, M, R = 32, 624, 397, 31
    A = 0x9908B0DF
    U, D = 11, 0xFFFFFFFF
    S, B = 7, 0x9D2C5680
    T, C = 15, 0xEFC60000
    L = 18
    F = 1812433253
    index = N + 1
    lower_mask = (1 << R) - 1
    upper_mask = (not lower_mask) & ((1 << W) - 1)

    def __init__(self, seed):
        self.mt = [0] * self.N
        self.seed(seed)

    def seed(self, seed):
        self.mt[0] = seed
        self.index = self.N
        for i in range(1, self.index):
            self.mt[i] = (self.F * (self.mt[i - 1] ^ (self.mt[i - 1] >> (self.W - 2))) + i) & ((1 << self.W) - 1)

    def extract_number(self):
        if self.index >= self.N:
            if self.index > self.N:
                raise Exception
            self.twist()

        y = self.mt[self.index]
        y ^= (y >> self.U) & self.D
        y ^= (y << self.S) & self.B
        y ^= (y << self.T) & self.C
        y ^= y >> self.L
        self.index += 1

        return y & ((1 << self.W) - 1)

    def twist(self):
        for i in range(self.N):
            x = (self.mt[i] & self.upper_mask) + (self.mt[(i + 1) % self.N] & self.lower_mask)
            x_a = x >> 1
            if x % 2 != 0:
                x_a = x_a ^ self.A
            self.mt[i] = self.mt[(i + self.M) % self.N] ^ x_a
        self.index = 0


def main():
    custom_rng = MT19937(8)
    for i in range(10):
        print(custom_rng.extract_number())


if __name__ == "__main__":
    main()
