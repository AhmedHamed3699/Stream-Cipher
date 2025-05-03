import random

class KeyExchange:
    def __init__(self, p, a):
        self.p = p
        self.a = a
    
    def generate_private(self) -> int:
        return random.randint(2 , self.p -2)
    
    def generate_public(self, private_key) -> int:
        return pow(self.a, private_key, self.p)

    def compute_shared_secret_key(self, othre_public_key, my_private_key) -> int:
        return pow(othre_public_key, my_private_key, self.p)
    
    def compare_shared_keys(self, key1, key2) -> bool:
        return key1 == key2
