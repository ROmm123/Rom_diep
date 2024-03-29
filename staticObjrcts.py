import pygame
import random
from HP import HP


class StaticObject():
    def __init__(self, setting, map_width, map_height):
        # Generate random coordinates of x,y pos in the map range
        self.width = 50  # Width of the rectangle
        self.height = 50  # Height of the rectangle
        self.color = random.choice([setting.red, setting.green, setting.blue])  # random col
        self.position = (random.randint(0, map_width - 20)  # Random x-coordinate
                         , random.randint(0, map_height - 20))  # Random y-coordinate
        self.HP = HP((self.position[0] + self.width // 2), (self.position[1] + self.height // 2), self.width // 2,
                     setting)
        # pass the.... center.... pos of the obj ,halfbase , setting object
        self.Rect_static_obj = pygame.Rect(self.position[0], self.position[1], self.width, self.height)


class StaticObjects():

    def __init__(self, setting, map_width, map_height):
        self.surface = setting.surface
        self.Static_objects = []  # the static object list
        for _ in range(100):
            obj = StaticObject(setting, map_width, map_height)
            print(obj.position)
            self.Static_objects.append(obj)

    def draw(self, viewport_x, viewport_y, setting):

        for static_obj in self.Static_objects:
            obj_x = static_obj.position[0] - viewport_x
            obj_y = static_obj.position[1] - viewport_y
            if 0 <= obj_x <= setting.screen_width and 0 <= obj_y <= setting.screen_height:
                pygame.draw.rect(self.surface, static_obj.color, (obj_x, obj_y, static_obj.width, static_obj.height))
                pygame.draw.rect(self.surface, static_obj.HP.LifeColor,
                                 (obj_x - (static_obj.width // 2), (obj_y + (static_obj.height + 10)),
                                  (2 * static_obj.width), 10))

# Example usage:
# setting = pygame.display.set_mode((800, 600))  # Example of creating a Pygame surface
# static_obj = StaticObject(setting, map_width, map_height, side_length, color)
