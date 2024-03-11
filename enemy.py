import pygame
import threading
from player import Player
from map import Map
from settings import settings
from weapon import Weapon
from Network import Client
from server_oop import Server

class Enemy():


    def init(self):
        pygame.init()
        self.setting = settings()
        self.Playerr = Player(0, 0, 35, self.setting.red, self.setting)
        self.MAP = Map(self.Playerr, self.setting)
        self.WEAPON = Weapon(20, 20, self.setting.greenfn, self.Playerr, self.setting)

    def run(self):
        while True:
            self.Playerr.handleevents()
            self.Playerr.move()
            chunk = self.MAP.calcchunk()
            self.setting.surface.fill((255,255,255))
            #self.MAP.draw_map(chunk)
            self.Playerr.draw()
            self.WEAPON.run_weapon()
            self.setting.update()
            #self.client.send_data(str(self.Playerr.screen_position))

if __name == '__main':

    game = Enemy()
    game.run()
    pygame.quit()