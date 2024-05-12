import socket
import json
import threading
from Random_PosObj import Random_Position
from settings import setting


class main_server:
    def __init__(self, host, port, obj_port):
        self.main_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.main_server_socket.bind((host, port))

        self.obj_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.obj_socket.bind((host, obj_port))

        self.static_objects = Random_Position(600 * 64, 675 * 64)
        self.clients = []
        self.clients_lock = threading.Lock()
        self.obj_client = -1


    def provide_ID(self ,addr):
        self.main_server_socket.sendto((str(self.obj_client)).encode("utf-8") , addr)


    def handle_pos_obj(self):

        while True:
            try:
                data, addr_obj = self.obj_socket.recvfrom(2048)
                if data:
                    data = data.decode()
                    data_dict = json.loads(data)
            except:
                print(f"Client {addr_obj} disconnected")
                with self.clients_lock:
                    self.clients.remove(addr_obj)
                break
            position_collision = data_dict["position_collision"]
            obj_pos = {
                "position_collision": position_collision
            }
            if len(self.clients) > 1:
                for addr in self.clients:
                    if addr != addr_obj:
                        print(json.dumps(obj_pos).encode())
                        self.obj_socket.sendto(json.dumps(obj_pos).encode() , addr)

    def handle_client_main(self, client_socket):
        try:
            while True:
                data , addr = self.main_server_socket.recvfrom(2048)
                if not data:
                    break  # No more data, client has disconnected

                # Parse JSON data into a dictionary
                data_dict = json.loads(data)

                pos_x = int(data_dict["player_position_x"])
                pos_y = int(data_dict["player_position_y"])

                # Check which server the client should be on based on their position
                if pos_y < (187*64) and pos_x < (250*64):
                    data = "1_" + str(self.obj_client)
                    client_socket.sendto(data.encode() , addr)
                elif pos_y < (187*64) and pos_x > (250 * 64) and pos_x<(30784):
                    data = "2_" + str(self.obj_client)
                    client_socket.sendto(data.encode() , addr)
                elif pos_y > (187*64)and pos_y<(22724) and pos_x < (250*64):
                    data = "3_" + str(self.obj_client)
                    client_socket.sendto(data.encode() , addr)
                elif pos_y > (187*64)and pos_y<(22724) and pos_x > (250 * 64) and pos_x<(30784):
                    data = "4_" + str(self.obj_client)
                    client_socket.sendto(data.encode() , addr)

        except json.JSONDecodeError:
            client_socket.sendto("0".encode() , addr)  # Handle JSON decode error
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Connection closed.")

    def handle_obj_conection(self):
        try:
            while True:
                data_obj, addr_obj = self.obj_socket.recvfrom(2048)
                # Retrieve the crate position destination data
                positions_data = self.static_objects.crate_position_dst_data()
                # Construct the data to send to the client
                data_to_send = {
                    "crate_positions": positions_data
                }
                print(data_to_send)  # Print the data to send

                # Convert the dictionary to a JSON string
                json_data = json.dumps(data_to_send)
                # Encode the JSON string to bytes
                encoded_data = json_data.encode()

                # Send the encoded data to the clientll
                self.obj_socket.sendto(encoded_data , addr_obj)

                with self.clients_lock:
                    self.clients.append(addr_obj)
                obj_thread = threading.Thread(target=self.handle_pos_obj)
                obj_thread.start()
        except:
            print("hello")

    def main_for_clients(self):
        while True:
            print("Waiting for new client...")
            #client_socket, addr = self.main_server_socket.accept()
            data , addr = self.main_server_socket.recvfrom(2048)
            self.obj_client += 1
            self.provide_ID(addr)
            print(f"New client connected: {addr}")

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=self.handle_client_main)
            client_thread.start()



if __name__ == '__main__':
    my_server = main_server('localhost', 55557, 55558)
    print("Starting server...")
    obj_thread = threading.Thread(target=my_server.handle_obj_conection)
    obj_thread.start()
    my_server.main_for_clients()
