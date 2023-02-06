import socket
import threading

# CONSTANTS
HEADER = 1024
SERVER = "localhost"
PORT = 8000
HOST = (SERVER, PORT)
FORMAT = 'utf-8'

stop_thread = False

class ClientSide():

    def __init__(self):

        # CONNECT TO THE SERVER
        self.username = input("Enter your nickname: ")

        if self.username == "admin":
            self.password = input("Enter your password: ")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect(HOST)
        except:
            print("[ERROR] Unable to connect")
            exit()

    def receive(self):
        while True:

            global stop_thread
            if stop_thread:
                break

            try:
                message = self.client.recv(HEADER).decode(FORMAT)

                if message == "NAME":
                    self.client.send(self.username.encode(FORMAT))

                    next_message = self.client.recv(HEADER).decode(FORMAT)

                    # ADMIN AUTHENTIFICATION
                    if next_message == "ADMIN":
                        self.client.send(self.password.encode(FORMAT))
                        if self.client.recv(HEADER).decode(FORMAT) == "DENY":
                            print("[ERROR] Wrong password")
                            stop_thread = True
                    
                    # TELL USER IF BANNED - CONNECTION REFUSED IF BANNED
                    elif next_message == "BAN":
                        print("[ERROR] Connection refused. You are banned from the server.")
                        self.client.close()
                        stop_thread = True
                else:
                    print(message)
            except:
                print("[ERROR] An error occured")
                self.client.close()
                break

    def write(self):
        while True:

            if stop_thread:
                break
            
            # MODEL OF A MESSAGE SENT TO THE SERVER
            message = f"{self.username}: {input('')}"

            # COMMANDS OF THE SERVER
            if message[len(self.username)+2:].startswith("/"):
                if self.username == "admin":
                    if message[len(self.username)+2:].startswith("/kick"):
                        self.client.send(f"KICK {message[len(self.username)+2+6:]}".encode(FORMAT))
                    if message[len(self.username)+2:].startswith("/ban"):
                        self.client.send(f"BAN {message[len(self.username)+2+5:]}".encode(FORMAT))
                    if message.startswith("/clearban"):
                        self.client.send("CLEAR").encode(FORMAT)
                else:
                    print("[ERROR] Commands can only be executed by an admin")
            else:
                self.client.send(message.encode(FORMAT))


Client = ClientSide()

receive_thread = threading.Thread(target=Client.receive)
receive_thread.start()

write_thread = threading.Thread(target=Client.write)
write_thread.start()