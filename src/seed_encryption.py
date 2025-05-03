from Crypto.Cipher import AES

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
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted = cipher.encrypt(self.pad(seed_bytes))
        return encrypted

    def decrypt_seed(self, encrypted_data, key):
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted_data)
        return self.unpad(decrypted)