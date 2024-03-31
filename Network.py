import socket

class Client:
    def __init__(self, host, port, enemies_Am_port):
        self.Enemies_Am_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Enemies_Am_socket.connect((host, enemies_Am_port))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
    def send_data(self, data):
        self.client_socket.send(data.encode())

    def send_to_Enemies_Am(self):
        self.Enemies_Am_socket.send("0".encode())


    def receive_data(self):
        data=self.client_socket.recv(2048).decode("utf-8")
        return data

    def receive_data_EnemiesAm(self,):
        data =self.Enemies_Am_socket.recv(2048).decode("utf-8")
        return data

    def close(self):
        self.client_socket.close()

    def close_udp(self):
        self.Enemies_Am_socket.close()


