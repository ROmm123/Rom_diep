import sys
import pygame
from map import *
import player
from settings import setting



class enemy_player():
    def __init__(self,dataa,settings,player):
        self.data = dataa
        self.set = settings
        self.surface = settings.surface
        self.Playerrr = player
        #self.radius = radius
        #self.color = color
        #self.center_x = 500
        #self.center_y = 500

    def calculate(self):
        properties = self.data.split(';')
        k1 = int(properties[5])  # Convert float to int
        k2 = int(properties[6])  # Convert float to int
        b1 = k1 - self.Playerrr.screen_position[0]
        b2 = k2 - self.Playerrr.screen_position[1]
        a1 = abs(k1 - int(self.Playerrr.screen_position[0]))
        a2 = abs(k2 - int(self.Playerrr.screen_position[1]))
        self.check(a1,a2,b1,b2,properties)


    def check(self,a1,a2,b1,b2,properties):
        if a2 < self.set.screen_height and a1 < self.set.screen_width:
            radius = properties[8]
            color_from_packet = properties[7]
            color_from_packet = color_from_packet.replace("("," ")
            color_from_packet = color_from_packet.replace(")", " ")
            color_from_packet = color_from_packet.split(",")
            color=(255,0,0)

            print(f"{self.Playerrr.screen_position},{self.Playerrr.surface},{self.Playerrr.color},{self.Playerrr.radius}")
            self.draw(color,b1,b2,radius)
        else:
            print('0')

    def draw(self, color, center_x, center_y, radius):
        center_x = int(center_x) + self.Playerrr.center_x
        center_y = int(center_y) + self.Playerrr.center_y
        #radius = int(radius)
        pygame.draw.circle(self.surface, color, (center_x, center_y), 35)


