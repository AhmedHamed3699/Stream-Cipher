import json
import sys
from communication import Sender, Receiver

BATCH_SIZE = 10

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py sender|receiver")
        sys.exit(1)

    comm_type = sys.argv[1].lower()
    if comm_type not in ['sender', 'receiver']:
        print("Invalid argument. Use 'sender' or 'receiver'.")
        sys.exit(1)

    config = {}
    plaintext = None
    with open('../data/config.json', 'r') as file:
        config = json.load(file)
    with open('../data/input.txt', 'r') as file:
        plaintext = file.read()

    if comm_type == 'sender':
        sender = Sender(config, plaintext)
        sender.start()
    else:
        receiver = Receiver(config)
        receiver.start()
    

if __name__ == '__main__':
    main()
