import pygame
from player import Player
from map import Map
from settings import settings
from weapon import Weapon


class Game():

    def __init__(self):
        pygame.init()
        self.setting = settings()
        self.Playerr = Player(0, 0, 35, self.setting.red, self.setting)
        self.MAP = Map(self.Playerr, self.setting)
        self.WEAPON = Weapon(20 , 20 , self.setting.green_fn , self.Playerr , self.setting )

    def run(self):
        while True:
            self.Playerr.handle_events()
            self.Playerr.move()
            chunk = self.MAP.calc_chunk()
            self.MAP.draw_map(chunk)
            self.Playerr.draw()
            self.WEAPON.run_weapon()
            self.setting.update()


if __name__ == '__main__':
    print("sda")
    game = Game()
    game.run()
    pygame.quit()
