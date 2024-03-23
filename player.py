import sys

import pygame

from map import *
from HP import *
from normal_shot import NormalShot
from weapon import Weapon



class Player():

    def __init__(self , x , y , radius , shape, color , setting):
        self.surface = setting.surface
        self.screen_position = [x,y]
        self.radius = radius
        self.shape = shape
        self.color = color
        self.setting = setting
        self.speed = 5
        self.acceleration = 0.1
        self.center_x = setting.screen_width / 2
        self.center_y = setting.screen_height / 2
        self.triangle_points = (self.center_x, self.center_y - self.radius * 1.5), (self.center_x - self.radius, self.center_y), (self.center_x + self.radius, self.center_y)
        self.position = [(self.screen_position[0] + self.center_x), (self.screen_position[1] + self.center_y)]
        self.move_button = [False , False , False , False]
        self.hp = HP(self.center_x, self.center_y, radius, setting)

    def hurt(self):
        if self.hp.Damage >= self.radius * 2:
            self.hp.ISAlive = False
        else:
            self.hp.Damage += 5
        print(self.hp.Damage)


    def isAlive(self):
        if not self.hp.ISAlive:
            pygame.quit()
            sys.exit()


    def draw(self):
        if self.shape == "circle":
            pygame.draw.circle(self.surface , self.color ,(self.center_x , self.center_y) , self.radius)
            self.speed = 5

        elif self.shape == "triangle":
            pygame.draw.polygon(self.surface , self.color ,[self.triangle_points[0], self.triangle_points[1], self.triangle_points[2]])
            self.speed = 3

        pygame.draw.rect(self.surface, self.hp.LifeColor, self.hp.HealthBar)
        pygame.draw.rect(self.surface, self.hp.DamageColor,
                        (self.center_x - self.radius, self.center_y + self.radius + 10, self.hp.Damage, 10))



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
                elif event.key == pygame.K_x:
                    self.hurt()



    def move(self):
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

