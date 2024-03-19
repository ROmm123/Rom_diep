import sys

import pygame

from map import *
from normal_shot import NormalShot
from weapon import Weapon



class Player():

    def __init__(self , x , y , radius , color , setting):
        self.surface = setting.surface
        self.screen_position = [x,y]
        self.radius = radius
        self.color = color
        self.setting = setting
        self.speed = 5
        self.acceleration = 0.1
        self.center_x = setting.screen_width / 2
        self.center_y = setting.screen_height / 2
        self.position = [(self.screen_position[0] + self.center_x), (self.screen_position[1] + self.center_y)]
        self.move_button = [False , False , False , False]
        self.NORMAL_SHOT = NormalShot(5, self.setting.green, self.setting)


    def draw(self):
        pygame.draw.circle(self.surface , self.color ,(self.center_x , self.center_y) , self.radius)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.move_button[0] = True
                elif event.key == pygame.K_d:
                    self.move_button[1] = True
                elif event.key == pygame.K_w:
                    self.move_button[2] = True
                elif event.key == pygame.K_s:
                    self.move_button[3] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.move_button[0] = False
                elif event.key == pygame.K_d:
                    self.move_button[1] = False
                elif event.key == pygame.K_w:
                    self.move_button[2] = False
                elif event.key == pygame.K_s:
                    self.move_button[3] = False


    def move(self):
        self.speed = 5
        if self.move_button[0]:
            self.screen_position[0] -= self.speed
            if self.screen_position[0] < 0:
                self.screen_position[0] += self.speed

        if self.move_button[1]:
            self.screen_position[0] += self.speed

        if self.move_button[2]:
            self.screen_position[1] -= self.speed
            if self.screen_position[1] < 0:
                self.screen_position[1] += self.speed

        if self.move_button[3]:
            self.screen_position[1] += self.speed










