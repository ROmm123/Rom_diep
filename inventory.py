import pygame
from settings import *


class inventory():
    def __init__(self, settings):
        self.settings = settings

    def draw_inventory(self):
        yellow = pygame.image.load("colors/yellow.jpg")
        green = pygame.image.load("colors/green.jpg")
        blue = pygame.image.load("colors/blue.jpg")
        red = pygame.image.load("colors/red.jpg")

        background_rect = yellow.get_rect(topleft=(0, 0))
        self.settings.surface.blit(yellow, background_rect)
        background_rect = green.get_rect(topleft=(0, 48))
        self.settings.surface.blit(green, background_rect)
        background_rect = blue.get_rect(topleft=(0, 90))
        self.settings.surface.blit(blue, background_rect)
        background_rect = red.get_rect(topleft=(0, 130))
        self.settings.surface.blit(red, background_rect)

        text_front = pygame.font.Font('Power Smash.ttf', 15)
        t = "True"
        f = "0"
        a = [None, None, None, None, None, None, None]
        a[0] = '(1) Speed:' + " " + f
        a[2] = '(2) Health:' + " " + f
        a[4] = '(3) Shield:' + " " + f
        a[6] = '(4) Size:' + " " + f
        x = 10
        y = 0
        for i in range(len(a)):
            y += 20
            text_surface = text_front.render(a[i], False, 'Black')
            self.settings.surface.blit(text_surface, (x, y))
