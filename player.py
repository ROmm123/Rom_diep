import sys

import pygame

from map import *
from settings import setting



class Player():

    def __init__(self , x , y , radius , color , setting):
        self.surface = setting.surface
        self.screen_position = [x,y]
        self.radius = radius
        self.color = color
        self.speed = 5
        self.center_x = 400
        self.center_y = 300
        self.Move_button = [False , False , False , False]

    def draw(self):
        pygame.draw.circle(self.surface , self.color ,(self.center_x , self.center_y) , self.radius)

    def draw_client(self, data):
        if data == "0":
            return
        else:
            properties = data.split(',')
            client_circle_x = properties[5]
            client_circle_y = properties[6]
            print(f"{client_circle_x},{client_circle_y}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.Move_button[0] = True
                elif event.key == pygame.K_d:
                    self.Move_button[1] = True
                elif event.key == pygame.K_w:
                    self.Move_button[2] = True
                elif event.key == pygame.K_s:
                    self.Move_button[3] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.Move_button[0] = False
                elif event.key == pygame.K_d:
                    self.Move_button[1] = False
                elif event.key == pygame.K_w:
                    self.Move_button[2] = False
                elif event.key == pygame.K_s:
                    self.Move_button[3] = False

    def move(self):

        # Update screen position based on movement direction
        if self.Move_button[0]:
            self.screen_position[0] -= self.speed
            if self.screen_position[0] < 0:
                self.screen_position[0] += self.speed

        if self.Move_button[1]:
            self.screen_position[0] += self.speed

        if self.Move_button[2]:
            self.screen_position[1] -= self.speed
            if self.screen_position[1] < 0:
                self.screen_position[1] += self.speed

        if self.Move_button[3]:
            self.screen_position[1] += self.speed










