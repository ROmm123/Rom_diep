import sys
import pygame
from map import *
import player
from settings import setting
import math
from enemy_weapon import enemy_Weapon



class enemy_player():
    def __init__(self,dataa,settings,player,weapon):
        self.data = dataa
        self.set = settings
        self.surface = settings.surface
        self.Playerrr = player
        self.enemy_weapon = weapon
        self.enemy_center_x=0
        self.enemy_center_y=0
        self.enemy_raduis=0
        enemy_playerr=enemy_player(0, 0, 35, self.setting.red, self.setting)
        self.enemy_weapon = enemy_Weapon(70, 70, self.setting.green_fn, self.enemy_player, self.setting)

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
            self.radius = properties[8]
            color_from_packet = properties[7]
            color_from_packet = color_from_packet.replace("("," ")
            color_from_packet = color_from_packet.replace(")", " ")
            color_from_packet = color_from_packet.split(",")
            color=(255,0,0)

            self.draw_enemy(color,b1,b2,self.radius)
            #self.draw_wepon_enemy(properties)
        else:
            print('0')

    def draw_enemy(self, color, center_x, center_y, radius):
        self.center_x = int(center_x) + self.Playerrr.center_x
        self.center_y = int(center_y) + self.Playerrr.center_y
        #radius = int(radius)
        pygame.draw.circle(self.surface, color, (center_x, center_y), 35)



class enemy_obj():
    def __init__(self , center_x , center_y , radius , color , setting):
        self.obj_color=color
        self.obj_x=center_x
        self.obj_y=center_y
        self.obj_raduis=radius
        self.obj_surface=setting.surface
    def draw_wepon_enemy(self,properties):
        '''
        weapon_surf = pygame.Surface((int(properties[11]), int(properties[12])), pygame.SRCALPHA)
        pygame.draw.rect(weapon_surf, self.WEAPON.color , (0, 0, int(properties[11]), int(properties[12])))
        rotated_weapon = pygame.transform.rotate(weapon_surf, math.degrees(-properties[13]))
        '''
        enemy_playerr=enemy_obj()
        self.enemy_weapon = enemy_obj(enemy_player.center_x, enemy_player.center_x, self.setting.green_fn, self.enemy_player, self.setting)
        self.enemy_weapon.enemy_run_weapon()


