import socket
import json


class Client:
    def __init__(self, host, port, enemies_Am_port):
        self.Enemies_Am_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Enemies_Am_socket.connect((host, enemies_Am_port))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.prev_data = {'rect_center_x': 397.7510118170747, 'rect_center_y': 225.03372723582248, 'rect_width': 20, 'rect_height': 20, 'tangent_x': 398.6506070902448, 'player_position_x': 0, 'player_position_y': 0, 'player_color': [255, 0, 0], 'player_radius': 45, 'weapon_angle': -1.6007873316517744}

    def send_data(self, data_dict):
        data_str = json.dumps(data_dict)  # Convert dictionary to JSON-formatted string
        self.client_socket.send(data_str.encode("utf-8"))  # Encode string to bytes and send

    def send_to_Enemies_Am(self):
        self.Enemies_Am_socket.send("0".encode())  # Send encoded bytes

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

        '''self.client_socket.setblocking(False, timeout TODO)
        try:
            data_str = self.client_socket.recv(2048).decode("utf-8")
            self.prev_data = data_str
        except BlockingIOError:
            data_str = self.prev_data
            # No data available, return None or handle it as needed
            return data_str
        except Exception as e:
            # Handle other exceptions
            print(f"Error receiving data: {e}")
            return None

        if data_str:

            # Find the last '}' index in the original string
            last_bracket_index = data_str.rfind('}')

            # Cut the string until the last '}'
            if last_bracket_index != -1:
                data_str = data_str[:last_bracket_index + 1]

            try:
                data_dict = json.loads(data_str)
                return data_dict
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")
                return None
        else:
            # No data received, return None
            return None'''

    def receive_data_EnemiesAm(self):
        data_str = self.Enemies_Am_socket.recv(2048).decode("utf-8")  # Receive bytes, decode to string
        data_dict = json.loads(data_str)  # Parse string to dictionary
        return data_dict

    def close(self):
        self.client_socket.close()

    def close_udp(self):
        self.Enemies_Am_socket.close()
