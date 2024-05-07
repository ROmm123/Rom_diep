import pygame
import threading
import re  # Import re module for regular expressions
import json
from weapon import Weapon
import math


class enemy_main():
    def __init__(self, data, player, setting):
        self.data = data
        self.setting = setting
        self.surface = setting.surface
        self.player = player
        self.radius = player.radius
        self.image = pygame.image.load("pictures/shmulik_red.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)  # Initial position
        self.angle = 0

    def calculate(self):
        k1 = int(float(self.data["player_position_x"]))  # Convert float to int
        k2 = int(float(self.data["player_position_y"]))  # Convert float to int
        b1 = k1 - self.player.screen_position[0]
        b2 = k2 - self.player.screen_position[1]
        a1 = abs(k1 - int(self.player.screen_position[0]))
        a2 = abs(k2 - int(self.player.screen_position[1]))
        self.check(a1, a2, b1, b2)

    def check(self, a1, a2, b1, b2):
        if a2 < self.setting.screen_height and a1 < self.setting.screen_width:
            radius = int(float(self.data["player_radius"]))
            weapon_angle = self.data.get("weapon_angle", "")
            if isinstance(weapon_angle, (int, float)):
                angle_str = re.sub(r'[^0-9.-]', '', str(weapon_angle))
                try:
                    self.angle = float(angle_str)
                except ValueError:
                    print(f"Invalid angle value: {angle_str}")
            else:
                print("Invalid weapon_angle data type")

            self.draw_enemy(b1, b2, radius)

            self.player.hit_online(self.radius, int(self.data["player_position_x"]) + 400,
                                   int(self.data["player_position_y"]) + 300)

            if self.data["normal_shot_start_x"] is not None:
                start_x = int(self.data["normal_shot_start_x"]) + b1
                start_y = int(self.data["normal_shot_start_y"]) + b2
                velocity_x = float(self.data["normal_shot_velocity_x"])
                velocity_y = float(self.data["normal_shot_velocity_y"])
                # if start_y!=0 and start_x!=0 and velocity_x!=0 and velocity_y!=0:
                self.player.NORMAL_SHOT.shots.append({"position": [start_x, start_y], "velocity": [velocity_x,
                                                                                                   velocity_y]})  # adds a shot to an array for it to print on the screen

            if self.data["big_shot_start_x"] is not None:
                big_start_x = int(self.data["big_shot_start_x"]) + b1
                big_start_y = int(self.data["big_shot_start_y"]) + b2
                big_velocity_x = float(self.data["big_shot_velocity_x"])
                big_velocity_y = float(self.data["big_shot_velocity_y"])
                # if start_y!=0 and start_x!=0 and velocity_x!=0 and velocity_y!=0:
                self.player.BIG_SHOT.shots.append({"position": [big_start_x, big_start_y], "velocity": [big_velocity_x,
                                                                                                big_velocity_y]})  # adds a shot to an array for it to print on the screen

        else:
            pass

    def draw_enemy(self, center_x, center_y, radius):
        if self.data["ability"]:
            self.image = pygame.image.load("pictures/small_enemy_shmulik.png")
            self.radius = 22
            self.rect = self.image.get_rect()
            self.rect.center = (400, 300)  # Initial position
        else:
            self.image = pygame.image.load("pictures/shmulik_red.png")
            self.radius = 28.5
            self.rect = self.image.get_rect()
            self.rect.center = (400, 300)  # Initial position
        center_x = int(center_x) + 400
        center_y = int(center_y) + 300
        radius = int(radius)
        if int(self.data["damage dealt"]) >= 2 * radius:
            center_x = 0
            center_y = 0

        rotated_image = pygame.transform.rotate(self.image, math.degrees(-self.data["weapon_angle"]))
        rotated_rect = rotated_image.get_rect(center=(center_x, center_y))
        self.surface.blit(rotated_image, rotated_rect)

        health_bar = pygame.Rect(center_x - 28.5, (center_y + 28.5 + 10), 2 * 28.5, 10)
        pygame.draw.rect(self.surface, self.setting.green, health_bar)
        pygame.draw.rect(self.surface, self.setting.red,
                         (center_x - 28.5, center_y + 28.5 + 10, self.data["damage dealt"], 10))

    def main(self):
        self.calculate()
