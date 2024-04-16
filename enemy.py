import sys

import pygame

from map import *
from HP import *
from normal_shot import NormalShot
from weapon import Weapon

class Enemy:

    def __init__(self, player_id, x, y, radius,color, setting):
        self.surface = setting.surface  # player surface
        self.map_position = [x, y]  # top left screen position
        self.radius = radius  # player radius
        self.color = setting.red  # player color
        self.setting = setting  # game settings
        self.player_id = player_id  # player id
        self.speed = 5  # player speed
        self.acceleration = 0.1  # player acceleration (NOT USED)
        self.center = [(setting.screen_width / 2) + 300, (setting.screen_height / 2) + 200]  # player's center relative to the screen
        self.position = [self.center[0], self.center[1]]  # player position relative to the map
        self.hp = HP(self.position[0], self.position[1], radius, setting)  # initialize hp
        self.hit_damage = 0
        self.moveIndex = 0

    def get_position_x(self):
        return self.position
    def get_position_y(self):
        return self.position[1]
    def get_rect_player(self):
        # gets and returns the player's rect
        rect_width = self.radius * 2
        rect_height = self.radius * 2
        rect_x = int(self.position[0] - self.radius)
        rect_y = int(self.position[1] - self.radius)
        return pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    def hurt(self):
        # reduces the player's HP and checks if he's dead
        self.hp.Damage += self.hit_damage
        self.hp.FullHP = False
        if self.hp.Damage >= self.radius * 2:
            self.hp.ISAlive = False
        print("damage done:", self.hp.Damage)

    def heal(self):
        # increases the player's HP and checks if the HP is full
        self.hp.Damage -= 2
        if self.hp.Damage <= 0:
            self.hp.FullHP = True
            print("Full HP")
            # HP REGEN NEEDS WORK

    def isntAlive(self):
        # exits the game if the player dies (NEEDS TO RESPAWN INSTEAD)
        if not self.hp.ISAlive:
            return True
        else:
            return False

    def draw(self):
        # draws the player according to its shape, and the hp bar
        pygame.draw.circle(self.surface, self.color,(int(self.position[0]), int(self.position[1])), self.radius)

        pygame.draw.rect(self.surface, self.hp.LifeColor,
                         (self.position[0] - self.radius, self.position[1] + self.radius + 10, 2 * self.radius, 10))
        pygame.draw.rect(self.surface, self.hp.DamageColor,
                        (self.position[0] - self.radius, self.position[1] + self.radius + 10, self.hp.Damage, 10))

    #move the enemy in diagonals
    def move(self):
        if self.moveIndex < 400:
            self.speed = 2 #(self.moveIndex / 25)
            self.center[0] += self.speed
            self.center[1] += self.speed
            self.moveIndex+=1
        elif self.moveIndex < 800:
            self.speed = -2 #-((self.moveIndex-100) / 25)
            self.center[0] += self.speed
            self.center[1] += self.speed
            self.moveIndex +=1
        else:
            self.moveIndex = 0



