import sys
import pygame
from map import *
import player
from settings import setting
import math
import re


class enemy_calculate():
    def __init__(self,dataa,settings,player,weapon):
        self.data = dataa
        self.set = settings
        self.surface = settings.surface
        self.Playerrr = player
        self.WEAPON = weapon

    def calculate(self):
        properties = self.data.split(';')
        k1 = int(float(properties[5]))  # Convert float to int
        k2 = int(float(properties[6]))  # Convert float to int
        b1 = k1 - self.Playerrr.screen_position[0]
        b2 = k2 - self.Playerrr.screen_position[1]
        a1 = abs(k1 - int(self.Playerrr.screen_position[0]))
        a2 = abs(k2 - int(self.Playerrr.screen_position[1]))
        self.check(a1,a2,b1,b2,properties)


    def check(self,a1,a2,b1,b2,properties):
        if a2 < self.set.screen_height and a1 < self.set.screen_width:
            radius = int(float(properties[8]))
            self.WEAPON.radius = radius
            angle_str = re.sub(r'[^0-9\.\-]', '', properties[13])
            self.WEAPON.angle = float(angle_str)
            color_from_packet = properties[7]
            color_from_packet = color_from_packet.replace("("," ")
            color_from_packet = color_from_packet.replace(")", " ")
            color_from_packet = color_from_packet.split(",")
            color=(255,0,0)
            self.WEAPON.color=color
            self.draw_enemy(color,b1,b2,radius)
            #self.draw_wepon_enemy(properties)
        else:
            print('0')

    def draw_enemy(self, color, center_x, center_y, radius):
        center_x = int(center_x) + self.Playerrr.center_x
        center_y = int(center_y) + self.Playerrr.center_y
        self.WEAPON.x=center_x
        self.WEAPON.y=center_y
        #radius = int(radius)
        pygame.draw.circle(self.surface, color, (center_x, center_y), 35)

        self.WEAPON.run_weapon()
    def draw_wepon_enemy(self,properties):
        '''
        weapon_surf = pygame.Surface((int(properties[11]), int(properties[12])), pygame.SRCALPHA)
        pygame.draw.rect(weapon_surf, self.WEAPON.color , (0, 0, int(properties[11]), int(properties[12])))
        rotated_weapon = pygame.transform.rotate(weapon_surf, math.degrees(-properties[13]))'''