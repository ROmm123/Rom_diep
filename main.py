import pygame
import threading
from player import Player
from map import Map
from settings import settings
from weapon import Weapon
from normal_shot import NormalShot
from Network import Client
from server_oop import Server

class Game():

    def __init__(self):
        pygame.init()
        self.setting = settings()
        self.Playerr = Player(0, 0, 35, self.setting.red, self.setting)
        self.MAP = Map(self.Playerr, self.setting)
        self.WEAPON = Weapon(30 , 30 , self.setting.green_fn , self.Playerr , self.setting )
        self.NORMAL_SHOT = NormalShot(5, self.setting.green_fn , self.WEAPON , self.setting)

    def run(self):

        while True:
            self.Playerr.handle_events()
            self.Playerr.move()
            chunk = self.MAP.calc_chunk()
            self.MAP.draw_map(chunk)


            self.Playerr.draw()
            self.WEAPON.run_weapon()
            self.NORMAL_SHOT.run()

            self.setting.update()
            self.client.send_data(str(self.Playerr.screen_position))



    def connect_to_server(self):
        self.client = Client('localhost', 10009)

    def close_connections(self):
        self.client.close()
        self.server.close()

if __name__ == '__main__':
    game = Game()
    game.connect_to_server()
    game.run()
    game.close_connections()
    pygame.quit()
