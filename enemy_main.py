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
        self.image, _ = setting.rand_image()
        self.rect = self.image.get_rect()
        self.rect.center = (self.setting.screen_width//2, self.setting.screen_height//2)  # Initial position
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

            self.player.hit_online(self.radius, int(self.data["player_position_x"]) + self.setting.screen_width//2,
                                   int(self.data["player_position_y"]) + self.setting.screen_height//2)

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
            if self.data["ultimate_shot_start_x"] is not None:
                ultimate_start_x = int(self.data["ultimate_shot_start_x"]) + b1
                ultimate_start_y = int(self.data["ultimate_shot_start_y"]) + b2
                ultimate_velocity_x = float(self.data["ultimate_shot_velocity_x"])
                ultimate_velocity_y = float(self.data["ultimate_shot_velocity_y"])
                # if start_y!=0 and start_x!=0 and velocity_x!=0 and velocity_y!=0:
                self.player.ULTIMATE_SHOT.shots.append({"position": [ultimate_start_x, ultimate_start_y], "velocity": [ultimate_velocity_x,
                                                                                                ultimate_velocity_y]})  # adds a shot to an array for it to print on the screen

        else:
            pass

    def draw_enemy(self, center_x, center_y, radius):
        if self.data["ability"]:
            self.image = self.setting.list_of_small_images[self.data["which_picture"]]
            self.radius = 22
            self.rect = self.image.get_rect()
            self.rect.center = (self.setting.screen_width//2, self.setting.screen_height//2)  # Initial position-
        else:
            self.image = self.setting.list_of_images[self.data["which_picture"]]
            self.radius = 30
            self.rect = self.image.get_rect()
            self.rect.center = (self.setting.screen_width//2, self.setting.screen_height//2)  # Initial position
        center_x = int(center_x) + self.setting.screen_width//2
        center_y = int(center_y) + self.setting.screen_height//2
        radius = int(radius)
        if int(self.data["damage dealt"]) >= 2 * radius:
            center_x = 0
            center_y = 0

        rotated_image = pygame.transform.rotate(self.image, math.degrees(-self.data["weapon_angle"]))
        rotated_rect = rotated_image.get_rect(center=(center_x, center_y))
        self.surface.blit(rotated_image, rotated_rect)

        health_bar = pygame.Rect(center_x - 30, (center_y + 30 + 10), 2 * 30, 10)
        pygame.draw.rect(self.surface, self.setting.green, health_bar)
        pygame.draw.rect(self.surface, self.setting.red,
                         (center_x - 30, center_y + 30 + 10, self.data["damage dealt"], 10))

    def main(self):
        self.calculate()
