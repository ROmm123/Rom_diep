import sys
import pygame
from map import *
import player
from settings import setting



class enemy_player():
    def __init__(self,dataa,settings,player):
        self.data = dataa
        self.set = settings
        self.Playerrr = player
        #self.radius = radius
        #self.color = color
        #self.center_x = 500
        #self.center_y = 500

    def calculate(self):
        print(self.data)
        properties = self.data.split(';')
        client_circle_x = properties[5]
        client_circle_y = properties[6]
        k1 = int(float(properties[1]))  # Convert float to int
        k2 = int(float(properties[2]))  # Convert float to int
        b1 = k1 - int(self.Playerrr.center_x)
        b2 = k2 - int(self.Playerrr.center_y)
        a1 = abs(k1 - int(self.Playerrr.center_x))
        a2 = abs(k2 - int(self.Playerrr.center_y))
        self.check(a1,a2,properties)

    def check(self,a1,a2,properties):
        if a2 < self.set.screen_height and a1 < self.set.screen_width:
            radius = properties[8]
            print(radius)
            color_from_packet = properties[7]
            color_from_packet = color_from_packet.replace("("," ")
            color_from_packet = color_from_packet.replace(")", " ")
            color_from_packet = color_from_packet.split(",")
            color=(255,0,0)
            center_x=properties[5]
            center_y=properties[6]
            self.draw(color,center_x,center_y,radius)
        else:
            print('0')

    def draw(self, color, center_x, center_y, radius):
        center_x = int(center_x)
        center_y = int(center_y)
       # radius = int(radius)
        pygame.draw.circle(self.Playerrr.surface, color, (center_x, center_y), 35)


