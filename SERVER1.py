import socket
import threading
import time

from Network import Client


from Static_Obj import StaticObjects
from settings import setting
import queue
import json

class Server:
    def __init__(self, host, port):


        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.clients_lock = threading.Lock()
        self.index = 0
        self.queue = queue.Queue()
        self.enemy_dict_list =[]

        print("Server initialized")

    def handle_client(self, client_socket,count):
        while True:

            data = self.recive_from_client(client_socket)
            print("double dict data :"+str(data))
            self.queue.put(data)


            #print(self.clients)
            if not data:
                print(f"closing socket {count}")
                print(f"Client {client_socket.getpeername()} disconnected")
                with self.clients_lock:
                    self.clients.remove((client_socket, client_socket.getpeername()))
                    client_socket.close()
                print(self.clients)
                break

    def s(self):
        count = 0
        try:
            while True:
                print("Waiting for new client...")
                client_socket, addr = self.server_socket.accept()
                print(addr)

                count+=1
                print(f"New client connected: {addr}")
                with self.clients_lock:
                    self.clients.append((client_socket, addr))
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,count,))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server stopped")
        finally:
            print("Closing client sockets...")
            with self.clients_lock:
                for client_socket, _ in self.clients:
                    client_socket.close()

            self.server_socket.close()
            print("Server socket closed")

    def recive_from_client(self, client_socket):
        data = client_socket.recv(2048).decode("utf-8")
        print(data)
        # Convert the received JSON string to a dictionary
        loaded_data = json.loads(data)
        # Iterate over the keys of the dictionary
        for key in loaded_data.keys():
            # Check if the key is a string
            if isinstance(key, str):
                # Convert the string key to an integer key
                int_key = int(key)
                # Replace the string key with the integer key
                loaded_data[int_key] = loaded_data.pop(key)
        return loaded_data

    def exists_in_list(self , loaded_data) -> dict:
        index_in_list = 0
        keys_iterator = iter(loaded_data.keys())
        ID = next(keys_iterator)
        for dictionary in self.enemy_dict_list:
            dictionary_k_iterator = iter(dictionary.keys())
            exists_ID = next(dictionary_k_iterator)
            if ID == exists_ID:
                return True , index_in_list
            index_in_list+=1
        return False , None

    def replace(self , loaded_data , index):
        self.enemy_dict_lis[index] = loaded_data

    def build_EnemieData(self):
        while True:
            if not self.queue.empty():  # Check if the queue is not empty
                unloaded_data = self.queue.get()
                if unloaded_data is not None:  # Check if data is not None
                    loaded_data = json.loads(unloaded_data)
                    flag, index = self.exists_in_list(loaded_data)
                    if flag:
                        if self.enemy_dict_list[index] != loaded_data:
                            with self.clients_lock:
                                self.replace(loaded_data, index)
                    else:
                        with self.clients_lock:
                            self.enemy_dict_list.append(json.loads(loaded_data))
            else:
                # Sleep briefly to avoid busy-waiting
                time.sleep(0.1)

    def send_enemy_data(self):
        while True:
            for element in self.enemy_dict_list:
                json.dumps(element)
            list_as_string = ','.join(self.enemy_dict_list)
            with self.clients_lock:
                for client_socket , nigga in self.clients:
                    client_socket.send(list_as_string.encode("utf-8"))









if __name__ == '__main__':
    my_server = Server('localhost', 11111)
    print("Starting server...")
    threading.Thread(target=my_server.build_EnemieData).start()
    threading.Thread(target=my_server.send_enemy_data).start()
    my_server.s()