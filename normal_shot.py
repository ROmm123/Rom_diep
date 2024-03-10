import sys
import pygame
import math

import weapon
from map import *


class NormalShot:
    def __init__(self, color, radius, weapon, setting):
        self.surface = setting.surface
        self.color = color
        self.radius = radius
        self.weapon = weapon
        self.speed = 2
        self.green_circles = []
        self.remove_indices = []
        self.velocity = [self.speed * weapon.dx, self.speed * weapon.dy]
        self.direction = [weapon.dx, weapon.dy]
        self.position = [weapon.rect_center_x, weapon.rect_center_y]

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (int(self.position[0]), int(self.position[1])), self.radius)


    def update(self):
        self.green_circles.append({"position": [self.position], "velocity": self.velocity})
        for i, circle in enumerate(self.green_circles):
            # Update the position of the green circle based on its velocity
            circle["position"][0] += circle["velocity"][0]
            circle["position"][1] += circle["velocity"][1]
            pygame.draw.circle(self.surface, self.color, (int(circle["position"][0]), int(circle["position"][1])), self.radius)

            # Remove if off the screen
            if circle["position"][0] < 0 or circle["position"][0] > self.surface.get_width() or \
                    circle["position"][1] < 0 or circle["position"][1] > self.surface.get_height():
                self.remove_indices.append(i)
        for index in self.remove_indices[::-1]:
            del self.green_circles[index]

    def run(self):
        self.draw()
        self.update()




