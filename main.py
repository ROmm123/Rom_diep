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
            self.Playerr.isAlive()
            self.Playerr.handle_events_shapes(key_state)



            if self.Playerr.shape == "circle":
                self.Playerr.WEAPON.run_weapon()
                self.handle_events_shots(key_state, mouse_state)

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

    def handle_events_shots(self, key_state, mouse_state):  # NOT FINISHED?
        if key_state[pygame.K_SPACE] and not self.Playerr.NORMAL_SHOT.shot_button[0]:
            self.Playerr.NORMAL_SHOT.shoot(self.Playerr.position, self.Playerr.screen_position, self.Playerr.WEAPON.angle)
            self.Playerr.NORMAL_SHOT.shot_button[0] = True
        # IF SPACE PRESSED, NORMAL SHOT
        elif not key_state[pygame.K_SPACE] and self.Playerr.NORMAL_SHOT.prev_key:
            self.Playerr.NORMAL_SHOT.shot_button[0] = False
        self.Playerr.NORMAL_SHOT.prev_key = key_state[pygame.K_SPACE]

        if mouse_state[0] and not self.Playerr.NORMAL_SHOT.shot_button[1]:
            self.Playerr.BIG_SHOT.shoot(self.Playerr.position, self.Playerr.screen_position, self.Playerr.WEAPON.angle)
            self.Playerr.NORMAL_SHOT.shot_button[1] = True
        # IF LEFT MOUSE BUTTON PRESSED, BIG SHOT
        elif not mouse_state[0] and self.Playerr.BIG_SHOT.prev_key:
            self.Playerr.NORMAL_SHOT.shot_button[1] = False
        self.Playerr.BIG_SHOT.prev_key = mouse_state[0]

    def handle_events_shapes(self, key_state):
        if key_state[pygame.K_b]:
            self.Playerr.shape = "triangle"
        if key_state[pygame.K_n]:
            self.Playerr.shape = "circle"
        if key_state[pygame.K_v]:
            self.Playerr.WEAPON.rect_height = 40
        if key_state[pygame.K_g]:
            self.Playerr.WEAPON.rect_width = 40
            self.Playerr.WEAPON.offset_distance += 20
        if key_state[pygame.K_h]:
            self.Playerr.WEAPON.rect_height = 25
            self.Playerr.WEAPON.rect_width = 25


if __name__ == '__main__':
    game = Game()
    game.connect_to_server()
    game.run()
    game.close_connections()
    pygame.quit()
