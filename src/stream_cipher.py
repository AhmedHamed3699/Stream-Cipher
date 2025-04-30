import numpy as np
from LCG import LCG

class StreamCipher:
    def __init__(self, input_file, seed=42, a=7, c=0, m=127):
        lcg = LCG(seed, a, c, m)
        with open(input_file, 'r') as file:
            data = file.read()
        self.__plaintext = np.frombuffer(data, dtype=np.uint8)
        self.__keystream = np.array(lcg.n_next(len(self.plaintext)))
        self.__index = 0
    
    def run(self, n):
        plaintext = self.__plaintext[self.__index : self.__index + n]
        key = self.__keystream[self.__index : self.__index + n]
        return np.bitwise_xor(plaintext, key)
        