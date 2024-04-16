import pygame
import threading
import socket
from enemy import Enemy
from player import Player
from map import Map
from settings import settings
from weapon import Weapon
from normal_shot import *
from Network import Client
import random
from server_oop import Server
from inventory import *
from static_objects import StaticObjects
from enemy_main import Enemy_main

class main_server():
    def __init__(self, host, port):
        self.main_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_server_socket.bind((host, port))
        self.main_server_socket.listen(5)
        self.clients = []
        self.clients_lock = threading.Lock()

    def main(self):
        while True:
            print("Waiting for new client...")
            client_socket, addr = self.main_server_socket.accept()
            print(addr)


if __name__ == '__main__':
    my_server = main_server('localhost', 33333)
    print("Starting server...")
    my_server.main()