import pygame
import random
from HP import HP


class StaticObject:
    def __init__(self, setting, map_width, map_height):
        # Generate random coordinates of x,y pos in the map range
        self.width = 30
        self.height = 30
        self.HoldedAbiliy = random.choice(setting.ability)
        if self.HoldedAbiliy == "Size":
            self.color = setting.blue
        elif self.HoldedAbiliy == "Speed":
            self.color = setting.yellow
        elif self.HoldedAbiliy == "damage":
            self.color = setting.red
        else:
            self.color = setting.green

        self.position = (random.randint(0, map_width - 20)
                         , random.randint(0, map_height - 20))
        self.HP = HP((self.position[0] + self.width // 2), (self.position[1] + self.height // 2), self.width // 2,
                     setting)
        # pass the.... center.... pos of the obj ,halfbase , setting object
        self.Rect_static_obj = pygame.Rect(self.position[0], self.position[1], self.width, self.height)


class StaticObjects():

    def __init__(self, setting, map_width, map_height):
        self.surface = setting.surface
        self.Static_objects = []  # the static object list
        for _ in range(2000):
            obj = StaticObject(setting, map_width, map_height)
            print(obj.position)
            self.Static_objects.append(obj)

    def draw(self, viewport_x, viewport_y, setting):

        for static_obj in self.Static_objects:
            obj_x = static_obj.position[0] - viewport_x
            obj_y = static_obj.position[1] - viewport_y
            if -25 <= obj_x <= setting.screen_width + 20 and -25 <= obj_y <= setting.screen_height + 20:
                pygame.draw.rect(self.surface, static_obj.color, (obj_x, obj_y, static_obj.width, static_obj.height))
                pygame.draw.rect(self.surface, static_obj.HP.LifeColor,
                                 (obj_x - (static_obj.width // 2), (obj_y + (static_obj.height + 10)),
                                  (2 * static_obj.width), 10))
                pygame.draw.rect(self.surface, static_obj.HP.DamageColor,
                                 (obj_x - (static_obj.width // 2), (obj_y + (static_obj.height + 10)),
                                  static_obj.HP.Damage, 10))

    def hurted(self, static_obj):
        if static_obj in self.Static_objects:
            if static_obj.HP.Damage >= 2 * static_obj.width:
                static_obj.HP.ISAlive = False
            else:
                static_obj.HP.Damage += 5

# Example usage:
# setting = pygame.display.set_mode((800, 600))  # Example of creating a Pygame surface
# static_obj = StaticObject(setting, map_width, map_height, side_length, color)
