import socket
import json
import errno
import ast

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

    def send_database_data(self, data_dict):
        try:
            print(data_dict)
            data_str = json.dumps(data_dict)
            self.socket_chat.send(data_str.encode("utf-8"))
            print("data sent")
        except Exception as e:
            print(f"Error sending data: {e}")
            


    def recevie_data(self):
        clientsMessages = self.socket_chat.recv(2048).decode("utf-8")
        return clientsMessages

    def receive_database_data(self):
        while True:
            print("before receive in receive_database_data")
            data = self.socket_chat.recv(2048).decode("utf-8")
            print(data)
            if not data:
                break
            if "sign" in data:
                return None

            string_tuple = data.strip('()')

            # Split string by commas and remove empty elements
            tuple_elements = [elem.strip() for elem in string_tuple.split(',') if elem.strip()]

            # Convert elements to appropriate data types
            actual_tuple = []
            for elem in tuple_elements:
                if elem == "None":
                    actual_tuple.append(None)
                else:
                    try:
                        actual_tuple.append(ast.literal_eval(elem))
                    except (SyntaxError, ValueError):
                        # Handle invalid literals here
                        actual_tuple.append(None)

            return tuple(actual_tuple)

    def close(self):
        try:
            self.socket_chat.close()

        except Exception as e:
            print(f"Error closing sockets: {e}")