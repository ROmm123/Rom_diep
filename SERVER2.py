import socket
import threading

class Server:
    def __init__(self, host, port, tcp_port):


        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1000)
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
        print("Server initialized", flush=True)

    def handle_client(self, client_socket,count):
        while True:

            data = self.recive_from_client(client_socket)

            if not data:
                print(f"closing socket {count}", flush=True)
                self.enemies = self.enemies - 1

                for client_socket_am in self.enemies_am_list:
                    try:
                        client_socket_am.send(str(self.enemies).encode())
                    except:
                        self.enemies_am_list.remove(client_socket_am)

                print(f"Client {client_socket.getpeername()} disconnected", flush=True)
                for receiver_socket , addr  in self.clients:
                    if receiver_socket != client_socket:
                        receiver_socket.send("-1".encode())
                        print("i send", flush=True)
                with self.clients_lock:
                    self.clients.remove((client_socket, client_socket.getpeername()))
                    client_socket.close()
                    print("no in list", flush=True)
                print("pass the self.lock", flush=True)
                print(self.clients)
                break


            if len(self.clients) > 1:
                for receiver_socket , addr  in self.clients:
                    if receiver_socket != client_socket:
                        receiver_socket.send(data.encode("utf-8"))


    def handle_Enemies_Am(self):
        try:
            while True:
                client_socket, addr = self.Enemies_Am_socket.accept()
                self.enemies_am_list.append(client_socket)
                self.enemies+=1
                print("recived from "+ str(addr) +" enemies: "+ str(self.enemies), flush=True)

                for client_socket in self.enemies_am_list:
                    client_socket.send(str(self.enemies).encode())
        except ConnectionRefusedError as e:
            print(f"{e}", flush=True)

    def s(self):
        count = 0
        try:
            while True:
                print("Waiting for new client...", flush=True)
                client_socket, addr = self.server_socket.accept()
                print(addr)

                count+=1
                print(f"New client connected: {addr}", flush=True)
                with self.clients_lock:
                    self.clients.append((client_socket, addr))
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,count,))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server stopped", flush=True)
        finally:
            print("Closing client sockets...", flush=True)
            with self.clients_lock:
                for client_socket, _ in self.clients:
                    client_socket.close()

            self.server_socket.close()
            print("Server socket closed", flush=True)

    def recive_from_client(self, client_socket):
        try:
            data = client_socket.recv(2048).decode("utf-8")
            return data
        except:
            return None




if __name__ == '__main__':
    my_server = Server('0.0.0.0', 22222, 22223)
    print("Starting server...", flush=True)
    enemies_T = threading.Thread(target = my_server.handle_Enemies_Am)
    enemies_T.start()
    my_server.s()