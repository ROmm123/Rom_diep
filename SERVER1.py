import socket
import threading
from Network import Client


from static_objects import StaticObjects
from settings import settings

class Server:
    def __init__(self, host, port, tcp_port):


        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.clients_lock = threading.Lock()

        self.Enemies_Am_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Enemies_Am_socket.bind((host, tcp_port))
        self.Enemies_Am_socket.listen(5)
        self.udp_thread = threading.Thread(target=self.handle_Enemies_Am)
        self.udp_thread.start()
        self.udp_list = []
        self.enemies = -1
        self.enemies_am_list = []
        print("Server initialized")

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(2048)
                if not data:
                    print("no data")
                    break
                data = data.decode()
            except:
                self.enemies = self.enemies - 1
                print(f"Client {client_socket.getpeername()} disconnected")
                with self.clients_lock:
                    self.clients.remove((client_socket, client_socket.getpeername()))
                break


            if len(self.clients) > 1:
                for receiver_socket , addr  in self.clients:
                    if receiver_socket != client_socket:
                        receiver_socket.send(data.encode("utf-8"))
            '''else:
                data = "0"
                client_socket.send(data.encode())'''

    def handle_Enemies_Am(self):
        try:
            while True:
                client_socket, addr = self.Enemies_Am_socket.accept()
                self.enemies_am_list.append(client_socket)
                self.enemies+=1
                print("recived from "+ str(addr) +" enemies: "+ str(self.enemies))

                for client_socket in self.enemies_am_list:
                    client_socket.send(str(self.enemies).encode())
        except:
            print("hello")

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
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
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




if __name__ == '__main__':
    my_server = Server('localhost', 11111, 11112)
    print("Starting server...")
    enemies_T = threading.Thread(target = my_server.handle_Enemies_Am)
    enemies_T.start()
    my_server.s()

