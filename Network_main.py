import socket
import json


class Client_main:
    def __init__(self, host, port):
        self.client_socket_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket_main.connect((host, port))

    def send_data(self, data_dict):
        data_str = json.dumps(data_dict)  # Convert dictionary to JSON-formatted string
        self.client_socket_main.send(data_str.encode("utf-8"))  # Encode string to bytes and send

    def receive_data(self):
        data_str = self.client_socket_main.recv(2048).decode("utf-8")

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


    def close(self):
        self.client_socket_main.close()

