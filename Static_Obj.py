import pygame
import random
from HP import HP


class StaticObject():
    def __init__(self, setting, map_width, map_height, x, y, HeldAbility, damage, width_ract, height_ract):
        # Generate random coordinates of x,y pos in the map range
        self.width = width_ract  # Width of the rectangle
        self.height = height_ract  # Height of the rectangle
        self.position = [x, y]
        self.HP = HP((self.position[0] + self.width // 2), (self.position[1] + self.height // 2), self.width // 2,
                     setting,damage)
        # pass the.... center.... pos of the obj ,halfbase , setting object
        self.rect_static_obj = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.collision_flag = False
        self.HeldAbility = HeldAbility
        if HeldAbility == "Size":
            self.color = setting.red
        elif HeldAbility == "Speed":
            self.color = setting.yellow
        elif HeldAbility == "Shield":
            self.color = setting.blue
        elif HeldAbility == "Health1":
            self.color = setting.green
        elif HeldAbility == "Health2":
            self.color = setting.green
        elif HeldAbility == "Health3":
            self.color = setting.green
        elif HeldAbility == "Health4":
            self.color = setting.green

        self.move_button = [False, False, False, False]
        self.speed = 5


class StaticObjects():

    def __init__(self, setting, map_width, map_height, crate_positions , damage_list):
        self.setting = setting
        self.surface = setting.surface
        self.Static_objects = []
        self.side = ""
        print("------------")
        print(damage_list)
        print("-------------")
        damage_array = self.extract_values_from_dict(damage_list)

        for pos_key, inner_dict in crate_positions.items():
            for inner_key, pos_value in inner_dict.items():
                x, y = pos_value
                inner_key = inner_key.split("_")
                damage = damage_array [int(inner_key[1])]

                if  int(inner_key[1]) <= 245:
                    if int(inner_key[1]) <= 35:
                        obj = StaticObject(setting, map_width, map_height, x, y,setting.ability[0] , damage,30,30)
                    elif int(inner_key[1]) <= 35*2:
                        obj = StaticObject(setting, map_width, map_height, x, y,setting.ability[1], damage,30,30)
                    elif int(inner_key[1]) <= 35*3:
                        obj = StaticObject(setting, map_width, map_height, x, y,setting.ability[2], damage,30,30)
                    elif int(inner_key[1]) <= 35*4:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[3], damage,30,30)
                    elif int(inner_key[1]) <= 35*5:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[4], damage,22.5,22.5)
                    elif int(inner_key[1]) <= 35*6:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[5], damage,15,15)
                    elif int(inner_key[1]) <= 35*7:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[6], damage, 7.5, 7.5)

                elif  int(inner_key[1]) <= 490:
                    if int(inner_key[1]) <= 35*8:
                        obj = StaticObject(setting, map_width, map_height, x, y,setting.ability[0] , damage,30,30)
                    elif int(inner_key[1]) <= 35*9:
                        obj = StaticObject(setting, map_width, map_height, x, y,setting.ability[1], damage,30,30)
                    elif int(inner_key[1]) <= 35*10:
                        obj = StaticObject(setting, map_width, map_height, x, y,setting.ability[2], damage,30,30)
                    elif int(inner_key[1]) <= 35*11:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[3], damage,30,30)
                    elif int(inner_key[1]) <= 35*12:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[4], damage,22.5,22.5)
                    elif int(inner_key[1]) <= 35*13:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[5], damage,15,15)
                    elif int(inner_key[1]) <= 35*14:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[6], damage, 7.5, 7.5)

                elif  int(inner_key[1]) <= 735:
                    if int(inner_key[1]) <= 35*15:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[0], damage, 30, 30)
                    elif int(inner_key[1]) <= 35 * 16:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[1], damage, 30, 30)
                    elif int(inner_key[1]) <= 35 * 17:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[2], damage, 30, 30)
                    elif int(inner_key[1]) <= 35 * 18:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[3], damage, 30, 30)
                    elif int(inner_key[1]) <= 35 * 19:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[4], damage, 22.5, 22.5)
                    elif int(inner_key[1]) <= 35 * 20:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[5], damage, 15, 15)
                    elif int(inner_key[1]) <= 35 * 21:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[6], damage, 7.5, 7.5)

                elif  int(inner_key[1]) <= 980:
                    if int(inner_key[1]) <= 35*22:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[0], damage, 30, 30)
                    elif int(inner_key[1]) <= 35 * 23:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[1], damage, 30, 30)
                    elif int(inner_key[1]) <= 35 * 24:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[2], damage, 30, 30)
                    elif int(inner_key[1]) <= 35 * 25:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[3], damage, 30, 30)
                    elif int(inner_key[1]) <= 35 * 26:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[4], damage, 22.5, 22.5)
                    elif int(inner_key[1]) <= 35 * 27:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[5], damage, 15, 15)
                    elif int(inner_key[1]) <= 35 * 28:
                        obj = StaticObject(setting, map_width, map_height, x, y, setting.ability[6], damage, 7.5, 7.5)


                self.Static_objects.append(obj)

    def draw(self, viewport_x, viewport_y, setting, player_rect, normal_shots_rects, big_shots_rects):
        collision_list = []
        normal_position_collision = None
        big_position_collision = None

        for static_obj in self.Static_objects:
            obj_x = static_obj.position[0] - viewport_x
            obj_y = static_obj.position[1] - viewport_y
            static_obj.rect_static_obj = pygame.Rect(static_obj.position[0], static_obj.position[1], static_obj.width,
                                                     static_obj.height)

            # checks collision with the shots
            normal_shot_collision_result = self.normal_shot_collisions(normal_shots_rects, static_obj)
            big_shot_collision_result = self.big_shot_collisions(big_shots_rects, static_obj)
#            npc_shot_collision_result = self.npc_shot_collisions(npc_shots_rects, static_obj)

            if normal_shot_collision_result is not None:
                normal_position_collision = static_obj.position
                collision_list.append(normal_shot_collision_result)

            if big_shot_collision_result is not None:
                big_position_collision = static_obj.position
                collision_list.append(big_shot_collision_result)

            #if npc_shot_collision_result is not None:
             #   npc_position_collision = static_obj.position
              #  collision_list.append(npc_shot_collision_result)

            # checks if the object needs to be drawn
            if static_obj.HP.ISAlive:
                if -25 <= obj_x <= setting.screen_width + 20 and -25 <= obj_y <= setting.screen_height + 20:
                    # print("obj_x_y ", obj_x, obj_y)
                    pygame.draw.rect(self.surface, static_obj.color,
                                     (obj_x, obj_y, static_obj.width, static_obj.height))
                    pygame.draw.rect(self.surface, static_obj.HP.LifeColor,
                                     (obj_x - (static_obj.width // 2), (obj_y + (static_obj.height + 10)),
                                      (2 * static_obj.width), 10))
                    pygame.draw.rect(self.surface, static_obj.HP.DamageColor,
                                     (obj_x - (static_obj.width // 2), (obj_y + (static_obj.height + 10)),
                                      static_obj.HP.Damage, 10))

                    # checks collision with the player
                    player_collision_result = self.player_collisions(static_obj, player_rect)

                    if player_collision_result is not None:
                        collision_list.append(player_collision_result)

                    #if static_obj.rect_static_obj.colliderect(npc_rect):
                    #    print("Collision detected")
                    #    self.hurt(static_obj)

        return collision_list, normal_position_collision, big_position_collision #, npc_position_collision

    def npc_collision(self, npc_shots_rects):
        collision_list = []
        npc_position_collision = None

        for static_obj in self.Static_objects:
            static_obj.rect_static_obj = pygame.Rect(static_obj.position[0], static_obj.position[1], static_obj.width, static_obj.height)

            # checks collision with the shots
            npc_shot_collision_result = self.npc_shot_collisions(npc_shots_rects, static_obj)
            if npc_shot_collision_result is not None:
                npc_position_collision = static_obj.position
                collision_list.append(npc_shot_collision_result)

        return collision_list, npc_position_collision

    def player_collisions(self, static_obj, player_rect):
        if static_obj.rect_static_obj.colliderect(player_rect):
            if not static_obj.collision_flag:
                static_obj.collision_flag = True
                #self.hurt(static_obj) # get position by server to hurt
                # Calculate the centers of both the player's and static object's rectangles
                player_center_x, player_center_y = player_rect.center
                static_obj_center_x, static_obj_center_y = static_obj.rect_static_obj.center

                # Calculate the horizontal and vertical distances between the centers
                dx = static_obj_center_x - player_center_x
                dy = static_obj_center_y - player_center_y

                # Determine the side of collision based on the sign of the horizontal and vertical distances
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.side = "left"
                        static_obj.move_button[0] = True
                    else:
                        self.side = "right"
                        static_obj.move_button[1] = True
                else:
                    if dy > 0:
                        self.side = "top"
                        static_obj.move_button[2] = True
                    else:
                        self.side = "bottom"
                        static_obj.move_button[3] = True

                return "player hit", self.side
            else:
                return self.side
        else:
            static_obj.collision_flag = False

    def normal_shot_collisions(self, normal_shots_rects, static_obj):
        for index, shot_rect in enumerate(normal_shots_rects):
            if static_obj.rect_static_obj.colliderect(shot_rect):
                self.hurt(static_obj, 5)
                return "normal shot index", index

    def big_shot_collisions(self, big_shots_rects, static_obj):
        for index, shot_rect in enumerate(big_shots_rects):
            if static_obj.rect_static_obj.colliderect(shot_rect):
                self.hurt(static_obj, 8.5)
                return "big shot index", index

    def npc_shot_collisions(self, npc_shots_rects, static_obj):
        for index, shot_rect in enumerate(npc_shots_rects):
            if static_obj.rect_static_obj.colliderect(shot_rect):
                self.hurt(static_obj, 5)
                return "npc shot index", index

    def hurt(self, static_obj, damage):
        if static_obj in self.Static_objects:
            static_obj.HP.Damage += damage
            if static_obj.HP.Damage >= 2 * static_obj.width:
                static_obj.HP.ISAlive = False

    def give_ability(self):
        for static_obj in self.Static_objects:
            if not static_obj.HP.ISAlive:
                self.Static_objects.remove(static_obj)
                return static_obj.HeldAbility

    def extract_values_from_dict(self,dictionary):
        values = []
        print(dictionary)
        for key in dictionary:
            values.append(dictionary[key])
        return values

'''
    def move(self, static_obj):
        # Check if the speed condition is met
        if static_obj.speed > 0.3:
            # Apply movement based on the direction
            if static_obj.move_button[0]:
                static_obj.position[0] += static_obj.speed
            elif static_obj.move_button[1]:
                static_obj.position[0] -= static_obj.speed
            elif static_obj.move_button[2]:
                static_obj.position[1] += static_obj.speed
            elif static_obj.move_button[3]:
                static_obj.position[1] -= static_obj.speed

            # Decrease the speed
            static_obj.speed *= 0.99

        # Check if there was a collision
        if static_obj.collision_flag:
            # Reset the collision flag to avoid re-checking in subsequent frames
            static_obj.collision_flag = False

            # Apply movement based on the direction
            if static_obj.move_button[0]:
                static_obj.position[0] += static_obj.speed
            elif static_obj.move_button[1]:
                static_obj.position[0] -= static_obj.speed
            elif static_obj.move_button[2]:
                static_obj.position[1] += static_obj.speed
            elif static_obj.move_button[3]:
                static_obj.position[1] -= static_obj.speed

            # Decrease the speed
            static_obj.speed *= 0.99

            # Check if the speed condition is no longer met
            if static_obj.speed <= 0.3:
                # Reset the speed to avoid slowing down further
                static_obj.speed = 7
'''
# Example usage:
# setting = pygame.display.set_mode((800, 600))  # Example of creating a Pygame surface
# static_obj = StaticObject(setting, map_width, map_height, side_length, color)
