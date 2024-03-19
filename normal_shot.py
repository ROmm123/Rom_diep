import pygame
import math
import sys
import settings

class NormalShot:
    def __init__(self, radius, color, deceleration, setting):
        self.radius = radius
        self.color = color
        self.deceleration = deceleration
        self.setting = setting
        self.surface = self.setting.surface
        self.ellipse_size = [30, 10]
        self.offset_distance = 50
        self.speed = 5
        self.speed_multiplier = 2
        self.remove_speed = 0.3
        self.direction = [0, 0]
        self.shot_button = [False, False]
        self.prev_key = False
        self.shots = []
        self.remove_shots = []

    def draw(self):
        # Draw the shot circle
        for circle in self.shots:
            pygame.draw.circle(self.setting.surface, self.color, circle["position"], self.radius)

    def draw_ellipse(self):
        for circle in self.shots:
            pygame.draw.ellipse(self.setting.surface, (255, 255, 0), (circle["position"], self.ellipse_size))

    def shoot(self, player_position, screen_position, angle):
        # calculate the starting position and direction of the shot
        mouse_pos = pygame.mouse.get_pos()
        self.direction[0] = mouse_pos[0] - player_position[0]  # break down mouse position into x and y components
        self.direction[1] = mouse_pos[1] - player_position[1]
        mouse_x = screen_position[0] + self.direction[0]
        mouse_y = screen_position[1] + self.direction[1]

        print("mouse", mouse_x, mouse_y)
        print("screen", screen_position)
        print("center", player_position)

        magnitude = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        if magnitude != 0:  # checks if zero vector
            self.direction[0] /= magnitude  # normalize the direction vector (0-1)
            self.direction[1] /= magnitude

        print("direction", self.direction)

        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        start_x = player_position[0] + self.offset_distance * math.cos(angle)   # calculates the starting position - the middle of the weapon
        start_y = player_position[1] + self.offset_distance * math.sin(angle)

        print("start pos:", start_x, start_y)

        self.shots.append({"position": [start_x, start_y], "velocity": [self.velocity[0] * self.speed_multiplier, self.velocity[1] * self.speed_multiplier]})   #adds a shot to an array for it to print on the screen

    def update(self, shot_relative_vector):
        # updates the shots' position
        for i, circle in enumerate(self.shots):
            circle["velocity"][0] *= self.deceleration
            circle["velocity"][1] *= self.deceleration

            circle["position"][0] += circle["velocity"][0] + shot_relative_vector[0]
            circle["position"][1] += circle["velocity"][1] + shot_relative_vector[1]

            self.draw()

            if abs(circle["velocity"][0]) < self.remove_speed and abs(circle["velocity"][1] < self.remove_speed):
                print(circle["velocity"])
                self.remove_shots.append(i)

        self.remove()


    def remove(self):
        # remove shots that have stopped moving
        for index in reversed(self.remove_shots):
            del self.shots[index]
        self.remove_shots.clear()






