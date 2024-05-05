from socket import *
from threading import *

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = set()
        self.hostSocket = socket(AF_INET, SOCK_STREAM)
        self.hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)#This means that the program can reconnect at high speed to the same address and port, even if the previous connection is still open or waiting for data
        self.hostSocket.bind((self.host, self.port))
        self.hostSocket.listen()
        print("Waiting for connection...")

    def start(self):
        while True:
            clientSocket, clientAddress = self.hostSocket.accept()
            self.clients.add(clientSocket)
            print("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
            thread = Thread(target=self.clientThread, args=(clientSocket, clientAddress,))
            thread.start()

    def clientThread(self, clientSocket, clientAddress):
        while True:
            message = clientSocket.recv(1024).decode("utf-8")
            print(clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message)
            for client in self.clients:
                if client is not clientSocket:
                    client.send(
                        (clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message).encode("utf-8"))

            if not message:
                self.clients.remove(clientSocket)
                print(clientAddress[0] + ":" + str(clientAddress[1]) + " disconnected")
                break

        clientSocket.close()

if __name__ == "__main__":
    hostIp = "127.0.0.1"
    portNumber = 7500
    server = ChatServer(hostIp, portNumber)
    server.start()
