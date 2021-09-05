import socket
import threading

HEADER = 2048  # size of data
FORMAT = "utf-8"
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5051
ADDRESS = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    server.bind(ADDRESS)
except socket.error as e:
    str(e)


def readPosition(position):  # create a tuple
    # print(position)
    position = position.split(",")
    return int(position[0]), int(position[1])


def makePosition(tuple):  # creates a string
    # print(tuple)
    return str(tuple[0]) + "," + str(tuple[1])


# global variable
pos = [(0, 0), (100, 100)]  # current/starting positions


def handle_client(conn, addr, player):
    print(f"[NEW CONNECTION] {addr} connected")
    # conn.send("Server: You are connected".encode(FORMAT))
    # print("this", makePosition(pos[player]).encode(FORMAT))
    conn.send(makePosition(pos[player]).encode(
        FORMAT))  # first connection, sends the starting postiion

    connected = True
    while connected:
        try:
            #
            data = conn.recv(HEADER).decode(FORMAT)  # returns a string
            data = readPosition(data)  # returns a tuple

            # stores the current position in the global variable
            pos[player] = data

            reply = ""
            if not data:
                print("DISCONNECTED!")
                connected = False
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                # conn.send(("Server received: " + str(data)).encode(FORMAT))
                print("RECEIVED")

            reply = makePosition(reply)
            conn.send(reply.encode(FORMAT))
        except:
            print("Handle client error")
            connected = False
    print("LOST CONNECTION!")
    conn.close()


def start():
    server.listen(2)
    print(f"[LISTENING] server is listening on {SERVER}")

    currentPlayer = 0
    while True:
        conn, addr = server.accept()  # blocking code stops current thread until it's finished
        print(f"[CONNECTION] connected to {addr}")

        thread = threading.Thread(
            target=handle_client, args=(conn, addr, currentPlayer))
        thread.start()
        currentPlayer += 1


start()
