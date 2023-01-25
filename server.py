import socket 
import threading

# CONSTANTS
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
HOST = (SERVER, PORT)
FORMAT = 'utf-8'

clients = []
nicknames = []

class ServerSide:

    def __init__(self):
        # SERVER PREPARATION AND BINDING TO THE RIGHT HOST
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(HOST)

    def broadcast(self, message):
        for client in clients:
            client.send(message)

    # HANDLE THE CONNECTIONS OF THE CLIENTS
    def handle(self, client):

        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                self.broadcast(f"{nickname} left he chat".encode(FORMAT))
                nicknames.remove(nickname)
                break

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            client, addr = self.server.accept()
            print(f"[CONNECTED] {addr}")

            client.send("NICK".encode(FORMAT))
            nickname = client.recv(1024).decode(FORMAT)
            nicknames.append(nickname)
            clients.append(client)

            print(f"Nickname of the client is {nickname}")
            self.broadcast(f"{nickname} joined the chat".encode(FORMAT))
            client.send("Connected to the server".encode(FORMAT))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
            print(f"Active usersnames: {nicknames}")


print("[STARTING] Server is running..")
Server = ServerSide()
Server.start()