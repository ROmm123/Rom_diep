import sys

import pygame
import math
from inventory import inventory

from map import *
from HP import *
from normal_shot import NormalShot
from weapon import Weapon
import socket
from login_screen import socket_data


# from inventory import *


class Player():

    def __init__(self, username, password, x, y, radius, color, setting, speed_c, size_c, shield_c, hp_c_60, hp_c_30,
                 hp_c_15, hp_c_5):
        self.socket_data_base_main = socket_data().data_base_socket
        self.username = username
        self.password = password

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
        self.move_button = [False, False, False, False, False, False, True]  # movement buttons (a, d, w, s, l, t, k)
        self.NORMAL_SHOT = NormalShot(5, self.setting.green, 0.962, self.setting,
                                      pygame.image.load("pictures/ball_2.png"))  # initialize normal shot
        self.BIG_SHOT = NormalShot(7, self.setting.blue, 0.95, self.setting,
                                   pygame.image.load("pictures/ball.png"))  # initialize big shot
        self.ULTIMATE_SHOT = NormalShot(10, self.setting.red, 0.97, self.setting,
                                        pygame.image.load("pictures/fireball.png"))
        self.hp = HP(self.center[0], self.center[1], radius, setting)
        self.inventory = inventory(self.setting, speed_c, size_c, shield_c, hp_c_60, hp_c_30, hp_c_15, hp_c_5)
        self.last_normal_shot_time = pygame.time.get_ticks()  # get the time the moment a normal shot is fired
        self.last_big_shot_time = pygame.time.get_ticks()  # get the time the moment a big shot is fired
        self.last_ultimate_shot_time = pygame.time.get_ticks()
        self.speed_start_time = pygame.time.get_ticks()
        self.big_weapon = False
        self.ultimate_weapon = False
        self.small_weapon = True
        self.stored_abilities = []

        self.initiate_abilities("Speed", speed_c)
        self.initiate_abilities("Shield", shield_c)
        self.initiate_abilities("Size", size_c)
        self.initiate_abilities("Full HP", hp_c_60)
        self.initiate_abilities("30 HP", hp_c_30)
        self.initiate_abilities("15 HP", hp_c_15)
        self.initiate_abilities("5 HP", hp_c_5)

        self.ability = {}  # dictionary to stored ability and its expiration time
        self.ability_key_state = None
        self.image, self.num_of_image = setting.rand_image()
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)  # Initial position
        self.angle = 0
        self.auto = 0
        self.chat_flag = False


    def initiate_abilities(self, ability_name, count):
        for _ in range(count):
            self.stored_abilities.append(ability_name)

    def get_rect_player(self, radius, position1, position2):
        # gets and returns the player's rect
        rect_width = radius * 2
        rect_height = radius * 2
        rect_x = int(position1 - radius)
        rect_y = int(position2 - radius)
        return pygame.Rect(rect_x, rect_y, rect_width, rect_height)


    def hurt(self, hit_type):
        small_hit_damage = self.setting.hit_damage["normal shot"]
        big_hit_damage = self.setting.hit_damage["big shot"]
        ultimate_hit_damage = self.setting.hit_damage["ultimate shot"]
        # coll_hit_damage = self.setting.hit_damage["coll"]
        shield_effect = 0 if "Shield" in self.ability else 1

        # reduces the player's HP and checks if he's dead
        if "normal shot" in hit_type:
            self.hp.Damage += small_hit_damage * shield_effect
        if "big shot" in hit_type:
            self.hp.Damage += big_hit_damage * shield_effect
        if "ultimate shot" in hit_type:
            self.hp.Damage += ultimate_hit_damage * shield_effect
        if "npc shot" in hit_type:
            self.hp.Damage += small_hit_damage * shield_effect
        # if "coll" in hit_type:
        # self.hp.Damage += coll_hit_damage * shield_effect

        # reduces the player's HP and checks if he's dead
        if self.hp.Damage >= self.radius * 2:
            self.hp.ISAlive = False
            self.hp.Damage = 0
            self.screen_position = [0, 0]


    def add_ability(self, ability):
        # sets the end time of the ability
        current_time = pygame.time.get_ticks()
        self.ability[ability] = current_time + self.setting.ability_duration


    def update_ability(self):
        # update the ability timer
        to_remove = []
        current_time = pygame.time.get_ticks()
        for ability, end_time in self.ability.items():
            if current_time >= end_time:
                to_remove.append(ability)

        for ability in to_remove:
            del self.ability[ability]


    def hit(self):
        to_remove = []
        player_rect = self.get_rect_player(self.radius, self.position[0], self.position[1])
        # check collision with normal shots

        if self.NORMAL_SHOT.get_shot_rects(self.screen_position):
            for i, _ in enumerate(self.NORMAL_SHOT.get_shot_rects(self.screen_position)):
                shot_rect = self.NORMAL_SHOT.get_shot_rects(self.screen_position)[i]
                if player_rect.colliderect(shot_rect):
                    self.NORMAL_SHOT.remove_shots.append(i)
                    to_remove.append("normal shot")

        if self.BIG_SHOT.get_shot_rects(self.screen_position):
            for i, _ in enumerate(self.BIG_SHOT.get_shot_rects(self.screen_position)):
                shot_rect = self.BIG_SHOT.get_shot_rects(self.screen_position)[i]
                if player_rect.colliderect(shot_rect):
                    self.BIG_SHOT.remove_shots.append(i)
                    to_remove.append("big shot")

        if self.ULTIMATE_SHOT.get_shot_rects(self.screen_position):
            for i, _ in enumerate(self.ULTIMATE_SHOT.get_shot_rects(self.screen_position)):
                shot_rect = self.ULTIMATE_SHOT.get_shot_rects(self.screen_position)[i]
                if player_rect.colliderect(shot_rect):
                    self.ULTIMATE_SHOT.remove_shots.append(i)
                    to_remove.append("ultimate shot")

        self.NORMAL_SHOT.remove()
        self.BIG_SHOT.remove()
        self.ULTIMATE_SHOT.remove()
        return to_remove


    def npc_hit(self, npc_shots_rects):
        to_remove = []
        player_rect = self.get_rect_player(self.radius, self.position[0], self.position[1])

        if npc_shots_rects is not None:
            for i, _ in enumerate(npc_shots_rects):
                shot_rect = npc_shots_rects[i]
                if player_rect.colliderect(shot_rect):
                    to_remove.append("npc shot")
                    to_remove.append(i)
        return to_remove


    def hit_online(self, radius, enemy_position_x, enemy_position_y):
        to_remove = []
        if radius == 22:
            enemy_position_y -= 7
            enemy_position_x -= 7
        enemy_rect = self.get_rect_player(radius, enemy_position_x, enemy_position_y)

        # check collision with normal shots
        if self.NORMAL_SHOT.get_shot_rects(self.screen_position):
            for i, _ in enumerate(self.NORMAL_SHOT.get_shot_rects(self.screen_position)):
                all_shot_rects = self.NORMAL_SHOT.get_shot_rects(self.screen_position)
                shot_rect = None
                length = len(all_shot_rects)
                if i < length:
                    shot_rect = all_shot_rects[i]
                else:
                    print("ERROR")

                if enemy_rect.colliderect(shot_rect):
                    self.NORMAL_SHOT.remove_shots.append(i)
                    to_remove.append("normal shot")

        if self.BIG_SHOT.get_shot_rects(self.screen_position):
            for i, _ in enumerate(self.BIG_SHOT.get_shot_rects(self.screen_position)):
                all_shot_rects = self.BIG_SHOT.get_shot_rects(self.screen_position)
                shot_rect = None
                length = len(all_shot_rects)
                if i < length:
                    shot_rect = all_shot_rects[i]
                else:
                    print("ERROR")

                if enemy_rect.colliderect(shot_rect):
                    self.BIG_SHOT.remove_shots.append(i)
                    to_remove.append("big shot")

        if self.ULTIMATE_SHOT.get_shot_rects(self.screen_position):
            for i, _ in enumerate(self.ULTIMATE_SHOT.get_shot_rects(self.screen_position)):
                all_shot_rects = self.ULTIMATE_SHOT.get_shot_rects(self.screen_position)
                shot_rect = None
                length = len(all_shot_rects)
                if i < length:
                    shot_rect = all_shot_rects[i]
                else:
                    print("ERROR")

                if enemy_rect.colliderect(shot_rect):
                    self.ULTIMATE_SHOT.remove_shots.append(i)
                    to_remove.append("ultimate shot")

        self.NORMAL_SHOT.remove()
        self.BIG_SHOT.remove()
        self.ULTIMATE_SHOT.remove()
        return to_remove


    def isAlive(self):
        # exits the game if the player dies (NEEDS TO RESPAWN INSTEAD)
        if not self.hp.ISAlive:
            return True
        else:
            return False


    def build_dict_logout(self):
        data_for_logout = {
            "username": self.username,
            "password": self.password,
            "x": self.screen_position[0],
            "y": self.screen_position[1],
            "speed_c": self.inventory.speed_count,
            "size_c": self.inventory.size_count,
            "shield_c": self.inventory.shield_count,
            "hp_c_60": self.inventory.health_count,
            "hp_c_30": self.inventory.health2_count,
            "hp_c_15": self.inventory.health3_count,
            "hp_c_5": self.inventory.health4_count,
            "quary": "logout"
        }
        return data_for_logout


    def update_angle(self, mouse_pos):
        if isinstance(mouse_pos, tuple) and len(mouse_pos) == 2:
            dx = mouse_pos[0] - self.rect.centerx
            dy = mouse_pos[1] - self.rect.centery
            self.angle = math.atan2(dy, dx)  # Calculate angle between player and mouse


    def draw(self, mouse_pos):
        self.image = self.setting.list_of_images[self.num_of_image]
        self.radius = 30
        radius = self.radius
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)

        if "Size" in self.ability:
            if (pygame.time.get_ticks() - self.ability["Size"]) >= self.setting.ability_duration:
                del self.ability["Size"]
            else:
                self.image = self.setting.list_of_small_images[self.num_of_image]
                self.radius = 22
                self.rect = self.image.get_rect()
                self.rect.center = (400, 300)

        if isinstance(mouse_pos, tuple) and len(mouse_pos) == 2:
            self.update_angle(mouse_pos)
            rotated_image = pygame.transform.rotate(self.image, math.degrees(-self.angle))
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            self.surface.blit(rotated_image, rotated_rect)

            pygame.draw.rect(self.surface, self.hp.LifeColor, self.hp.HealthBar)
            pygame.draw.rect(self.surface, self.hp.DamageColor,
                             (self.center[0] - radius, self.center[1] + radius + 10, self.hp.Damage, 10))


    def handle_events_movement(self, socket) -> socket.socket(socket.AF_INET, socket.SOCK_STREAM):
        # checks for if any of the movement keys are pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dict_of_logout = self.build_dict_logout()
                self.socket_data_base_main.connect()
                self.socket_data_base_main.send_database_data(dict_of_logout)
                print("Sent data")
                self.socket_data_base_main.close()
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
                if event.key == pygame.K_t:
                    self.move_button[4] = True
                if event.key == pygame.K_l:
                    self.move_button[5] = True
                if event.key == pygame.K_8:
                    self.chat_flag = True
                if event.key == pygame.K_k:
                    if self.move_button[6]:
                        self.move_button[0] = True
                        self.move_button[2] = True
                        self.move_button[6] = False
                    else:
                        self.move_button[0] = False
                        self.move_button[2] = False
                        self.move_button[6] = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.move_button[0] = False
                elif event.key == pygame.K_d:
                    self.move_button[1] = False
                elif event.key == pygame.K_w:
                    self.move_button[2] = False
                elif event.key == pygame.K_s:
                    self.move_button[3] = False
                if event.key == pygame.K_t:
                    self.move_button[4] = False
                if event.key == pygame.K_l:
                    self.move_button[5] = False


    def handle_events_shapes(self, key_state):
        # checks for if any of the shapeshift keys are pressed
        if key_state[pygame.K_v]:
            self.big_weapon = True
            self.ultimate_weapon = False
            self.small_weapon = False
        elif key_state[pygame.K_g]:
            self.big_weapon = False
            self.ultimate_weapon = True
            self.small_weapon = False
        elif key_state[pygame.K_h]:
            self.big_weapon = False
            self.ultimate_weapon = False
            self.small_weapon = True


    def handle_events_abilities(self, key_state):
        to_remove = []
        if key_state[pygame.K_1] and "Speed" in self.stored_abilities and not self.ability_key_state[pygame.K_1]:
            self.add_ability("Speed")
            self.stored_abilities.remove("Speed")
            to_remove.append("Speed")
        elif key_state[pygame.K_2] and "Size" in self.stored_abilities and not self.ability_key_state[pygame.K_2]:
            self.add_ability("Size")
            self.stored_abilities.remove("Size")
            to_remove.append("Size")
        elif key_state[pygame.K_3] and "Shield" in self.stored_abilities and not self.ability_key_state[pygame.K_3]:
            self.add_ability("Shield")
            self.stored_abilities.remove("Shield")
            to_remove.append("Shield")
        elif key_state[pygame.K_4] and "Full HP" in self.stored_abilities and not self.ability_key_state[pygame.K_4]:
            self.add_ability("Full HP")
            self.stored_abilities.remove("Full HP")
            if self.hp.Damage != 0:
                self.hp.Damage = 0
                to_remove.append("Full HP")
        elif key_state[pygame.K_5] and "30 HP" in self.stored_abilities and not self.ability_key_state[pygame.K_5]:
            self.add_ability("30 HP")
            self.stored_abilities.remove("30 HP")
            if self.hp.Damage != 0:
                self.hp.Damage -= 30
                to_remove.append("30 HP")
        elif key_state[pygame.K_6] and "15 HP" in self.stored_abilities and not self.ability_key_state[pygame.K_6]:
            self.add_ability("15 HP")
            self.stored_abilities.remove("15 HP")
            if self.hp.Damage != 0:
                self.hp.Damage -= 15
                to_remove.append("15 HP")
        elif key_state[pygame.K_7] and "5 HP" in self.stored_abilities and not self.ability_key_state[pygame.K_7]:
            self.add_ability("5 HP")
            self.stored_abilities.remove("5 HP")
            if self.hp.Damage != 0:
                self.hp.Damage -= 5
                to_remove.append("5 HP")

        self.ability_key_state = key_state
        self.inventory.remove_from_inventory(to_remove)


    def handle_events_shots(self, key_state):
        # checks for if any of the attack keys are pressed
        current_time = pygame.time.get_ticks()

        if self.small_weapon:  # only if long or regular weapon
            if key_state[pygame.K_SPACE] and not self.NORMAL_SHOT.shot_button[0]:
                if current_time - self.last_normal_shot_time >= self.setting.normal_shot_cooldown:
                    self.NORMAL_SHOT.shoot(self.center, self.angle)
                    self.NORMAL_SHOT.shot_button[0] = True
                    self.last_normal_shot_time = current_time  # update last shot time

            # IF SPACE PRESSED, NORMAL SHOT
            elif not key_state[pygame.K_SPACE] and self.NORMAL_SHOT.prev_key:
                self.NORMAL_SHOT.shot_button[0] = False
            self.NORMAL_SHOT.prev_key = key_state[pygame.K_SPACE]


        elif self.big_weapon:  # only if wide or regular weapon
            if key_state[pygame.K_SPACE] and not self.NORMAL_SHOT.shot_button[1]:
                if current_time - self.last_big_shot_time >= self.setting.big_shot_cooldown:
                    self.BIG_SHOT.shoot(self.center, self.angle)
                    self.NORMAL_SHOT.shot_button[1] = True
                    self.last_big_shot_time = current_time  # update last shot time

            # IF LEFT MOUSE BUTTON PRESSED, BIG SHOT
            elif not key_state[pygame.K_SPACE] and self.BIG_SHOT.prev_key:
                self.NORMAL_SHOT.shot_button[1] = False
            self.BIG_SHOT.prev_key = key_state[pygame.K_SPACE]

        elif self.ultimate_weapon:  # only if long or regular weapon
            if key_state[pygame.K_SPACE] and not self.NORMAL_SHOT.shot_button[2]:
                if current_time - self.last_ultimate_shot_time >= self.setting.ultimate_shot_cooldown:
                    self.ULTIMATE_SHOT.shoot(self.center, self.angle)
                    self.NORMAL_SHOT.shot_button[2] = True
                    self.last_ultimate_shot_time = current_time  # update last shot time

            # IF SPACE PRESSED, NORMAL SHOT
            elif not key_state[pygame.K_SPACE] and self.NORMAL_SHOT.prev_key:
                self.NORMAL_SHOT.shot_button[2] = False
            self.NORMAL_SHOT.prev_key = key_state[pygame.K_SPACE]


    def move(self, ability, collision_side):
        speed = self.speed
        if "Speed" in self.ability:
            if (pygame.time.get_ticks() - self.ability["Speed"]) >= self.setting.ability_duration:
                del self.ability["Speed"]
            else:
                speed = speed * 1.6

        # moves the player according to the data in handle_events_movement and updates his position
        if self.move_button[0]:  # a
            self.screen_position[0] -= speed
            if self.screen_position[0] < 0 or "right" in collision_side:
                self.screen_position[0] += speed
            if (250 * 64 + 2) < self.screen_position[0] < (261 * 64 - 429):
                if self.move_button[5]:
                    self.screen_position[0] = self.screen_position[0] - (31 * 64)
                self.screen_position[0] += speed
                speed = 0

        if self.move_button[1]:  # d
            self.screen_position[0] += speed
            if self.screen_position[0] > 30780 or "left" in collision_side:
                self.screen_position[0] -= speed
            if (240 * 64 - 429) < self.screen_position[0] < (250 * 64 - 2):
                if self.move_button[5]:
                    self.screen_position[0] = self.screen_position[0] + (31 * 64)
                self.screen_position[0] -= speed
                speed = 0

        if self.move_button[2]:  # w
            self.screen_position[1] -= speed
            if self.screen_position[1] < 0 or "bottom" in collision_side:
                self.screen_position[1] += speed
            if (187 * 64 + 2) < self.screen_position[1] < (198 * 64 - 329):
                if self.move_button[5]:
                    self.screen_position[1] = self.screen_position[1] - (31 * 64)
                self.screen_position[1] += speed
                speed = 0

        if self.move_button[3]:  # s
            self.screen_position[1] += speed
            if self.screen_position[1] > 22720 or "top" in collision_side:
                self.screen_position[1] -= speed
            if (177 * 64 - 329) < self.screen_position[1] < (187 * 64 - 2):
                if self.move_button[5]:
                    self.screen_position[1] = self.screen_position[1] + (31 * 64)
                self.screen_position[1] -= speed
                speed = 0

        if self.move_button[4]:
            self.inventory.draw_inventory()
        self.inventory.add_to_inventory(ability)

        self.position = [(self.screen_position[0] + self.center[0]), (self.screen_position[1] + self.center[1])]

        return speed
