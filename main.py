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
        self.WEAPON = Weapon(30 , 30 , self.setting.grey, self.Playerr , self.setting)

        self.NORMAL_SHOT = NormalShot(5, self.setting.green, self.setting)
        self.BIG_SHOT = NormalShot(10, self.setting.blue, self.setting)


    def run(self):
        while True:
            key_state = pygame.key.get_pressed()  # Get the state of all keyboard keys
            mouse_state = pygame.mouse.get_pressed()
            chunk = self.MAP.calc_chunk()
            self.MAP.draw_map(chunk)

            self.Playerr.handle_events()
            self.Playerr.move()
            self.Playerr.draw()
            self.WEAPON.run_weapon()


            self.handle_events_shots(key_state, mouse_state)

            self.NORMAL_SHOT.update()
            self.BIG_SHOT.update()

            self.setting.update()

            self.client.send_data(str(self.Playerr.screen_position))

    def connect_to_server(self):
        self.client = Client('localhost', 10009)

    def close_connections(self):
        self.client.close()
        self.server.close()


    def handle_events_shots(self, key_state, mouse_state):
        if key_state[pygame.K_SPACE] and not self.NORMAL_SHOT.shot_button[0]:
            self.NORMAL_SHOT.shoot(self.Playerr.position, self.Playerr.screen_position, self.WEAPON.angle)
            self.NORMAL_SHOT.shot_button[0] = True
        #IF SPACE PRESSED, NORMAL SHOT
        elif not key_state[pygame.K_SPACE] and self.NORMAL_SHOT.prev_key:
            self.NORMAL_SHOT.shot_button[0] = False
        self.NORMAL_SHOT.prev_key = key_state[pygame.K_SPACE]


        if mouse_state[0] and not self.NORMAL_SHOT.shot_button[1]:
            self.BIG_SHOT.shoot(self.Playerr.position, self.Playerr.screen_position, self.WEAPON.angle)
            self.NORMAL_SHOT.shot_button[1] = True
        #IF LEFT MOUSE BUTTON PRESSED, BIG SHOT
        elif not mouse_state[0] and self.BIG_SHOT.prev_key:
            self.NORMAL_SHOT.shot_button[1] = False
        self.BIG_SHOT.prev_key = mouse_state[0]

if __name__ == '__main__':
    game = Game()
    game.connect_to_server()
    game.run()
    game.close_connections()
    pygame.quit()

