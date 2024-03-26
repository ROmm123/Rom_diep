import socket

class Client:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
    def send_data(self, data):
        self.client_socket.send(data.encode())

    def receive_data(self):
        data=self.client_socket.recv(2048).decode("utf-8")
        self.client_socket.setblocking(1)
        return data
    def close(self):
        self.client_socket.close()
