import sys
import pygame
import math

import weapon
from map import *


class NormalShot:
    def __init__(self, radius, color, weapon, setting):
        self.radius = radius
        self.color = color
        self.weapon = weapon
        self.setting = setting
        self.surface = setting.surface
        self.speed = 2
        self.green_circles = []
        self.circles_to_remove = []
        self.velocity = (self.speed * weapon.dx, self.speed * weapon.dy)
        self.direction = (weapon.dx, weapon.dy)
        self.position = ( + self.setting.screen_width // 2, weapon.rect_center_y + self.setting.screen_height // 2)

        #DIVIDE THE RECTANGLE'S POSITION INTO X AND Y COORDINATES AND SET AS THE STARTING POINT.

    def draw(self):
        for circle in self.green_circles:
            pygame.draw.circle(self.surface, self.color, circle["position"], self.radius)

    def update(self):
        self.green_circles.append({"position": (self.position[0], self.position[1]), "velocity": (self.velocity[0], self.velocity[1])})

        for circle in self.green_circles:
            # Update the position of the green circle based on its velocity
            circle["position"] = (circle["position"][0] + circle["velocity"][0], circle["position"][1] + circle["velocity"][1])
            pygame.draw.circle(self.surface, self.color, (int(circle["position"][0]), int(circle["position"][1])),self.radius)

            # Check if the circle is off the screen
            if circle["position"][0] < 0 or circle["position"][0] > self.surface.get_width() or \
                    circle["position"][1] < 0 or circle["position"][1] > self.surface.get_height():
                # Add the circle to the list of circles to remove
                self.circles_to_remove.append(circle)

        # Remove circles that have moved off-screen
        for circle in self.circles_to_remove:
            self.green_circles.remove(circle)

    def run(self):
        self.draw()
        self.update()
