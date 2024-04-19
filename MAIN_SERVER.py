import socket
import json

class main_server():
    def __init__(self, host, port):
        self.main_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_server_socket.bind((host, port))
        self.main_server_socket.listen(10000)

    def main(self):
        while True:
            print("Waiting for new client...")
            client_socket, addr = self.main_server_socket.accept()
            print(f"New client connected: {addr}")
            try:
                print("was here")
                data = client_socket.recv(2048)
                print(data)
                print("was here")

                # Parse JSON data into a dictionary
                data_dict = json.loads(data)

                pos_x = int(data_dict["player_position_x"])
                pos_y = int(data_dict["player_position_y"])
                print("was here")

                # check which server he should be by his position
                if pos_y < 21600 and pos_x < 19200:
                    client_socket.send("1".encode())

                if pos_y < 21600 and pos_x > 19200:
                    client_socket.send("2".encode())

                if pos_y > 21600 and pos_x < 19200:
                    client_socket.send("3".encode())

                if pos_y > 21600 and pos_x > 19200:
                    client_socket.send("4".encode())

            except:
                # Handle errors and send appropriate response
                client_socket.send("0".encode())
                print(f"Error occurred with client {addr}")

            finally:
                client_socket.close()


if __name__ == '__main__':
    my_server = main_server('localhost', 33333)
    print("Starting server...")
    my_server.main()