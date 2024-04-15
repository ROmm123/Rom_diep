import pygame.time


class setting():

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.clock = pygame.time.Clock()
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 00)
        self.yellow = (255, 255, 0)
        self.blue = (0, 0, 255)
        self.screen = (800, 600)
        self.surface = pygame.display.set_mode(self.screen)
        self.ability = ["Speed", "Size", "health","damage"]

    def update(self):
        pygame.display.update()
        self.clock.tick(60)
