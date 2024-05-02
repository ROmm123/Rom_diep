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
            data = json.loads(data)
            print(" dict data :"+str(data))
            self.queue.put(data)
            print("queue size : "+str(self.queue.qsize()))


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
        return data

    def exists_in_list(self , data) -> dict:
        print(type(data))
        ID = data["ID"] # ID =3
        c= 0;
        for dictionary in self.enemy_dict_list: # [{"ID" : 1.....} , {"ID" : 7.....} ,{"ID" : 3.....}]
            if ID == dictionary["ID"]:
                return True , c
            c+=1
        return None ,None

    def replace(self , data , index):
        self.enemy_dict_lis[index] = data

    def build_EnemieData(self):
        while True:
            if not self.queue.empty():  # Check if the queue is not empty
                data = self.queue.get() # {"ID" : 2 , ...UPDATED_DATA.......}
                if data is not None:  # Check if data is not None
                    flag ,index = self.exists_in_list(data)
                    if flag:
                        with self.clients_lock:
                            self.replace(data, index)
                    else:
                        with self.clients_lock:
                            self.enemy_dict_list.append(data)

    def send_enemy_data(self):
        while True:
            if self.enemy_dict_list:
                # Assuming self.enemy_dict_list is a list of dictionaries
                list_as_string = ','.join(map(str, self.enemy_dict_list))  # Convert dictionaries to strings and join with commas
                result_string = ' ,'.join(list_as_string.split(','))  # Join with spaces
                print(result_string)
                print("type : "+str(type(result_string)))

                # PRINT LIST_AS_STRING
                with self.clients_lock:
                    for client_socket , nigga in self.clients:
                        client_socket.send(result_string.encode("utf-8"))









if __name__ == '__main__':
    my_server = Server('localhost', 11111)
    print("Starting server...")
    threading.Thread(target=my_server.build_EnemieData).start()
    threading.Thread(target=my_server.send_enemy_data).start()
    my_server.s()