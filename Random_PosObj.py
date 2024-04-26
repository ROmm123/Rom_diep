import pygame
import random
from HP import HP


class StaticObject():
    def __init__(self, map_width, map_height):
        # Generate random coordinates of x,y pos in the map range
        self.width = 30  # Width of the rectangle
        self.height = 30  # Height of the rectangle
        self.position = [random.randint(450, map_width - 20)  # Random x-coordinate
            , random.randint(350, map_height - 20)]  # Random y-coordinate


class Random_Position():

    def __init__(self, map_width, map_height):
        # self.surface = setting.surface
        self.Static_objects = []  # the static object list
        for _ in range(2000):
            obj = StaticObject(map_width, map_height)
            self.Static_objects.append(obj)

    def crate_position_dst_data(self):
        locations = {}
        i = 0
        for obj in self.Static_objects:
            locations.update({'pos_' + str(i): obj.position})
            i = i +1
        return locations
