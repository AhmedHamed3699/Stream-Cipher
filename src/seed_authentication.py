from Crypto.Hash import HMAC, SHA256

class SeedAuthentication:
    def __init__(self):
        pass
    
    def generate_hmac(self, data_bytes, hmac_key):
        h = HMAC.new(hmac_key, digestmod=SHA256)
        h.update(data_bytes)
        return h.digest()

    def verify_hmac(self, data_bytes, hmac_key, received_hmac):
        h = HMAC.new(hmac_key, digestmod=SHA256)
        h.update(data_bytes)
        try:
            h.verify(received_hmac)
            return True
        except ValueError:
            return False
