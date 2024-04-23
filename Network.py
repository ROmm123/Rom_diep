import socket
import json

class Client:
    def __init__(self, host, port, enemies_Am_port=None):
        self.host = host
        self.port = port
        self.enemies_Am_port = enemies_Am_port


    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            if self.enemies_Am_port is not None:
                self.enemies_Am_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
        except ConnectionRefusedError:
            print("Connection refused.")
            # Handle the error as needed


    def send_data(self, data_dict):
        try:
            data_str = json.dumps(data_dict)
            self.client_socket.send(data_str.encode("utf-8"))
        except Exception as e:
            print(f"Error sending data: {e}")

    def send_to_enemies_Am(self):
        try:
            self.enemies_Am_socket.send("0".encode())
        except Exception as e:
            print(f"Error sending to enemy: {e}")

    def receive_data(self):
        try:
            data_str = self.client_socket.recv(2048).decode("utf-8")
            last_bracket_index = data_str.rfind('}')
            if last_bracket_index != -1:
                data_str = data_str[:last_bracket_index + 1]
            data_dict = json.loads(data_str)
            return data_dict
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

    def receive_data_EnemiesAm(self):
        try:
            data_str = self.enemies_Am_socket.recv(2048).decode("utf-8")
            data_dict = json.loads(data_str)
            return data_dict
        except Exception as e:
            print(f"Error receiving data from enemy: {e}")
            return None

    def close(self):
        try:
            self.client_socket.close()
        except Exception as e:
            print(f"Error closing client socket: {e}")

    def close_enemies_Am(self):
        try:
            self.enemies_Am_socket.close()
        except Exception as e:
            print(f"Error closing enemy socket: {e}")