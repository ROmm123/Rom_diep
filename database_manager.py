from Network_chat import *
class socket_data():
    def __init__(self):
        self.data_base_socket = Client_chat('localhost', 64444)  # global socket