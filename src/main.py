from LCG import LCG
from key_exchange import KeyExchange
from stream_cipher import StreamCipher

def main():
    cipher = StreamCipher('./../data/input.txt')
    print(cipher.run(2))
    ke = KeyExchange(7,3)
    a_private = ke.generate_private()
    a_public = ke.generate_public(a_private)
    b_private = ke.generate_private()
    b_public = ke.generate_public(b_private)
    a_shared = ke.compute_shared_secret_key(b_public,a_public)
    b_shared = ke.compute_shared_secret_key(a_public, b_private)
    print(ke.compare_shared_keys(a_shared, b_shared))
if __name__ == '__main__':
    main()