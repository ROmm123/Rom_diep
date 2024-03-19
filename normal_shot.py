import sys
import pygame
import math

import weapon
from map import *


class NormalShot:
    def __init__(self, color, start_x, start_y, radius, circle_center, setting):
        self.surface = setting.surface
        self.color = color
        self.position = [weapon.rect_center_x, weapon.rect_center_y]
        self.radius = radius
        self.speed = 2
        self.green_circles = []
        self.remove_indices = []
        self.velocity = [self.speed * weapon.dx, self.speed * weapon.dy]
        self.direction = [weapon.dx, weapon.dy]

    def draw(self, screen):
        pygame.draw.circle(self.surface, self.color, (int(self.position[0]), int(self.position[1])), self.radius)


    def update(self):
        self.green_circles.append({"position": [self.position], "velocity": self.velocity})
        #self.position[0] += self.velocity[0]
        #self.position[1] += self.velocity[1]

        for i, circle in enumerate(self.green_circles):
            # Update the position of the green circle based on its velocity
            circle["position"][0] += circle["velocity"][0]
            circle["position"][1] += circle["velocity"][1]

            pygame.draw.circle(self.surface, self.color, (int(circle["position"][0]), int(circle["position"][1])), self.radius)

            if circle["position"][0] < 0 or circle["position"][0] > self.surface.get_width() or \
                    circle["position"][1] < 0 or circle["position"][1] > self.surface.get_height():
                self.remove_indices.append(i)

        # Remove circles that have moved off-screen
        for index in self.remove_indices[::-1]:
            del self.green_circles[index]



