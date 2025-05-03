import socket
import random
import numpy as np
from key_exchange import KeyExchange
from stream_cipher import StreamCipher
from seed_encryption import SeedEncryption
from seed_authentication import SeedAuthentication

BATCH_SIZE = 10


class Communication:
    def __init__(self, port, peer_port):
        self.port = port
        self.peer_port = peer_port
        self.socket_gate = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_gate.bind(('0.0.0.0', self.port))

    def send(self, message):
        self.socket_gate.sendto(
            message, ("127.0.0.1", self.peer_port))

    def receive(self, buffer_size=1024):
        data, _ = self.socket_gate.recvfrom(buffer_size)
        return data

    def exit(self):
        self.socket_gate.close()


class Sender(Communication):
    def __init__(self, config, plaintext):
        super().__init__(5000, 5001)
        self.plaintext = np.array([ord(char) for char in plaintext])
        self.key_exchange = KeyExchange(
            config['key_p'], config['key_a'])
        self.seed_encryption = SeedEncryption()
        self.seed_authentication = SeedAuthentication()
        self.stream_cipher = StreamCipher(
            config['lcg_a'], config['lcg_c'], config['lcg_m'])
        print("Sender Started!")

    def start(self):
        self.send(self.key_exchange.public_key.to_bytes(16, 'big'))
        peer_public_key = self.receive()
        seed_key = self.key_exchange.compute_shared_secret_key(
            int.from_bytes(peer_public_key, 'big')).to_bytes(16, 'big')
        seed = random.randint(0, 2**16 - 1)
        seed_bytes = seed.to_bytes(16, 'big')
        encrypted_seed = self.seed_encryption.encrypt(seed_bytes, seed_key)
        hmac = self.seed_authentication.generate_hmac(encrypted_seed, seed_key)
        self.send(encrypted_seed)
        self.send(hmac)

        self.stream_cipher.create_lcg(seed)

        for i in range(0, len(self.plaintext), BATCH_SIZE):
            if i + BATCH_SIZE > len(self.plaintext):
                stream = self.plaintext[i:]
            else:
                stream = self.plaintext[i: i + BATCH_SIZE]
            print(f"Stream before encryption: {stream}")
            encrypted_stream = self.stream_cipher.run(stream)
            self.send(encrypted_stream.tobytes())
            print(f"Sent encrypted stream: {encrypted_stream}")

        self.send(b'EOF')
        print("Sender finished!")


class Receiver(Communication):
    def __init__(self, config):
        super().__init__(5001, 5000)
        self.key_exchange = KeyExchange(
            config['key_p'], config['key_a'])
        self.seed_encryption = SeedEncryption()
        self.seed_authentication = SeedAuthentication()
        self.stream_cipher = StreamCipher(
            config['lcg_a'], config['lcg_c'], config['lcg_m'])
        print("Receiver Started!")

    def start(self):
        peer_public_key = self.receive()
        self.send(self.key_exchange.public_key.to_bytes(16, 'big'))
        seed_key = self.key_exchange.compute_shared_secret_key(
            int.from_bytes(peer_public_key, 'big')).to_bytes(16, 'big')

        encrypted_seed = self.receive()
        hmac = self.receive()

        if not self.seed_authentication.verify_hmac(encrypted_seed, seed_key, hmac):
            print("Authentication failed!")
            return

        seed = int.from_bytes(self.seed_encryption.decrypt(
            encrypted_seed, seed_key), 'big')
        self.stream_cipher.create_lcg(seed)

        output = []
        flag = True
        while True:
            encrypted_stream = self.receive()
            if encrypted_stream == b'EOF':
                break
            encrypted_stream = np.frombuffer(
                encrypted_stream, dtype=np.uint32)[0::2]
            decrypted_stream = self.stream_cipher.run(encrypted_stream)
            output.append(decrypted_stream)
            print(f"Received encrypted stream: {encrypted_stream}")
            print(f"Decrypted stream: {decrypted_stream}")

        output = np.concatenate(output)
        output = np.array([chr(asc) for asc in output])
        output = ''.join(output)
        with open('../data/output.txt', 'w') as file:
            file.write(output)
        print("Receiver finished!")
