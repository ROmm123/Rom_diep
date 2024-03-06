import pygame
from player import Player
from map import Map
from screen import setting
from settings import settings


class Game():

    def __init__(self):
        pygame.init()
        self.setting = settings()
        self.Playerr = Player(0, 0, 35, self.setting.red, self.setting)
        self.MAP = Map(self.Playerr, self.setting)

    def run(self):
        while True:
            self.Playerr.handle_events()
            self.Playerr.move()
            chunk = self.MAP.calc_chunk()
            self.MAP.draw_map(chunk)
            self.setting.update()


if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
