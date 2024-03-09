import socket
import threading

class Server:
    def __init__(self, host, port):
        print("here")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.clients_lock = threading.Lock()

    def handle_client(self, client_socket, client_number):
        while True:
            data = client_socket.recv(2048).decode("utf-8")
            print(data)
            if not data:
                client_socket.close()
                break
            # data to another client
            if len(self.clients) > 1:
                other_client_socket = self.clients[1 - client_number]
                other_client_socket.send(data.encode("utf-8"))

    def start(self):
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print("was there")
                with self.clients_lock:
                    self.clients.append(client_socket)
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, len(self.clients) - 1))
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
    my_server = Server('localhost', 10009)
    my_server.start()
