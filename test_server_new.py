import socket
import threading

class Server:
    def __init__(self, host, port, udp_port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.clients_lock = threading.Lock()

        # UDP socket setup
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((host, udp_port))
        self.udp_thread = threading.Thread(target=self.handle_udp)
        self.udp_thread.start()
        self.udp_list = []
        print("Server initialized")

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(2048)
                if not data:
                    break
                data = data.decode()
            except:
                print(f"Client {client_socket.getpeername()} disconnected")
                with self.clients_lock:
                    self.clients.remove((client_socket, client_socket.getpeername()))
                    data = '0'
                    for receiver_socket, addr in self.clients:
                        if receiver_socket != client_socket:
                            receiver_socket.send(data.encode("utf-8"))
                client_socket.close()
                break


            if len(self.clients) > 1:
                for receiver_socket, addr in self.clients:
                    if receiver_socket != client_socket:
                        receiver_socket.send(data.encode("utf-8"))
            else:
                data = "0"
                client_socket.send(data.encode())

    def handle_udp(self):
        while True:
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                client_count = str(len(self.clients)-1)
                print("recived from "+ addr +" enemies: "+ client_count)

                for addr in self.udp_list:
                    self.udp_socket.sendto(client_count.encode(), addr)
            except:
                pass

    def start(self):
        try:
            while True:
                print("Waiting for new client...")
                client_socket, addr = self.server_socket.accept()
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
    my_server = Server('localhost', 10023, 10050)
    print("Starting server...")
    #my_server.start()
    my_server.handle_udp()
