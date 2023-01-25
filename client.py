import socket
import threading

# CONSTANTS
HEADER = 64
SERVER = "127.0.0.1"
PORT = 5050
HOST = (SERVER, PORT)
FORMAT = 'utf-8'

class ClientSide():

    def __init__(self):
        self.nickname = input("Choose a nickname: ")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect(HOST)
        except:
            print("[ERROR] Unable to connect")
            exit()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode(FORMAT)
                if message == "NICK":
                    self.client.send(self.nickname.encode(FORMAT))
                else:
                    print(message)
            except:
                print("[ERROR] An error occured")
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.send(message.encode(FORMAT))


Client = ClientSide()

receive_thread = threading.Thread(target=Client.receive)
receive_thread.start()

write_thread = threading.Thread(target=Client.write)
write_thread.start()

# ADD AUTHENTIFICATION LOGINS
# ADD DATABASE TO KEEP THE LOGS OF MESSAGES AND INFOS