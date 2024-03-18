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
        self.speed = 3
        self.direction = [0, 0]
        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        self.shots = []
        self.remove_shots = []
        self.offset_distance = 50
        self.shot_button = [False, False]
        self.prev_key = False

    def draw(self):
        # Draw the shot circle
        for circle in self.shots:
            pygame.draw.circle(self.setting.surface, self.color, circle["position"], self.radius)

    def shoot(self, player_position, screen_position, angle):
        # calculate the starting position and direction of the shot
        mouse_pos = pygame.mouse.get_pos()
        self.direction[0] = mouse_pos[0] - player_position[0]  # break down mouse position into x and y components
        self.direction[1] = mouse_pos[1] - player_position[1]
        mouse_x = screen_position[0] + self.direction[0]
        mouse_y = screen_position[1] + self.direction[1]

        print("direction", self.direction)
        print("mouse", mouse_x, mouse_y)
        print("screen", screen_position)
        print("center", player_position)

        magnitude = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        if magnitude != 0:  # checks if zero vector
            self.direction[0] /= magnitude  # normalize the direction vector (0-1)
            self.direction[1] /= magnitude

        velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        start_x = player_position[0] + self.offset_distance * math.cos(angle)   # calculates the starting position - the middle of the weapon
        start_y = player_position[1] + self.offset_distance * math.sin(angle)

        print("start pos:", start_x, start_y)

        self.shots.append({"position": [start_x, start_y], "velocity": velocity})   #adds a shot to an array for it to print on the screen

    def update(self, shot_relative_vector):
        # updates the shots' position
        for i, circle in enumerate(self.shots):
            circle["position"][0] += circle["velocity"][0] + shot_relative_vector[0]
            circle["position"][1] += circle["velocity"][1] + shot_relative_vector[1]
            self.draw()

            if circle["position"][0] < 0 or circle["position"][0] > self.setting.screen[0] or \
                    circle["position"][1] < 0 or circle["position"][1] > self.setting.screen[1]:
                self.remove_shots.append(i)     # SHOTS TO REMOVE - NOT FINISHED









