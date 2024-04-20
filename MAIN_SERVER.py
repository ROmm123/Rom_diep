import socket
import json
import threading

class main_server:
    def __init__(self, host, port):
        self.main_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_server_socket.bind((host, port))
        self.main_server_socket.listen(10000)

    def handle_client_main(self, client_socket):
        try:
            while True:
                data = client_socket.recv(2048)
                if not data:
                    break  # No more data, client has disconnected

                # Parse JSON data into a dictionary
                data_dict = json.loads(data)

                pos_x = int(data_dict["player_position_x"])
                pos_y = int(data_dict["player_position_y"])

                # Check which server the client should be on based on their position
                if pos_y < (294*64+32) and pos_x < 267*64:
                    client_socket.send("1".encode())
                elif pos_y < (294*64+32) and pos_x > 320*64:
                    client_socket.send("2".encode())
                elif pos_y > 398*64 and pos_x < 267*64:
                    client_socket.send("3".encode())
                elif pos_y > 398*64 and pos_x > 320*64:
                    client_socket.send("4".encode())

        except json.JSONDecodeError:
            client_socket.send("0".encode())  # Handle JSON decode error
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Connection closed.")
            client_socket.close()

    def main(self):
        while True:
            print("Waiting for new client...")
            client_socket, addr = self.main_server_socket.accept()
            print(f"New client connected: {addr}")
            client_thread = threading.Thread(target=self.handle_client_main, args=(client_socket,))
            client_thread.start()

if __name__ == '__main__':
    my_server = main_server('localhost', 55555)
    print("Starting server...")
    my_server.main()
