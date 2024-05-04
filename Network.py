import socket
import json
import ast
import time


class Client:
    def __init__(self, host, port, enemies_or_obj_Am_port=None):
        self.host = host
        self.port = port
        self.enemies_or_obj_Am_port = enemies_or_obj_Am_port
        self.client_socket = None  # Initialize client socket
        self.another_socket_for_enemies_or_obj = None  # Initialize enemies' socket

    def connect(self):
        try:
            # Connect to the main server
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))

            # If enemies_Am_port is provided, connect to the enemies' server
            if self.enemies_or_obj_Am_port is not None:
                self.another_socket_for_enemies_or_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.another_socket_for_enemies_or_obj.connect((self.host, self.enemies_or_obj_Am_port))

        except ConnectionRefusedError:
            print("Connection refused.")
            # Handle the error as needed



    def send_data(self, data_dict):
        try:
            data_str = json.dumps(data_dict)
            self.client_socket.send(data_str.encode("utf-8"))
        except Exception as e:
            print(f"Error sending data: {e}")

    def send_data_obj_parmetrs(self, data_dict):
        try:
            data_str = json.dumps(data_dict)
            self.another_socket_for_enemies_or_obj.send(data_str.encode("utf-8"))
        except Exception as e:
            print(f"Error sending data: {e}")

    def send_to_Enemies_Am(self):
        try:
            self.another_socket_for_enemies_or_obj.send("0".encode())
        except Exception as e:
            print(f"Error sending to enemy: {e}")

    def receive_obj_prameters(self):
        data_str = self.another_socket_for_enemies_or_obj.recv(2048).decode("utf-8")
        print(data_str)
        last_bracket_index = data_str.rfind('}')
        if last_bracket_index != -1:
            data_str = data_str[:last_bracket_index + 1]
        data_dict = json.loads(data_str)
        return data_dict


    def receive_list_obj_once(self):
        try:
            chunk = self.another_socket_for_enemies_or_obj.recv(2**20)  # Receive a chunk of data
            data_str = chunk.decode("utf-8")  # Decode the byte string to UTF-8 string
            last_bracket_index = data_str.rfind('}')
            if last_bracket_index != -1:
                data_str = data_str[:last_bracket_index + 1]
            data_dict = json.loads(data_str)  # Parse the JSON string into a dictionary
            return data_dict
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

    def receive_data_EnemiesAm(self):
        data_str = self.another_socket_for_enemies_or_obj.recv(2048).decode("utf-8")
        data_dict = json.loads(data_str)
        return data_dict

    def recevie_only_data_from_main(self):
        data_str = self.client_socket.recv(2048).decode("utf-8")
        return data_str

    import json

    def receive_data(self):
        while True:
            data_str = self.client_socket.recv(2048).decode("utf-8")
            print ("data str , in network : "+data_str)
            if data_str[0] == '[':
                index = data_str.find(']')
                index1 = index
                while str(data_str[index1-1]).isdigit(): # }]
                #if isinstance(int(data_str[index - 1]), int):
                    index1 = data_str[index1 + 2:].find(']')
                    index1 += index1
                # Remove the truncated part
                data_str = data_str[:index1 + 3]
                print("data str , after modification : " + str(data_str))

                # Split the concatenated JSON string into individual JSON objects
                json_list = []
                start = 1
                while start < len(data_str) - 2:
                    end = data_str.find('}', start)
                    json_list.append(data_str[start:end + 1])
                    start = end

                # Parse each JSON object and add it to the list
                data_list = []
                for json_str in json_list:
                    data_list.append(json.loads(json_str))

                # Print the resulting list
                print(data_list)


                return data_list



    def receive_data_ID(self): # '{} , {} , {} '
        data = self.client_socket.recv(2048).decode("utf-8")
        return int(data)

    def send_enemies_state(self , list_as_string):
        self.client_socket.send(list_as_string.encode("utf-8"))

    def close(self):
        try:
            self.client_socket.close()

        except Exception as e:
            print(f"Error closing sockets: {e}")

    def close_enemies_Am(self):
        try:
            self.another_socket_for_enemies_or_obj.close()
        except Exception as e:
            print(f"Error closing enemy socket: {e}")