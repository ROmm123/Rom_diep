import pygame
import random
from HP import HP


class StaticObject():
    def __init__(self, which_server):
        # Generate random coordinates of x,y pos in the map range
        self.width = 30  # Width of the rectangle
        self.height = 30  # Height of the rectangle

        if (which_server == 1):
            self.position = [random.randint(0, 240 * 64 - 430)  # Random x-coordinate
                , random.randint(0, 177 * 64 - 330)]  # Random y-coordinate
        elif (which_server == 2):
            self.position = [random.randint (261 * 64 - 430 , 30784)  # Random x-coordinate
                , random.randint(0, 177 * 64 - 330)]  # Random y-coordinate
        elif (which_server == 3):
            self.position = [random.randint(0, 240 * 64 - 430)  # Random x-coordinate
                , random.randint(198 * 64 - 330, 22724)]  # Random y-coordinate
        elif (which_server == 4):
            self.position = [random.randint(261 * 64 - 430 , 30784)  # Random x-coordinate
                , random.randint(198 * 64 - 330, 22724)]  # Random y-coordinate


class Random_Position():

    def __init__(self, map_width, map_height):
        # self.surface = setting.surface
        self.Static_objects = []  # the static object list
        for _ in range(245):
            obj = StaticObject(1)
            self.Static_objects.append(obj)

        for _ in range(245):
            obj = StaticObject(2)
            self.Static_objects.append(obj)

        for _ in range(245):
            obj = StaticObject(3)
            self.Static_objects.append(obj)

        for _ in range(245):
            obj = StaticObject(4)
            self.Static_objects.append(obj)


    def crate_position_dst_data(self):
        locations = {}
        i = 0
        for obj in self.Static_objects:
            locations.update({'pos_' + str(i): obj.position})
            i = i +1
        return locations
