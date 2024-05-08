import socket
import json
import threading
import time

from Random_PosObj import Random_Position
from connection_with_database import *
from settings import setting
import queue


class main_server:
    def __init__(self, host, port, obj_port, chat_port, database_port):
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
        self.queue_for_Sign_req = queue.Queue()  # Queue for clients that want to join the game
        self.queue_for_login_req = queue.Queue()  # Queue for clients that want to join the game
        self.queue_for_logout_req = queue.Queue()  # Queue for clients that want to leave the game

        self.static_objects = Random_Position(600 * 64, 675 * 64)
        self.clients = []
        self.clients_lock = threading.Lock()
        self.obj_client = -1
        self.array_demage = [0] * 2000
        self.positions_data = self.static_objects.crate_position_dst_data()

    def handle_database_clients(self):
        # MAKE IT A DIFFERENT THREAD , MULTITHREADING
        #("join handle database")
        while True:
            client_database_socket, addr = self.database_socket.accept()
            threading.Thread(target=self.insert_to_queue_database , args=(client_database_socket,)).start()
            print("started thread")



    def insert_to_queue_database(self , client_database_socket):
        print("in thread in main class, socket is : "+str(client_database_socket))
        Quary = ("login", "signin" , "logout")
        running = True
        while running:
            data_from_database = client_database_socket.recv(2048).decode("utf-8")
            if Quary[1] in data_from_database:
                self.queue_for_Sign_req.put(
                    (data_from_database, client_database_socket))  # Queue for clients that want to join the game
            elif Quary[0] in data_from_database:
                self.queue_for_login_req.put(
                    (data_from_database, client_database_socket))  # Queue for clients that want to join the game
            elif Quary[2] in data_from_database:
                print("log out packet , adding to flipin queue init")
                self.queue_for_logout_req.put(
                    (data_from_database, client_database_socket))
                running = False

    def handle_queue_database(self):
        while True:
            if not self.queue_for_Sign_req.empty():
                raw_signin_packet, client_database_socket = self.queue_for_Sign_req.get()
                raw_signin_packet = json.loads(raw_signin_packet)
                handle_data_for_signin(raw_signin_packet["username"], raw_signin_packet["password"])
            if not self.queue_for_login_req.empty():
                raw_signin_packet, client_database_socket = self.queue_for_login_req.get()
                raw_signin_packet = json.loads(raw_signin_packet)
                info = handle_data_forLogin(raw_signin_packet["username"], raw_signin_packet["password"])
                #("info : " + str(info))
                if info:
                    string_tuple = "(" + ", ".join(str(item) if item is not None else "None" for item in info) + ")"
                    print("STRING TUPLE : "+str(string_tuple))
                    print("TYPE : "+str(type(string_tuple)))
                    client_database_socket.send(string_tuple.encode("utf-8"))
                    #("data sent")
                else:
                    client_database_socket.send("sign again".encode("utf-8"))

            if not self.queue_for_logout_req.empty():
                signout_packet = self.queue_for_logout_req.get()
                print("logged out packet: "+str(signout_packet))
                loadedPacket = json.loads(signout_packet[0])
                print("USERNAME IN LOADEDPACKET = "+str(loadedPacket["username"]))
                print("TYPE USERNAME = "+str(type(loadedPacket["username"])))
                handle_data_for_logout(loadedPacket["x"], loadedPacket["y"], loadedPacket["speed_c"],
                                       loadedPacket["size_c"],
                                       loadedPacket["shield_c"], loadedPacket["hp_c_60"], loadedPacket["hp_c_30"],
                                       loadedPacket["hp_c_15"], loadedPacket["hp_c_5"], loadedPacket["username"],
                                       loadedPacket["password"])
    def handle_pos_obj(self, obj_socket, i):
        while True:
            data = self.recive_from_client(obj_socket)

            if not data:
                #(f"Client {obj_socket.getpeername()} disconnected")
                with self.clients_lock:
                    self.clients.remove((obj_socket, obj_socket.getpeername()))
                    #("not in list")
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
        #except Exception as e:
            #(f"An error occurred: {e}")
        finally:
            #("Connection closed.")
            client_socket.close()

    def handle_obj_conection(self):
        try:
            while True:
                obj_socket, addr_obj = self.obj_socket.accept()
                # Construct the data to send to the client
                data_to_send = {
                    "crate_positions": self.positions_data
                }
                #(data_to_send)  # # the data to send
                # Convert the dictionary to a JSON string
                json_data = json.dumps(data_to_send)
                # Encode the JSON string to bytes
                encoded_data = json_data.encode()
                # Send the encoded data to the clientll
                obj_socket.send(encoded_data)

                with self.clients_lock:
                    self.clients.append((obj_socket, addr_obj))

                obj_thread = threading.Thread(target=self.handle_pos_obj, args=(obj_socket, len(self.clients, )))
                obj_thread.start()
        except:
            pass
            #("hello")

    def main_for_clients(self):
        while True:
            #("Waiting for new client...")
            client_socket, addr = self.main_server_socket.accept()
            self.obj_client += 1
            #(f"New client connected: {addr}")

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=self.handle_client_main, args=(client_socket,))
            client_thread.start()
            print("opened thread")

    def array_to_dict(self, array):
        dictionary = {index: value for index, value in enumerate(array)}
        return dictionary

    def start_chat(self):
        while True:
            clientSocket, clientAddress = self.hostSocket.accept()
            self.clients_chat.add(clientSocket)
            #("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
            thread = threading.Thread(target=self.clientThread_chat, args=(clientSocket, clientAddress,))
            thread.start()

    def clientThread_chat(self, clientSocket, clientAddress):
        while True:
            message = clientSocket.recv(1024).decode("utf-8")
            #(clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message)
            for client_chat in self.clients_chat:
                if client_chat is not clientSocket:
                    client_chat.send(
                        (clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message).encode("utf-8"))

            if not message:
                self.clients.remove(clientSocket)
                #(clientAddress[0] + ":" + str(clientAddress[1]) + " disconnected")
                break

        clientSocket.close()


if __name__ == '__main__':
    my_server = main_server('localhost', 55555, 55556, 55557, 64444)
    #("Starting server...")
    obj_thread = threading.Thread(target=my_server.handle_obj_conection)
    chat_thread = threading.Thread(target=my_server.start_chat)
    database_thread = threading.Thread(target=my_server.handle_database_clients)
    obj_thread.start()
    chat_thread.start()
    database_thread.start()
    threading.Thread(target=my_server.handle_queue_database).start()
    my_server.main_for_clients()


