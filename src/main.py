import sys
from communication import Communication

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py sender|receiver")
        sys.exit(1)
    
    comm_type = sys.argv[1].lower()
    if comm_type not in ['sender', 'receiver']:
        print("Invalid argument. Use 'sender' or 'receiver'.")
        sys.exit(1)
    
    comm = Communication(comm_type)
    print(f"{comm_type.capitalize()} started.")
    while True:
        message = input(f"{comm_type.capitalize()} message: ")
        comm.send(message)
        data = comm.receive()
        print(f"{comm_type} received: {data}")

if __name__ == '__main__':
    main()