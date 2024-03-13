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
        self.WEAPON = Weapon(30 , 30 , self.setting.green, self.Playerr , self.setting)
        self.NORMAL_SHOT = NormalShot(5, self.setting.green, self.setting)

    def run(self):
        while True:
            key_state = pygame.key.get_pressed()  # Get the state of all keyboard keys
            chunk = self.MAP.calc_chunk()
            self.MAP.draw_map(chunk)

            self.Playerr.handle_events()
            self.Playerr.move()
            self.Playerr.draw()
            self.WEAPON.run_weapon()
            #ADD 400,300 TO SHOT POSITION.
            self.NORMAL_SHOT.handle_events(key_state, self.Playerr.position, self.Playerr.center_x, self.Playerr.center_y, self.Playerr.screen_position, self.WEAPON.angle)

            self.NORMAL_SHOT.update()
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

