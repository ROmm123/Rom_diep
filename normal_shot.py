import pygame
import math
import sys
import settings

class NormalShot:
    def __init__(self, radius, color, setting):
        self.radius = radius
        self.color = color
        self.setting = setting
        self.surface = self.setting.surface
        self.speed = 2
        self.direction = [0, 0]
        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        self.green_circles = []
        self.remove_circles = []
        self.offset_distance = 50
        self.shot_button = [False, False]
        self.prev_key = False

    def draw(self):
        for circle in self.green_circles:
            pygame.draw.circle(self.setting.surface, self.color, circle["position"], self.radius)

    def shoot(self, player_position, screen_position, angle):
        mouse_pos = pygame.mouse.get_pos()
        self.direction[0] = mouse_pos[0] - player_position[0]  # Break down mouse position into x and y components
        self.direction[1] = mouse_pos[1] - player_position[1]

        mouse_x = screen_position[0] + self.direction[0]
        mouse_y = screen_position[1] + self.direction[1]

        print("direction", self.direction)
        print("mouse", mouse_x, mouse_y)
        print("screen", screen_position)
        print("center", player_position)

        magnitude = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        if magnitude != 0:
            self.direction[0] /= magnitude
            self.direction[1] /= magnitude

        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        start_x = player_position[0] + self.offset_distance * math.cos(angle)
        start_y = player_position[1] + self.offset_distance * math.sin(angle)
        print("start pos:", start_x, start_y)
        self.green_circles.append({"position": [start_x, start_y], "velocity": self.velocity})

    def update(self):
        for i, circle in enumerate(self.green_circles):
            circle["position"][0] += circle["velocity"][0]
            circle["position"][1] += circle["velocity"][1]
            self.draw()

            if circle["position"][0] < 0 or circle["position"][0] > self.setting.screen[0] or \
                    circle["position"][1] < 0 or circle["position"][1] > self.setting.screen[1]:
                self.remove_circles.append(i)









