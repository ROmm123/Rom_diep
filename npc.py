import math
import random
import pygame
import settings
import player
from Static_Obj import StaticObjects
from Static_Obj import StaticObject
from HP import HP
from weapon import Weapon
from normal_shot import NormalShot
from inventory import *

class NPC:

    def __init__(self, x, y, radius, color, setting,  view_radius, player_position):   # enemy,
        self.surface = setting.surface
        self.radius = radius
        self.color = color
        self.setting = setting
        self.surface = self.setting.surface
        self.speed = 2
        self.rect_center_x = 0 #random.randint(0, total screen_width)
        self.rect_center_y = 0 #random.randint(0, total screen_height)
        self.position_map_x = x
        self.position_map_y = y
        self.set = set
        self.VR = view_radius
        self.player_position = player_position #position of plater relative to the map
        self.goal_x = self.rect_center_x
        self.goal_y = self.rect_center_y
        self.angel = 0
        self.can_move = True
        self.hp = HP(self.rect_center_x, self.rect_center_y, radius, setting)  # initialize hp
        self.tangent_x = 0  #for the weapon
        self.tangent_y = 0
        self.w_center_x = 0
        self.w_center_y = 0
        self.rect_npc = pygame.Rect((self.position_map_x-self.radius), (self.position_map_y-self.radius), (self.radius * 2), (self.radius * 2))
        #self.resetDefaultLocation()
        self.shot_cooldown =10000
        self.last_shot_time = pygame.time.get_ticks()
        self.SHOT = NormalShot(5, self.setting.green, 0.962, self.setting, pygame.image.load("pictures/ball_2.png"))  # initialize normal shot
        self.can_orbit = False
        self.distance = math.sqrt((self.goal_x-self.rect_center_x)**2 + (self.goal_y-self.rect_center_y)**2)


    def resetDefaultLocation(self):
    # Default location to seek if we don't see anything to interact with
        self.rect_center_x = random.randint(0,800)           #(0,38400)    # map limit x
        self.rect_center_y = random.randint(0,800)             #(0, 43200)    # map limit
        self.position_map_x = random.randint(12070,12600)
        self.position_map_y = random.randint(480,780)

    def draw(self, player_rect, shots_rects):
            pygame.draw.circle(self.surface, self.color, (int(self.rect_center_x), int(self.rect_center_y)),
                               self.radius)

            pygame.draw.rect(self.surface, self.hp.LifeColor,  # draw the green bar
                             (self.rect_center_x - self.radius, (self.rect_center_y + self.radius + 10),
                              (2 * self.radius), 10))
            pygame.draw.rect(self.surface, self.hp.DamageColor,  # draw the red bar
                             (self.rect_center_x - self.radius, (self.rect_center_y + self.radius + 10),
                              self.hp.Damage, 10))

            #print(self.rect_center_x, self.rect_center_y, 'npcccc')

            player_rect[0] = player_rect[0]
            player_rect[1] = player_rect[1]
            if self.rect_npc.colliderect(player_rect):
                #print("Collision detected")
                self.hurt()
            #print(self.rect_npc)
            #print(player_rect)

            for index, shot_rect in enumerate(shots_rects):
                if self.rect_npc.colliderect(shot_rect):
                    self.hurt()
                    return

    def get_rect(self):
        rect_width = self.radius * 2
        rect_height = self.radius * 2
        rect_x = int(self.position_map_x-self.radius)
        rect_y = int(self.position_map_y-self.radius)
        return pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    def get_target(self, static_objects, screen_pos_x, screen_pos_y, player_positions):       #למצוא מקום טוב יותר למצוא את המטרה במקום בלולאה אין סופית במיין
    #    self.goal_x = self.enemy[0]
    #    self.goal_y = self.enemy[1]
        min = math.sqrt((static_objects[0].position[0] - self.position_map_x) ** 2 + (static_objects[0].position[1] - self.position_map_y) ** 2)
        #for i in range(self.player_position):
        distance = math.sqrt((player_positions[0] - self.position_map_x) ** 2 + (player_positions[1] - self.position_map_y) ** 2)
        if distance < min:
            min = distance
            self.goal_x = player_positions[0] + 30/2 - screen_pos_x  #30 = StaticObject width
            self.goal_y = player_positions[1] + 30/2 - screen_pos_y  #30 = StaticObject height

    def get_angel_to_target(self):
        return math.atan2((self.goal_y-self.rect_center_y),(self.goal_x-self.rect_center_x))
    def get_angel_to_x_y(self,x,y):
        return math.atan2((y - self.rect_center_y), (x - self.rect_center_x))

    def player_collisions(self, static_obj, player_rect):
        if static_obj.rect_static_obj.colliderect(player_rect):
            if not static_obj.collision_flag:
                static_obj.collision_flag = True
                self.hurt()
                # Calculate the centers of both the player's and static object's rectangles
                player_center_x, player_center_y = player_rect.center
                static_obj_center_x, static_obj_center_y = static_obj.rect_static_obj.center

    def is_alive(self):
        if self.hp.ISAlive:
            return True
        else:
            return False

    def move(self):
        if not self.can_move:
            return
        self.angel = self.get_angel_to_target()
        self.rect_center_x += math.cos(self.angel) * self.speed
        self.rect_center_y += math.sin(self.angel) * self.speed
        #self.can_move = False

    def moveTowardLocation(self, x, y):
        #self.can_move = False
        angle = self.get_angel_to_x_y(x, y)
        self.rect_center_x += math.cos(angle) * self.speed
        self.rect_center_y += math.sin(angle) * self.speed
    def flee(self,x,y):
        if not self.can_move:
            return
        self.angel = self.get_angel_to_x_y(x, y)
        self.rect_center_x += math.cos(self.angel) * self.speed
        self.rect_center_y += math.sin(self.angel) * self.speed
        self.can_move = False

    def orbitClockwise(self):
        if not self.can_orbit:
            return
        a = self.get_angel_to_target() + math.pi / 8
        x = self.goal_x + math.cos(a) * self.distance
        y = self.goal_y + math.sin(a) * self.distance
        self.moveTowardLocation(x, y)

    def hurt(self):
        # reduces the player's HP and checks if he's dead
        self.hp.Damage += 5
        self.hp.FullHP = False
        if self.hp.Damage >= self.radius * 2:
            self.hp.ISAlive = False

    def npc_weapon(self):
        if self.hp.ISAlive:
            angle = math.atan2((self.goal_y-self.rect_center_y),(self.goal_x-self.rect_center_x)) #self.get_angel_to_target()

            # Calculate the point on the circle tangent to the mouse position
            self.tangent_x = self.rect_center_x + self.radius * math.cos(angle)
            self.tangent_y = self.rect_center_y + self.radius * math.sin(angle)

            self.w_center_x = self.tangent_x + 50 * math.cos(angle)     # 50 = offset_distance
            self.w_center_y = self.tangent_y + 50 * math.sin(angle)
            self.w_center_x += (self.radius - 15 - 50) * math.cos(angle)
            self.w_center_y += (self.radius - 15 - 50) * math.sin(angle)

            weapon_surf = pygame.Surface((25, 25), pygame.SRCALPHA)
            pygame.draw.rect(weapon_surf, self.setting.grey, (0, 0, 25, 25))

            weapon_surf = pygame.transform.rotate(weapon_surf, math.degrees(-angle))     # Rotate the rectangle surface based on the angle

            rect = weapon_surf.get_rect(center=(self.w_center_x, self.w_center_y))
            self.setting.surface.blit(weapon_surf, rect)

    def handle_events_shots(self, screen_pos_x, screen_pos_y):
        current_time = pygame.time.get_ticks()
        screen_position = [screen_pos_x, screen_pos_y]
        center = [self.rect_center_x, self.rect_center_y]
        self.distance = math.sqrt((self.goal_x-self.rect_center_x)**2 + (self.goal_y-self.rect_center_y)**2)

        self.can_move = True
        self.can_orbit = False

        if self.distance < self.VR:
            self.can_move = False
            self.can_orbit = True
            if current_time - self.last_shot_time >= self.shot_cooldown:
                print("shot")
                self.SHOT.npc_shoot(center, screen_position, self.goal_x, self.goal_y, self.get_angel_to_target())
                self.SHOT.shot_button[0] = True
                self.last_shot_time = current_time  # update last shot time




class NPCS:

    def __init__(self, setting, player_position , position_npc):
        self.setting = setting
        self.surface = setting.surface
        self.NPCs = []  # the NPCs list

        for inner_key, pos_value in position_npc.items():
            x, y = pos_value
            npc = NPC(x, y, 30, self.setting.red, self.setting, 300, player_position)
            self.NPCs.append(npc)

    def add_player(self, player_position):
        npc = NPC(0, 0, 30, self.setting.red, self.setting, 300, player_position)
        self.NPCs.append(npc)
    def run(self, screen_pos_x, screen_pos_y, player_rect, shots_rects, static_objects, player_positions):
        #self.can_move = True
        for NPC in self.NPCs:
            if NPC.hp.ISAlive:
                NPC.get_target(static_objects, screen_pos_x, screen_pos_y, player_positions)
                NPC.rect_npc = pygame.Rect((NPC.position_map_x - NPC.radius), (NPC.position_map_y - NPC.radius), (NPC.radius * 2), (NPC.radius * 2))

                NPC.rect_center_x = NPC.position_map_x - screen_pos_x
                NPC.rect_center_y = NPC.position_map_y - screen_pos_y

                NPC.move()
                #NPC.flee(NPC.goal_x, NPC.goal_y)
                #NPC.orbitClockwise()

                NPC.position_map_x = NPC.rect_center_x + screen_pos_x
                NPC.position_map_y = NPC.rect_center_y + screen_pos_y

                NPC.handle_events_shots(screen_pos_x, screen_pos_y)

                NPC.draw(player_rect, shots_rects)
                NPC.npc_weapon()
            else:
                self.NPCs.remove(NPC)