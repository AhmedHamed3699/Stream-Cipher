from Crypto.Cipher import AES

KEY_SIZE = 16

class SeedEncryption:
    def __init__(self):
        pass

    def pad(self, data):
        padding_len = KEY_SIZE - (len(data) % KEY_SIZE)
        return data + bytes([padding_len]) * padding_len

    def unpad(self, data):
        padding_len = data[-1]
        return data[:-padding_len]
    
    def encrypt(self, seed_bytes, key):
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted = cipher.encrypt(self.pad(seed_bytes))
        return encrypted

    def decrypt(self, encrypted_data, key):
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted_data)
        return self.unpad(decrypted)