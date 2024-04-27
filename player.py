import sys

import pygame

from map import *
# from HP import *
from normal_shot import NormalShot
from weapon import Weapon
import socket


# from inventory import *


class Player():

    def __init__(self, x, y, radius, color, setting):
        self.surface = setting.surface  # player surface
        self.screen_position = [x, y]  # top left screen position
        self.radius = radius  # player radius
        self.color = color  # player color
        self.setting = setting  # game settings
        self.player_id = 0  # player id
        self.speed = 5  # player speed
        self.acceleration = 0.1  # player acceleration (NOT USED)
        self.center = [setting.screen_width / 2, setting.screen_height / 2]  # player's center relative to the screen
        self.triangle_points = (self.center[0], self.center[1] - self.radius * 1.5), (
            self.center[0] - self.radius, self.center[1]), (
            self.center[0] + self.radius, self.center[1])  # triangle player shape points on screen
        self.position = [(self.screen_position[0] + self.center[0]),
                         (self.screen_position[1] + self.center[1])]  # player position relative to the map
        self.move_button = [False, False, False, False, False, False]  # movement buttons (a, d, w, s)
        # self.hp = HP(self.center[0], self.center[1], radius, setting)  # initialize hp
        self.WEAPON = Weapon(25, 25, self.setting.grey, self, self.setting)  # initialize the weapon
        self.NORMAL_SHOT = NormalShot(5, self.setting.green, 0.96, 2, self.setting)  # initialize normal shot
        self.BIG_SHOT = NormalShot(10, self.setting.blue, 0.97, 5, self.setting)  # initialize big shot
        self.normal_shot_cooldown = 500  # 0.5 second in milliseconds
        self.big_shot_cooldown = 3000  # 3 seconds in milliseconds
        self.speed_duration = 10000  # 10 seconds in milliseconds
        self.last_normal_shot_time = pygame.time.get_ticks()  # get the time the moment a normal shot is fired
        self.last_big_shot_time = pygame.time.get_ticks()  # get the time the moment a big shot is fired
        self.speed_start_time = pygame.time.get_ticks()
        # self.inventory = inventory(self.setting)
        self.big_weapon = False
        self.mid_weapon = False
        self.small_weapon = True
        self.ability = []  # list of Strings

    def get_rect_player(self, radius, position1, position2):
        # gets and returns the player's rect
        rect_width = radius * 2
        rect_height = radius * 2
        rect_x = int(position1 - radius)
        rect_y = int(position2 - radius)
        return pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    def hurt(self):
        # reduces the player's HP and checks if he's dead
        self.hp.Damage += 1
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

    def hit(self):
        player_rect = self.get_rect_player(self.radius, self.position[0], self.position[1])

        # check collision with normal shots

        if self.NORMAL_SHOT.get_shot_rects(self.screen_position):
            for i,_ in enumerate(self.NORMAL_SHOT.get_shot_rects(self.screen_position)):
                shot_rect = self.NORMAL_SHOT.get_shot_rects(self.screen_position)[i]
                if player_rect.colliderect(shot_rect):
                    self.NORMAL_SHOT.remove_shots.append(i)

        # check collision with big shots
        '''
        for i,  in enumerate(self.BIG_SHOT.get_shot_rects(self.screen_position)):
            shot_rect = self.BIG_SHOT.get_shot_rects(self.screen_position)[i]
                if player_rect.colliderect(shot_rect):
                    self.BIG_SHOT.remove_shots.append(i)
                    return "big shot"
                    '''
        self.NORMAL_SHOT.remove()

    def hit_online(self, radius, enemy_position_x, enemy_position_y):
        enemy_rect = self.get_rect_player(radius, enemy_position_x, enemy_position_y)
        enemy_position = [enemy_position_x, enemy_position_y]
        player_rect = self.get_rect_player(self.radius, self.position[0], self.position[1])
        # check collision with normal shots
        print("player rect", player_rect)

        if self.NORMAL_SHOT.get_shot_rects(self.screen_position):
            for i,_ in enumerate(self.NORMAL_SHOT.get_shot_rects(self.screen_position)):
                shot_rect = self.NORMAL_SHOT.get_shot_rects(self.screen_position)[i]
                print("shot rect", shot_rect)
                if enemy_rect.colliderect(shot_rect):
                    self.NORMAL_SHOT.remove_shots.append(i)

        # check collision with big shots
        '''
        for i,  in enumerate(self.BIG_SHOT.get_shot_rects(self.screen_position)):
            shot_rect = self.BIG_SHOT.get_shot_rects(self.screen_position)[i]
                if player_rect.colliderect(shot_rect):
                    self.BIG_SHOT.remove_shots.append(i)
                    return "big shot"
                    '''

        self.NORMAL_SHOT.remove()

    def isAlive(self):
        # exits the game if the player dies (NEEDS TO RESPAWN INSTEAD)
        if not self.hp.ISAlive:
            return True
        else:
            return False

    def draw(self):
        # draws the player according to its shape, and the hp bar
        pygame.draw.circle(self.surface, self.color, (self.center[0], self.center[1]), self.radius)

        # pygame.draw.rect(self.surface, self.hp.LifeColor, self.hp.HealthBar)
        # pygame.draw.rect(self.surface, self.hp.DamageColor,(self.center[0] - self.radius, self.center[1] + self.radius + 10, self.hp.Damage, 10))

    def handle_events_movement(self,socket) -> socket.socket(socket.AF_INET, socket.SOCK_STREAM):
        # checks for if any of the movement keys are pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                socket.close_enemies_Am()
                socket.close()
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
                if event.key == pygame.K_i:
                    self.move_button[4] = True
                if event.key==pygame.K_l:
                    self.move_button[5]=True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.move_button[0] = False
                elif event.key == pygame.K_d:
                    self.move_button[1] = False
                elif event.key == pygame.K_w:
                    self.move_button[2] = False
                elif event.key == pygame.K_s:
                    self.move_button[3] = False
                if event.key == pygame.K_i:
                    self.move_button[4] = False
                if event.key==pygame.K_l:
                    self.move_button[5]=False

    def handle_events_shapes(self, key_state):
        # checks for if any of the shapeshift keys are pressed
        if key_state[pygame.K_v]:
            self.WEAPON.rect_height = 40
            self.WEAPON.rect_width = 25
            self.big_weapon = True
            self.mid_weapon = False
            self.small_weapon = False
        elif key_state[pygame.K_g]:
            self.WEAPON.rect_width = 40
            self.WEAPON.rect_height = 25
            self.WEAPON.offset_distance += 20
            self.big_weapon = False
            self.mid_weapon = True
            self.small_weapon = False
        elif key_state[pygame.K_h]:
            self.WEAPON.rect_height = 25
            self.WEAPON.rect_width = 25
            self.big_weapon = False
            self.mid_weapon = False
            self.small_weapon = True

    def handle_events_shots(self, key_state, mouse_state):
        # checks for if any of the attack keys are pressed
        current_time = pygame.time.get_ticks()
        if self.small_weapon == True:  # only if long or regular weapon
            if key_state[pygame.K_SPACE] and not self.NORMAL_SHOT.shot_button[0]:
                if current_time - self.last_normal_shot_time >= self.normal_shot_cooldown:
                    self.NORMAL_SHOT.shoot(self.center, self.screen_position, self.WEAPON.angle)
                    self.NORMAL_SHOT.shot_button[0] = True
                    self.last_normal_shot_time = current_time  # update last shot time

            # IF SPACE PRESSED, NORMAL SHOT
            elif not key_state[pygame.K_SPACE] and self.NORMAL_SHOT.prev_key:
                self.NORMAL_SHOT.shot_button[0] = False
            self.NORMAL_SHOT.prev_key = key_state[pygame.K_SPACE]

        if self.big_weapon == True:  # only if wide or regular weapon
            if key_state[pygame.K_SPACE] and not self.NORMAL_SHOT.shot_button[1]:
                if current_time - self.last_big_shot_time >= self.big_shot_cooldown:
                    self.BIG_SHOT.shoot(self.center, self.screen_position, self.WEAPON.angle)
                    self.NORMAL_SHOT.shot_button[1] = True
                    self.last_big_shot_time = current_time  # update last shot time

            # IF LEFT MOUSE BUTTON PRESSED, BIG SHOT
            elif not key_state[pygame.K_SPACE] and self.BIG_SHOT.prev_key:
                self.NORMAL_SHOT.shot_button[1] = False
            self.BIG_SHOT.prev_key = key_state[pygame.K_SPACE]

    def move(self):
        # moves the player according to the data in handle_events_movement and updates his position
        if self.move_button[0]:  # a
            self.screen_position[0] -= self.speed
            if self.screen_position[0] < 0:
                self.screen_position[0] += self.speed
            if self.screen_position[0] > (250 * 64 + 2) and self.screen_position[0] < (261 * 64-430):
                if self.move_button[5]:
                    self.screen_position[0]=self.screen_position[0]-(31*64)
                self.screen_position[0] += self.speed

        if self.move_button[1]:  # d
            self.screen_position[0] += self.speed
            if self.screen_position[0]>(30780):
                self.screen_position[0] -= self.speed
            if self.screen_position[0] > (240*64 - 430) and self.screen_position[0] < (250 * 64-2):
                if self.move_button[5]:
                    self.screen_position[0]=self.screen_position[0]+(31*64)

                self.screen_position[0] -= self.speed

        if self.move_button[2]:  # w
            self.screen_position[1] -= self.speed
            if self.screen_position[1] < 0:
                self.screen_position[1] += self.speed
            if self.screen_position[1]>(187*64+2) and self.screen_position[1]<(198*64-330):
                if self.move_button[5]:
                    self.screen_position[1]=self.screen_position[1]-(31*64)
                self.screen_position[1] += self.speed

        if self.move_button[3]:  # s
            self.screen_position[1] += self.speed
            print(self.screen_position[1])
            if self.screen_position[1]>(22720):
                self.screen_position[1] -= self.speed
            if self.screen_position[1]>(177*64-330) and self.screen_position[1]<(187*64-2):
                if self.move_button[5]:
                    self.screen_position[1]=self.screen_position[1]+(31*64)
                self.screen_position[1] -= self.speed


        if self.move_button[4]:
            self.inventory.draw_inventory()

        self.position = [(self.screen_position[0] + self.center[0]), (self.screen_position[1] + self.center[1])]
