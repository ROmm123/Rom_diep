import pygame
import threading
from player import Player
from map import Map
from settings import settings
from weapon import Weapon
from Network import Client
from server_oop import Server

class Game():

    def __init__(self):
        pygame.init()
        self.setting = settings()
        self.Playerr = Player(0, 0, 35, self.setting.red, self.setting)
        self.MAP = Map(self.Playerr, self.setting)
        self.WEAPON = Weapon(20 , 20 , self.setting.green_fn , self.Playerr , self.setting )
        self.server = Server('localhost', 10009)  # Adjust host and port as needed

    def run(self):
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.start()

        while True:
            self.Playerr.handle_events()
            self.Playerr.move()
            chunk = self.MAP.calc_chunk()
            self.MAP.draw_map(chunk)
            self.Playerr.draw()
            self.WEAPON.run_weapon()
            self.setting.update()

    def connect_to_server(self):
        self.client = Client('localhost', 10009)  # Adjust host and port as needed
        self.client.send_data("Hello from client")

    def close_connections(self):
        self.client.close()
        self.server.close()

if __name__ == '__main__':
    game = Game()
    game.connect_to_server()
    game.run()
    game.close_connections()
    pygame.quit()
