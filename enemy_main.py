import pygame
import threading
import re  # Import re module for regular expressions
import json


class enemy_main():
    def __init__(self, data, player, setting, weapon):
        self.data = json.loads(data)
        self.set = setting
        self.surface = setting.surface
        self.Playerrr = player
        self.WEAPON = weapon


    def calculate(self):

        k1 = int(float(self.data["player_position_x"])) # Convert float to int
        k2 = int(float(self.data["player_position_y"]))# Convert float to int
        print(k1)
        print(k2)
        b1 = k1 - self.Playerrr.screen_position[0]
        b2 = k2 - self.Playerrr.screen_position[1]
        a1 = abs(k1 - int(self.Playerrr.screen_position[0]))
        a2 = abs(k2 - int(self.Playerrr.screen_position[1]))
        self.check(a1, a2, b1, b2, self.data)

    def check(self, a1, a2, b1, b2, data):
        if a2 < self.set.screen_height and a1 < self.set.screen_width:
            radius = int(float(data["player_radius"]))
            self.WEAPON.radius = radius
            self.WEAPON.angle=float(data["weapon_angle"])
            '''
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
            '''
        else:
            print('0000')

    def draw_enemy(self, color, center_x, center_y, radius):
        center_x = int(center_x) + self.Playerrr.screen_position[0]
        center_y = int(center_y) + self.Playerrr.screen_position[1]

        self.WEAPON.x = center_x
        self.WEAPON.y = center_y
        radius = int(radius)
        pygame.draw.circle(self.surface, color, (center_x, center_y), radius)

        self.WEAPON.run_weaponF()



    def main(self):
        self.calculate()
        print("enemy")
