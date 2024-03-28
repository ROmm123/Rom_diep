import pygame
import threading
from player import Player
from map import Map
from settings import settings
from weapon import Weapon
from normal_shot import NormalShot
from Network import Client
from server_oop import Server


class Game:

    def __init__(self):
        pygame.init()
        self.setting = settings()
        self.Playerr = Player(0, 0, 30, "circle", self.setting.red, self.setting)
        self.MAP = Map(self.Playerr, self.setting)



    def run(self):
        while True:
            self.shot_relative_vector = [0, 0]

            key_state = pygame.key.get_pressed()  # Get the state of all keyboard keys
            mouse_state = pygame.mouse.get_pressed()
            chunk = self.MAP.calc_chunk()
            self.MAP.draw_map(chunk)

            if self.Playerr.screen_position[0] > 0:
                if self.Playerr.move_button[0]:
                    self.shot_relative_vector[0] = self.Playerr.speed

                if self.Playerr.move_button[1]:
                    self.shot_relative_vector[0] = -self.Playerr.speed

            if self.Playerr.screen_position[1] > 0:
                if self.Playerr.move_button[2]:
                    self.shot_relative_vector[1] = self.Playerr.speed

                if self.Playerr.move_button[3]:
                    self.shot_relative_vector[1] = -self.Playerr.speed

            self.Playerr.handle_events()
            self.Playerr.move()
            self.Playerr.draw()
            self.Playerr.handle_events_shapes(key_state)
            self.Playerr.hit()
            self.Playerr.isAlive()



            if self.Playerr.shape == "circle":
                self.Playerr.WEAPON.run_weapon()
                self.Playerr.handle_events_shots(key_state, mouse_state)

            else:
                self.Playerr.WEAPON.remove()

            self.Playerr.NORMAL_SHOT.update(self.shot_relative_vector)
            self.Playerr.BIG_SHOT.update(self.shot_relative_vector)

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
