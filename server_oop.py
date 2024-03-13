import socket
import threading

class Server:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.clients_lock = threading.Lock()

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(2048).decode("utf-8")
            if not data:
                client_socket.close()
                break
            # data to another client
            if len(self.clients) > 1:
                for receiver_socket in self.clients:
                    if receiver_socket != client_socket:
                        receiver_socket.send(data.encode("utf-8"))
            else:
                data = "0"
                client_socket.send(data.encode("utf-8"))

    def start(self):
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                with self.clients_lock:
                    self.clients.append(client_socket)
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket))
                client_thread.start()
        except KeyboardInterrupt:
            pass
        finally:
            with self.clients_lock:
                for client_socket in self.clients:
                    client_socket.close()

            # Close the server socket
            self.server_socket.close()

if __name__ == '__main__':
    my_server = Server('localhost', 10022)
    my_server.start()
