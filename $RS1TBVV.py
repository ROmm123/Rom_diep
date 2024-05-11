import socket
import json
import threading
from Random_PosObj import Random_Position
from random_pos_npc import Random_Position_npc
from settings import setting
import queue


class main_server:
    def __init__(self, host, port, obj_port, chat_port, database_port , npc_port):
        # socket with main
        self.main_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_server_socket.bind((host, port))
        self.main_server_socket.listen(1000)

        # socket _for_ obj
        self.obj_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.obj_socket.bind((host, obj_port))
        self.obj_socket.listen(1000)

        # socket_for_chat
        self.clients_chat = set()
        self.hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostSocket.bind((host, chat_port))
        self.hostSocket.listen(1000)

        # socket_for_data_base
        self.database_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.database_socket.bind((host, database_port))
        self.database_socket.listen(1000)
        self.queue = queue.Queue()  # Queue for clients that want to join the game

        # socket_for_npc
        self.npc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.npc_socket.bind((host, npc_port))
        self.npc_socket.listen(1000)
        self.clients_npcs = []
        self.clients_lock_npcs = threading.Lock()
        self.npcs_pos = Random_Position_npc()
        self.npc_positions = self.npcs_pos.crate_position_dst_data()
        self.array_demage_npc = [0] * 100



        self.static_objects = Random_Position(600 * 64, 675 * 64)
        self.clients = []
        self.clients_lock = threading.Lock()
        self.obj_client = -1
        self.array_demage = [0] * 2000
        self.positions_data = self.static_objects.crate_position_dst_data()

    def handle_database_clients(self):
        print("join handle database")
        while True:
            client_database_socket, addr = self.database_socket.accept()
            data_from_database = client_database_socket.recv(2048).decode("utf-8")
            self.queue.put(data_from_database)

    def handle_pos_obj(self, obj_socket, i):
        while True:
            data = self.recive_from_client(obj_socket)

            if not data:
                print(f"Client {obj_socket.getpeername()} disconnected")
                with self.clients_lock:
                    self.clients.remove((obj_socket, obj_socket.getpeername()))
                    print("not in list")
                    obj_socket.close()
                    break

            data_dict = json.loads(data)
            position_collision = data_dict["position_collision"]

            if position_collision != None:

                obj_pos = {
                    "position_collision": position_collision,
                }

                if len(self.clients) > 1:
                    for receiver_socket, addr in self.clients:
                        if receiver_socket != obj_socket:
                            receiver_socket.send(json.dumps(obj_pos).encode())

    def handle_pos_npc(self, npc_socket, i):
        while True:
            data = self.recive_from_client(npc_socket)

            if not data:
                print(f"Client {npc_socket.getpeername()} disconnected")
                with self.clients_lock:
                    self.clients.remove((npc_socket, npc_socket.getpeername()))
                    print("not in list")
                    npc_socket.close()
                    break

            data_dict = json.loads(data)
            position_collision = data_dict["position_collision"]

            if position_collision != None:

                obj_pos = {
                    "position_collision": position_collision,
                }

                if len(self.clients) > 1:
                    for receiver_socket, addr in self.clients:
                        if receiver_socket != obj_socket:
                            receiver_socket.send(json.dumps(obj_pos).encode())

    def recive_from_client(self, obj_socket):
        try:
            data = obj_socket.recv(2048).decode("utf-8")
            return data
        except:
            return None

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
                if pos_y < (187 * 64) and pos_x < (250 * 64):
                    data = "1_" + str(self.obj_client)
                    client_socket.send(data.encode())
                elif pos_y < (187 * 64) and pos_x > (250 * 64) and pos_x < (30784):
                    data = "2_" + str(self.obj_client)
                    client_socket.send(data.encode())
                elif pos_y > (187 * 64) and pos_y < (22724) and pos_x < (250 * 64):
                    data = "3_" + str(self.obj_client)
                    client_socket.send(data.encode())
                elif pos_y > (187 * 64) and pos_y < (22724) and pos_x > (250 * 64) and pos_x < (30784):
                    data = "4_" + str(self.obj_client)
                    client_socket.send(data.encode())

        except json.JSONDecodeError:
            client_socket.send("0".encode())  # Handle JSON decode error
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Connection closed.")
            client_socket.close()

    def handle_obj_conection(self):
        try:
            while True:
                obj_socket, addr_obj = self.obj_socket.accept()
                # Construct the data to send to the client
                data_to_send = {
                    "crate_positions": self.positions_data
                }
                #print(data_to_send)  # Print the data to send
                # Convert the dictionary to a JSON string
                json_data = json.dumps(data_to_send)
                # Encode the JSON string to bytes
                encoded_data = json_data.encode()
                # Send the encoded data to the clientll
                obj_socket.send(encoded_data)

                with self.clients_lock:
                    self.clients.append((obj_socket, addr_obj))

                #npc_thread = threading.Thread(target=self.handle_pos_obj, args=(obj_socket, len(self.clients, )))
                #npc_thread.start()
        except:
            print("hello")

    def handle_npc_conection(self):
        try:
            while True:
                npc_socket, addr_npc = self.npc_socket.accept()
                # Construct the data to send to the client
                print(self.npc_positions)  # Print the data to send
                # Convert the dictionary to a JSON string
                json_data = json.dumps(self.npc_positions)
                # Encode the JSON string to bytes
                encoded_data = json_data.encode()
                # Send the encoded data to the clientll
                npc_socket.send(encoded_data)

                array_to_dict = self.array_to_dict(self.array_demage_npc)
                json_data = json.dumps(array_to_dict)
                # Encode the JSON string to bytes
                encoded_data = json_data.encode()
                # Send the encoded data to the clientll
                npc_socket.send(encoded_data)



                with self.clients_lock_npcs:
                    self.clients_npcs.append((npc_socket, addr_npc))

                npc_thread = threading.Thread(target=self.handle_pos_npc, args=(npc_socket, len(self.clients_npcs, )))
                npc_thread.start()
        except:
            print("hello")

    def main_for_clients(self):
        while True:
            print("Waiting for new client...")
            client_socket, addr = self.main_server_socket.accept()
            self.obj_client += 1
            print(f"New client connected: {addr}")

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=self.handle_client_main, args=(client_socket,))
            client_thread.start()

    def array_to_dict(self, array):
        dictionary = {index: value for index, value in enumerate(array)}
        return dictionary

    def start_chat(self):
        while True:
            clientSocket, clientAddress = self.hostSocket.accept()
            self.clients_chat.add(clientSocket)
            print("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
            thread = threading.Thread(target=self.clientThread_chat, args=(clientSocket, clientAddress,))
            thread.start()

    def clientThread_chat(self, clientSocket, clientAddress):
        while True:
            message = clientSocket.recv(1024).decode("utf-8")
            print(clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message)
            for client_chat in self.clients_chat:
                if client_chat is not clientSocket:
                    client_chat.send(
                        (clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message).encode("utf-8"))

            if not message:
                self.clients.remove(clientSocket)
                print(clientAddress[0] + ":" + str(clientAddress[1]) + " disconnected")
                break

        clientSocket.close()


if __name__ == '__main__':
    my_server = main_server('localhost', 55555, 55556, 55557, 64444,55558)
    print("Starting server...")
    obj_thread = threading.Thread(target=my_server.handle_obj_conection)
    npc_thread = threading.Thread(target=my_server.handle_npc_conection)
    chat_thread = threading.Thread(target=my_server.start_chat)
    database_thread = threading.Thread(target=my_server.handle_database_clients)
    obj_thread.start()
    npc_thread.start()
    chat_thread.start()
    database_thread.start()
    my_server.main_for_clients()
