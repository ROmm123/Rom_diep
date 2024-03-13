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
        self.shot_button = [False]
        self.prev_key = False

    def draw(self):
        for circle in self.green_circles:
            pygame.draw.circle(self.setting.surface, self.setting.green, circle["position"], self.radius)

    def shoot(self, player_position, center_x, center_y,  screen_position, angle):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = screen_position[0] + mouse_pos[0]
        mouse_y = screen_position[1] + mouse_pos[1]

        self.direction[0] = mouse_x - player_position[0]
        self.direction[1] = mouse_y - player_position[1]
        print(player_position)

        magnitude = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        if magnitude != 0:
            self.direction[0] /= magnitude
            self.direction[1] /= magnitude

        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        start_x = center_x + self.offset_distance * math.cos(angle)
        start_y = center_y + self.offset_distance * math.sin(angle)
        self.green_circles.append({"position": [start_x, start_y], "velocity": self.velocity})

    def update(self):
        for i, circle in enumerate(self.green_circles):
            circle["position"][0] += circle["velocity"][0]
            circle["position"][1] += circle["velocity"][1]
            self.draw()

            if circle["position"][0] < 0 or circle["position"][0] > self.setting.screen[0] or \
                    circle["position"][1] < 0 or circle["position"][1] > self.setting.screen[1]:
                self.remove_circles.append(i)


    def handle_events(self, key_state, player_position, center_x, center_y, screen_position, angle):
        if key_state[pygame.K_SPACE] and not self.shot_button:
            self.shoot(player_position, center_x, center_y, screen_position, angle)
            self.shot_button = True
        elif not key_state[pygame.K_SPACE] and self.prev_key:
            self.shot_button = False
        self.prev_key = key_state[pygame.K_SPACE]






