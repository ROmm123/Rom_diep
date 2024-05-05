import socket
import json
import errno

class Client_chat:
    def __init__(self, host_chat, port_chat):
        self.host = host_chat
        self.port = port_chat
        self.socket_chat = None  # Initialize client socket

    def connect(self):
        try:
            # Connect to the main server
            self.socket_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_chat.connect((self.host, self.port))

        except ConnectionRefusedError:
            print("Connection refused.")
            # Handle the error as needed

    def send_data(self, clientMessage):
        try:
            self.socket_chat.send(clientMessage.encode("utf-8"))
        except Exception as e:
            print(f"Error sending data: {e}")

    def recevie_data(self):
        clientsMessages = self.socket_chat.recv(2048).decode("utf-8")
        return clientsMessages

    def close(self):
        try:
            self.socket_chat.close()

        except Exception as e:
            print(f"Error closing sockets: {e}")
