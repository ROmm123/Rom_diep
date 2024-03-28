import socket
import threading
import time

class Server:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.clients_lock = threading.Lock()
        self.enemies_num = -1

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(2048).decode("utf-8")
            if not data:
                client_socket.close()
                break
            # data to another client
            if len(self.clients) > 1:
                updated_packet = self.add_enemies_to_packet(data)
                for receiver_socket in self.clients:
                    if receiver_socket != client_socket:
                        receiver_socket.send(updated_packet.encode("utf-8"))
                        time.sleep(0.4)
            else:
                data = "0"
                client_socket.send(data.encode("utf-8"))

    def start(self):
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                with self.clients_lock:
                    self.clients.append(client_socket)
                self.enemies_num+=1
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except KeyboardInterrupt:
            pass
        finally:
            with self.clients_lock:
                for client_socket in self.clients:
                    client_socket.close()

            # Close the server socket
            self.server_socket.close()

    def add_enemies_to_packet(self ,data):
        packet = data+("&"+str(self.enemies_num))
        return packet



if __name__ == '__main__':
    my_server = Server('localhost', 10023)
    my_server.start()