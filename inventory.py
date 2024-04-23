import pygame
from settings import *


class inventory():
    def __init__(self, settings):
        self.speed_count, self.health_count, self.size_count, self.shield_count = 0, 0, 0, 0
        self.a = None
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

        self.a = [None, None, None, None, None, None, None]
        self.a[0] = '(1) Speed:' + " " + str(self.speed_count)
        self.a[2] = '(2) Health:' + " " + str(self.health_count)
        self.a[4] = '(3) Shield:' + " " + str(self.shield_count)
        self.a[6] = '(4) Size:' + " " + str(self.size_count)
        x = 10
        y = 0
        for i in range(len(self.a)):
            y += 20
            text_surface = text_front.render(self.a[i], False, 'Black')
            self.settings.surface.blit(text_surface, (x, y))

    def add_to_inventory(self, ability):
        if ability is not None:
            if ability == "Speed":
                self.speed_count += 1
            elif ability == "Size":
                self.size_count += 1
            elif ability == "Shield":
                self.shield_count += 1
            else:
                self.health_count += 1

    def remove_from_inventory(self, to_remove):
        if to_remove:
            if "Speed" in to_remove:
                self.speed_count -= 1
            elif "Size" in to_remove:
                self.size_count -= 1
            elif "Shield" in to_remove:
                self.shield_count -= 1
            else:
                self.health_count -= 1



