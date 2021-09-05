import socket

FORMAT = "utf-8"


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.11"
        self.port = 5051
        self.addr = (self.server, self.port)
        self.pos = self.connect()
        print(self.pos)

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str(data).encode(FORMAT))
            return self.client.recv(2048).decode(FORMAT)
        except socket.error as e:
            print(e)


# n = Network()
# print(n.send("Hello"))
# print(n.send("WORKING"))
