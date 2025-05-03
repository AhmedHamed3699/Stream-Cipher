import random

class KeyExchange:
    def __init__(self, p, a):
        self.p = p
        self.a = a
        self.private_key = None
        self.public_key = None
        self.generate_keys()
    
    def generate_keys(self) -> None:
        self.private_key = random.randint(2 , self.p -2)
        self.public_key = pow(self.a, self.private_key, self.p)
        print(f"Private key: {self.private_key}")
        print(f"Public key: {self.public_key}")

    def compute_shared_secret_key(self, othre_public_key) -> int:
        shared_key = pow(othre_public_key, self.private_key, self.p)
        print(f"Other public key: {othre_public_key}")
        print(f"Shared key: {shared_key}")
        return shared_key
    
    def compare_shared_keys(self, key1, key2) -> bool:
        return key1 == key2
