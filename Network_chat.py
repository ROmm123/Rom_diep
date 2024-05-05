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
        remaining_data = b''
        while True:
            data = self.socket_chat.recv(2048)
            if not data:
                break
            remaining_data += data

            while remaining_data:
                start_index = remaining_data.find(b'{')
                if start_index == -1:
                    # Check if the remaining data is just "-1"
                    if remaining_data.strip() == b'-1':
                        remaining_data = b''
                        return -1
                    break

                end_index = remaining_data.find(b'}', start_index)
                if end_index == -1:
                    break

                end_index += 1  # Include the closing brace
                json_str = remaining_data[start_index:end_index].decode("utf-8")
                data_dict = json.loads(json_str)
                remaining_data = remaining_data[end_index:]
                return data_dict

        return None

    def close(self):
        try:
            self.socket_chat.close()

        except Exception as e:
            print(f"Error closing sockets: {e}")
