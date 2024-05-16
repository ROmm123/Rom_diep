import pygame


class StaticObject():
    def __init__(self, setting, x, y, HeldAbility, width_ract, height_ract):
        # Generate random coordinates of x,y pos in the map range
        self.width = width_ract  # Width of the rectangle
        self.height = height_ract  # Height of the rectangle
        self.position = [x, y]
        # pass the.... center.... pos of the obj ,halfbase , setting object
        self.rect_static_obj = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.collision_flag = False
        self.HeldAbility = HeldAbility
        if HeldAbility == "Size":
            self.color = setting.red
            self.image = pygame.image.load("pictures/size.png")
        elif HeldAbility == "Speed":
            self.color = setting.yellow
            self.image = pygame.image.load("pictures/speed.png")
        elif HeldAbility == "Shield":
            self.color = setting.blue
            self.image = pygame.image.load("pictures/shield.png")
        elif HeldAbility == "Full HP":
            self.color = setting.green4
            self.image = pygame.image.load("pictures/health.png")
        elif HeldAbility == "30 HP":
            self.color = setting.green3
            self.image = pygame.image.load("pictures/health2.png")
        elif HeldAbility == "15 HP":
            self.color = setting.green2
            self.image = pygame.image.load("pictures/health3.png")
        else:
            self.color = setting.green
            self.image = pygame.image.load("pictures/health4.png")

        self.move_button = [False, False, False, False]
        self.isAlive = True


class StaticObjects():
    def __init__(self, setting, map_width, map_height, crate_positions):
        self.setting = setting
        self.surface = setting.surface
        self.Static_objects = []
        self.side = ""

        for pos_key, inner_dict in crate_positions.items():
            for inner_key, pos_value in inner_dict.items():
                x, y = pos_value
                x += self.setting.screen_width
                y += self.setting.screen_height
                inner_key = inner_key.split("_")


                if  int(inner_key[1]) <= 245:
                    if int(inner_key[1]) <= 35:
                        obj = StaticObject(setting, x, y,setting.ability[0] ,30,30)
                    elif int(inner_key[1]) <= 35*2:
                        obj = StaticObject(setting, x, y,setting.ability[1], 30,30)
                    elif int(inner_key[1]) <= 35*3:
                        obj = StaticObject(setting, x, y,setting.ability[2],30,30)
                    elif int(inner_key[1]) <= 35*4:
                        obj = StaticObject(setting, x, y, setting.ability[3], 30,30)
                    elif int(inner_key[1]) <= 35*5:
                        obj = StaticObject(setting, x, y, setting.ability[4],22.5,22.5)
                    elif int(inner_key[1]) <= 35*6:
                        obj = StaticObject(setting, x, y, setting.ability[5],15,15)
                    elif int(inner_key[1]) <= 35*7:
                        obj = StaticObject(setting, x, y, setting.ability[6], 7.5, 7.5)

                elif  int(inner_key[1]) <= 490:
                    if int(inner_key[1]) <= 35 * 8:
                        obj = StaticObject(setting, x, y, setting.ability[0], 30, 30)
                    elif int(inner_key[1]) <= 35 * 9:
                        obj = StaticObject(setting, x, y, setting.ability[1], 30, 30)
                    elif int(inner_key[1]) <= 35 * 10:
                        obj = StaticObject(setting, x, y, setting.ability[2], 30, 30)
                    elif int(inner_key[1]) <= 35 * 11:
                        obj = StaticObject(setting, x, y, setting.ability[3], 30, 30)
                    elif int(inner_key[1]) <= 35 * 12:
                        obj = StaticObject(setting, x, y, setting.ability[4], 22.5, 22.5)
                    elif int(inner_key[1]) <= 35 * 13:
                        obj = StaticObject(setting, x, y, setting.ability[5], 15, 15)
                    elif int(inner_key[1]) <= 35 * 14:
                        obj = StaticObject(setting, x, y, setting.ability[6], 7.5, 7.5)


                elif  int(inner_key[1]) <= 735:
                    if int(inner_key[1]) <= 35 * 15:
                        obj = StaticObject(setting, x, y, setting.ability[0], 30, 30)
                    elif int(inner_key[1]) <= 35 * 16:
                        obj = StaticObject(setting, x, y, setting.ability[1], 30, 30)
                    elif int(inner_key[1]) <= 35 * 17:
                        obj = StaticObject(setting, x, y, setting.ability[2], 30, 30)
                    elif int(inner_key[1]) <= 35 * 18:
                        obj = StaticObject(setting, x, y, setting.ability[3], 30, 30)
                    elif int(inner_key[1]) <= 35 * 19:
                        obj = StaticObject(setting, x, y, setting.ability[4], 22.5, 22.5)
                    elif int(inner_key[1]) <= 35 * 20:
                        obj = StaticObject(setting, x, y, setting.ability[5], 15, 15)
                    elif int(inner_key[1]) <= 35 * 21:
                        obj = StaticObject(setting, x, y, setting.ability[6], 7.5, 7.5)

                elif  int(inner_key[1]) <= 980:
                    if int(inner_key[1]) <= 35 * 22:
                        obj = StaticObject(setting, x, y, setting.ability[0], 30, 30)
                    elif int(inner_key[1]) <= 35 * 23:
                        obj = StaticObject(setting, x, y, setting.ability[1], 30, 30)
                    elif int(inner_key[1]) <= 35 * 24:
                        obj = StaticObject(setting, x, y, setting.ability[2], 30, 30)
                    elif int(inner_key[1]) <= 35 * 25:
                        obj = StaticObject(setting, x, y, setting.ability[3], 30, 30)
                    elif int(inner_key[1]) <= 35 * 26:
                        obj = StaticObject(setting, x, y, setting.ability[4], 22.5, 22.5)
                    elif int(inner_key[1]) <= 35 * 27:
                        obj = StaticObject(setting, x, y, setting.ability[5], 15, 15)
                    elif int(inner_key[1]) <= 35 * 28:
                        obj = StaticObject(setting, x, y, setting.ability[6], 7.5, 7.5)

                self.Static_objects.append(obj)

    def draw(self, viewport_x, viewport_y, setting, player_rect):
        collision_list = []
        position_collision = None

        for static_obj in self.Static_objects:
            obj_x = static_obj.position[0] - viewport_x
            obj_y = static_obj.position[1] - viewport_y
            static_obj.rect_static_obj = pygame.Rect(static_obj.position[0], static_obj.position[1], static_obj.width,
                                                     static_obj.height)

            if static_obj.isAlive:
                if -25 <= obj_x <= setting.screen_width + 20 and -25 <= obj_y <= setting.screen_height + 20:
                    self.surface.blit(static_obj.image, (obj_x - 4, obj_y - 4))
                    # checks collision with the player
                    player_collision_result = self.player_collisions(static_obj, player_rect)

                    if player_collision_result is not None:
                        collision_list.append(player_collision_result)
                        static_obj.isAlive = False
                        position_collision = static_obj.position

        return collision_list, position_collision

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

    def give_ability(self):
        for static_obj in self.Static_objects:
            if not static_obj.isAlive:
                self.Static_objects.remove(static_obj)
                return static_obj.HeldAbility

    def extract_values_from_dict(self,dictionary):
        values = []
        print(dictionary, flush=True)
        for key in dictionary:
            values.append(dictionary[key])
        return values
