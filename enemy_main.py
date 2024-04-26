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
        self.check(a1, a2, b1, b2, self.data)

    def check(self, a1, a2, b1, b2, data):
        if a2 < self.setting.screen_height and a1 < self.setting.screen_width:
            radius = int(float(data["player_radius"]))
            self.WEAPON.radius = radius
            weapon_angle = data.get("weapon_angle", "")
            if isinstance(weapon_angle, (int, float)):
                angle_str = re.sub(r'[^0-9\.\-]', '', str(weapon_angle))
                try:
                    self.WEAPON.angle = float(angle_str)
                except ValueError:
                    print(f"Invalid angle value: {angle_str}")
            else:
                print("Invalid weapon_angle data type")

            color = (255, 0, 0)
            self.WEAPON.color = color
            self.draw_enemy(color, b1, b2, radius)
            hit = self.player.hit_online(int(data["player_radius"]),int(data["player_position_x"]),int(data["player_position_y"]))
            if hit is not None:
                print(hit)
            if data["shot_start_x"] != None:
                start_x = int(data["shot_start_x"]) + b1
                start_y = int(data["shot_start_y"]) + b2
                velocity_x = float(data["shot_velocity_x"])
                velocity_y = float(data["shot_velocity_y"])
                # if start_y!=0 and start_x!=0 and velocity_x!=0 and velocity_y!=0:
                self.player.NORMAL_SHOT.shots.append({"position": [start_x, start_y], "velocity": [velocity_x,
                                                                                                   velocity_y]})  # adds a shot to an array for it to print on the screen

        else:
            print('0000')

    def draw_enemy(self, color, center_x, center_y, radius):
        center_x = int(center_x) + 400
        center_y = int(center_y) + 300

        self.WEAPON.x = center_x
        self.WEAPON.y = center_y
        radius = int(radius)
        pygame.draw.circle(self.surface, color, (center_x, center_y), radius)
        self.WEAPON.run_enemy_weapon()
        self.WEAPON.color = self.setting.grey
        self.WEAPON.x = 400
        self.WEAPON.y = 300

    def main(self):
        self.calculate()
        print("enemy")
