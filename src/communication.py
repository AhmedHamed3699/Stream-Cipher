import socket

class Communication:
    def __init__(self, type):
        self.port = 5000
        self.peer_port = 5001
        if type == "receiver":
            self.port = 5001
            self.peer_port = 5000
        self.socket_gate = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_gate.bind(('0.0.0.0', self.port))

    def send(self, message):
        self.socket_gate.sendto(message.encode(), ("127.0.0.1", self.peer_port))

    def receive(self):
        data, _ = self.socket_gate.recvfrom(1024)
        return data.decode()
    
    def exit(self):
        self.socket_gate.close()
