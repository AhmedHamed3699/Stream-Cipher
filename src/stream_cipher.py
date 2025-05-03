import numpy as np
from LCG import LCG

class StreamCipher:
    def __init__(self, a=7, c=0, m=127):
        self.a = a
        self.c = c
        self.m = m
        self.seed = None
    
    def create_lcg(self, seed):
        self.lcg = LCG(seed, self.a, self.c, self.m)

    def run(self, message):
        key = np.array(self.lcg.n_next(len(message)))
        return np.bitwise_xor(message, key)
        