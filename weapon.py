import math

import pygame

class Weapon():

    def __init__(self , width , height , color , playerr , set):
        self.offset_distance = 50
        self.color = color
        self.weapon_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect_center_x
        self.rect_center_y
        self.mouse_x = 0
        self.mouse_y = 0
        self.angle = 0
        self.dx = self.mouse_x - set.screen[0] // 2
        self.dy = self.mouse_y - set.screenn[1] // 2
        self.tangent_x = set.screenn[0] + playerr.radius * math.cos(self.angle)
        self.tangent_y = set.screenn[1] + playerr.radius * math.sin(self.angle)
        self.set = set
        self.player = playerr


    def mouse_pos(self):
        self.mouse_x , self.mouse_y = pygame.mouse.get_pos()

    def calc_angle(self):
        self.angle = math.atan2(self.dy , self.dx)

    def calc_tangent_point(self):
        self.tangent_x = self.set.screen_width // 2  + self.player.radius * math.cos(self.angle)
        self.tangent_y = self.set.screen_height // 2 + self.player.radius * math.sin(self.angle)

    def calc_angle_to_tangent(self):
        angle_to_tangent = math.atan2(self.tangent_y - self.set.screen_height // 2, self.tangent_x - self.set.screen_width // 2)
        return angle_to_tangent
    def calc_rect_pos(self):
        self.rect_center_x = self.tangent_x + self.offset_distance * math.cos(self.calc_angle_to_tangent())
        self.rect_center_y = self.tangent_y + self.offset_distance * math.sin(self.calc_angle_to_tangent())
        self.rect_center_x += (self.player.radius - 15 - self.offset_distance) * math.cos(self.angle)
        self.rect_center_y += (self.player.radius - 15 - self.offset_distance) * math.sin(self.angle)

    def rotate_surf(self):
        self.weapon_surf = pygame.transform.rotate(self.weapon_surf, math.degrees(-self.calc_angle_to_tangent()))

    def draw_weapon(self):
        rect = self.weapon_surf.get_rect(center=(self.rect_center_x , self.rect_center_y))