import socket
import threading
import time

from Network import Client


from Static_Obj import StaticObjects
from settings import setting
import queue
import json

class Server:
    def __init__(self, host, port , tcp_port):


        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        self.clients = []
        self.clients_lock = threading.Lock()
        self.index = 0
        self.queue = queue.Queue()
        self.enemy_dict_list =[]
        self.sending_list =[]

            # socket enemies
        self.Enemies_Am_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Enemies_Am_socket.bind((host, tcp_port))
        self.udp_thread = threading.Thread(target=self.handle_Enemies_Am)
        self.udp_thread.start()
        self.enemies = -1
        self.enemies_am_list = []


        print("Server initialized")

    def handle_client(self):
        while True:

            data = self.recive_from_client()
            print("fresh STR data : "+str(data))
            if data:
                data = json.loads(data)
                print(" dict data :"+str(data))
                self.queue.put(data)
                print("queue size : "+str(self.queue.qsize()))


            '''#print(self.clients)
            if not data:
                print(f"closing socket {count}")
                print(f"Client {client_socket.getpeername()} disconnected")
                with self.clients_lock:
                    self.clients.remove((client_socket, client_socket.getpeername()))
                    client_socket.close()
                print(self.clients)
                break'''

    def handle_Enemies_Am(self):
        try:
            while True:
                data, addr = self.Enemies_Am_socket.recvfrom(2048)
                self.enemies_am_list.append(addr)
                self.enemies+=1
                print("recived from "+ str(addr) +" enemies: "+ str(self.enemies))

                for address in self.enemies_am_list:
                    self.Enemies_Am_socket.sendto(str(self.enemies).encode() , address)
        except:
            print("hello")

    def s(self):
        count = 0
        try:
            while True:
                print("Waiting for new client...")
                data, addr = self.server_socket.recvfrom(2048)
                print(addr)

                count+=1
                print(f"New client connected: {addr}")
                with self.clients_lock:
                    self.clients.append(addr)
                client_thread = threading.Thread(target=self.handle_client)
                client_thread.start()
        except KeyboardInterrupt:
            print("Server stopped")
        finally:
            print("Closing client sockets...")
            self.server_socket.close()
            print("Server socket closed")

    def recive_from_client(self):
        data , addr= self.server_socket.recvfrom(2048).decode("utf-8")
        if data[0] != '{' :
            return None

        index = str(data).find('}')

        return data[:index+1]

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
        self.enemy_dict_list[index] = data

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
                list_as_string = json.dumps(self.enemy_dict_list)
                print(type(list_as_string))
                with self.clients_lock:
                    for address in self.clients:
                        print("sent data : "+str(list_as_string))
                        self.server_socket.sendto(list_as_string.encode("utf-8") , address)









if __name__ == '__main__':
    my_server = Server('localhost', 11111 , 11112)
    print("Starting server...")
    enemies_T = threading.Thread(target = my_server.handle_Enemies_Am).start()
    threading.Thread(target=my_server.build_EnemieData).start()
    threading.Thread(target=my_server.send_enemy_data).start()
    my_server.s()