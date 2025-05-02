from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class SeedEncryption:
    def __init__(self):
        pass

    def pad(data):
        padding_len = 16 - (len(data) % 16)
        return data + bytes([padding_len]) * padding_len

    def unpad(data):
        padding_len = data[-1]
        return data[:-padding_len]
    
    def encrypt_seed(self, seed_bytes, key):
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(self.pad(seed_bytes))
        return iv + encrypted

    def decrypt_seed(self, encrypted_data, key):
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        return self.unpad(decrypted)

