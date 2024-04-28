import pygame
import threading
import re  # Import re module for regular expressions
import json


class enemy_main():
    def __init__(self, data, player, setting, weapon):
        self.data = data
        self.setting = setting
        self.surface = setting.surface
        self.player = player
        self.WEAPON = weapon

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
            self.WEAPON.radius = radius
            weapon_angle = self.data.get("weapon_angle", "")
            if isinstance(weapon_angle, (int, float)):
                angle_str = re.sub(r'[^0-9.-]', '', str(weapon_angle))
                try:
                    self.WEAPON.angle = float(angle_str)
                except ValueError:
                    print(f"Invalid angle value: {angle_str}")
            else:
                print("Invalid weapon_angle data type")

            color = (255, 0, 0)
            self.WEAPON.color = color
            self.draw_enemy(color, b1, b2, radius)

            self.player.hit_online(self.player.radius, int(self.data["player_position_x"]) + 400,
                                   int(self.data["player_position_y"]) + 300)
            if self.data["shot_start_x"] != None:
                start_x = int(self.data["shot_start_x"]) + b1
                start_y = int(self.data["shot_start_y"]) + b2
                velocity_x = float(self.data["shot_velocity_x"])
                velocity_y = float(self.data["shot_velocity_y"])
                # if start_y!=0 and start_x!=0 and velocity_x!=0 and velocity_y!=0:
                self.player.NORMAL_SHOT.shots.append({"position": [start_x, start_y], "velocity": [velocity_x,
                                                                                                   velocity_y]})  # adds a shot to an array for it to print on the screen

        else:
            pass
    def draw_enemy(self, color, center_x, center_y, radius):
        center_x = int(center_x) + 400
        center_y = int(center_y) + 300

        self.WEAPON.x = center_x
        self.WEAPON.y = center_y
        radius = int(radius)
        if int(self.data["damage dealt"]) >= 2*radius:
            center_x = 0
            center_y = 0
        pygame.draw.circle(self.surface, color, (center_x, center_y), radius)
        health_bar = pygame.Rect(center_x - radius, (center_y + radius + 10), 2 * radius, 10)
        pygame.draw.rect(self.surface, self.setting.green, health_bar)
        pygame.draw.rect(self.surface, self.setting.red,
                         (center_x - radius, center_y + radius + 10, self.data["damage dealt"], 10))
        self.WEAPON.run_enemy_weapon()
        self.WEAPON.color = self.setting.grey
        self.WEAPON.x = 400
        self.WEAPON.y = 300

    def main(self):
        self.calculate()
