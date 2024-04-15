import socket
import json


class Client:
    def __init__(self, host, port, enemies_Am_port):
        self.Enemies_Am_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Enemies_Am_socket.connect((host, enemies_Am_port))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def send_data(self, data_dict):
        data_str = json.dumps(data_dict)  # Convert dictionary to JSON-formatted string
        self.client_socket.send(data_str.encode("utf-8"))  # Encode string to bytes and send

    def send_to_Enemies_Am(self):
        self.Enemies_Am_socket.send("0".encode())  # Send encoded bytes

    def receive_data(self):
        data_str = self.client_socket.recv(2048).decode("utf-8")

        # מצא את האינדקס האחרון של '}' במחרוזת המקורית
        last_bracket_index = data_str.rfind('}')

        # חתוך את המחרוזת עד לתו '}' האחרון
        if last_bracket_index != -1:
            data_str = data_str[:last_bracket_index + 1]

        try:
            data_dict = json.loads(data_str)  # פענח את המחרוזת למילון
            return data_dict
        except json.JSONDecodeError as e:
            return None

    def receive_data_EnemiesAm(self):
        data_str = self.Enemies_Am_socket.recv(2048).decode("utf-8")  # Receive bytes, decode to string
        data_dict = json.loads(data_str)  # Parse string to dictionary
        return data_dict

    def close(self):
        self.client_socket.close()

    def close_udp(self):
        self.Enemies_Am_socket.close()
