import socket
import threading

# CONSTANTS
HEADER = 1024
SERVER = "localhost"
PORT = 8000
HOST = (SERVER, PORT)
FORMAT = 'utf-8'

clients = []
usernames = []


class ServerSide:

    def __init__(self):
    
        # INITIALIZE THE SERVER 
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(HOST)

    # SEND MESSAGE TO ALL THE ACTIVE USERS OF THE CHAT SERVER
    def broadcast(self, message):
        for client in clients:
            client.send(message)

    # HANDLE THE CONNECTIONS OF EACH CLIENT
    def handle(self, client):

        while True:
            try:
                msg = message = client.recv(HEADER)

                # REQUEST TO KICK A CLIENT
                if msg.decode(FORMAT).startswith("KICK"):
                    if usernames[clients.index(client)] == "admin":
                        user_to_kick = msg.decode(FORMAT)[5:]
                        self.kick(user_to_kick, "k")
                    else:
                        client.send("[WARNING] Command was refused. You are not an admin!".encode(FORMAT))

                # REQUEST TO BAN A CLIENT
                elif msg.decode(FORMAT).startswith("BAN"):
                    if usernames[clients.index(client)] == "admin":
                        user_to_ban = msg.decode(FORMAT)[4:]
                        self.kick(user_to_ban, "b")

                        with open("bans.txt", "a") as f:
                            f.write(f"{user_to_ban}\n")

                        print(f"{user_to_ban} was banned")
                    else:
                        client.send("[WARNING] Command was refused. You are not an admin!".encode(FORMAT))

                # REQUEST TO CLEAR ALL THE BANS
                elif msg.decode(FORMAT).startswith("CLEAR"):
                    if usernames[clients.index(client)] == "admin":
                        f = open("bans.txt","w")
                        f.close()
                    else:
                        client.send("[WARNING] Command was refused. You are not an admin!".encode(FORMAT))
                    
                else:
                    self.broadcast(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                username = usernames[index]
                self.broadcast(f"{username} left he chat".encode(FORMAT))
                usernames.remove(username)
                break

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
        while True:
            client, addr = self.server.accept()
            print(f"[CONNECTED] {addr}")
            
            # CREATE AN USERNAME FOR THE CLIENT
            client.send("NAME".encode(FORMAT))
            username = client.recv(HEADER).decode(FORMAT)

            # READ THE BANS TEXT FILE TO CHECK IF USERNAME IS BANNED
            check_ban = False
            with open("bans.txt", "r") as f:
                for line in f:
                    if username in line:
                        check_ban = True

            if check_ban:
                client.send("BAN".encode(FORMAT))
                client.close()
                continue
            
            # REQUEST PASSWORD IF ADMIN
            if username == "admin":
                client.send("ADMIN".encode(FORMAT))
                password = client.recv(HEADER).decode(FORMAT)

                if password != "admin":
                    client.send("DENY".encode(FORMAT))
                    client.close()
                    continue

            usernames.append(username)
            clients.append(client)

            # CLIENT JOIN THE SERVER
            print(f"Nickname of the client is {username}")
            self.broadcast(f"{username} joined the chat".encode(FORMAT))
            client.send("Connected to the server".encode(FORMAT))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()   

    # METHOD TO KICK USER FROM CHAT SERVER
    def kick(self, user, choice):
        if user in usernames:
            user_index = usernames.index(user)
            client_to_kick = clients[user_index]
            clients.remove(client_to_kick)
            client_to_kick.send("You were kicked from the server".encode(FORMAT))
            client_to_kick.close()
            usernames.remove(user)

            # DISPLAY IF USER WAS KICKED OR BANNED
            if choice == "k":
                self.broadcast(f"{user} was kicked".encode(FORMAT))
            elif choice == "b":
                self.broadcast(f"{user} was banned".encode(FORMAT))

print("[STARTING] Server is running..")
Server = ServerSide()
Server.start()
