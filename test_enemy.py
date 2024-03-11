import sys
import pygame
from map import *
import player
from settings import setting



class enemy_player():

    def Enemy_player(self , x , y , radius , color ,z):
        self.screen_position = z
        self.radius = radius
        self.color = color
        self.center_x = 500
        self.center_y = 500

    def calculate(self,data):
        properties = data.split(',')
        client_circle_x = properties[5]
        client_circle_y = properties[6]
        k1 = int(float(properties[1]))  # Convert float to int
        k2 = int(float(properties[2]))  # Convert float to int
        b1 = k1 - int(self.player.center_x)
        b2 = k2 - int(self.player.center_y)
        a1 = abs(k1 - int(self.player.center_x))
        a2 = abs(k2 - int(self.player.center_y))
        self.check(a1,a2,properties)

    def check(self,a1,a2,properties):
        if a2 < self.settings.screen_height and a1 < self.settings.screen_width:
            self.radius= properties[8]
            color_from_packet = properties[7]
            color_from_packet = color_from_packet.replace("("," ")
            color_from_packet = color_from_packet.replace(")", " ")
            color_from_packet = color_from_packet.split(",")
            print(color_from_packet[0])





    def draw(self):

        pygame.draw.circle(self.surface , self.color ,(self.center_x , self.center_y) , self.radius)

