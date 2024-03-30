import socket

class Client:
    def __init__(self, host, port, udp_port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((host, udp_port))
        self.host = host
        self.udp_port = udp_port
    def send_data(self, data):
        self.client_socket.send(data.encode())

    def send_data_udp(self, data):
        self.udp_socket.sendto(data.encode(),(self.host,self.udp_port))

    def receive_data(self):
        data=self.client_socket.recv(2048).decode("utf-8")
        return data

    def receive_data_udp(self,):
        data, addr =self.udp_socket.recvfrom(2048).decode("utf-8")
        return data

    def close(self):
        self.client_socket.close()

    def close_udp(self):
        self.udp_socket.close()
