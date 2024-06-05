from Network_chat import *

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()

class socket_data():
    def __init__(self):
        self.data_base_socket = Client_chat(config['main_server_ip'], 64444)  # global socket