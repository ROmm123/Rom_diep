import pygame
import random
from HP import HP


class StaticObject():
    def __init__(self, map_width, map_height):
        # Generate random coordinates of x,y pos in the map range
        self.width = 30  # Width of the rectangle
        self.height = 30  # Height of the rectangle
        self.position = [random.randint(450, map_width - 20)  # Random x-coordinate
            , random.randint(350, map_height - 20)]  # Random y-coordinate

        """self.HP = HP((self.position[0] + self.width // 2), (self.position[1] + self.height // 2), self.width // 2,
                     setting)
        # pass the.... center.... pos of the obj ,halfbase , setting object
        self.rect_static_obj = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.collision_flag = False
        self.HeldAbility = random.choice(setting.ability)
        if self.HeldAbility == "Size":
            self.color = setting.blue
        elif self.HeldAbility == "Speed":
            self.color = setting.yellow
        elif self.HeldAbility == "Damage":
            self.color = setting.red
        else:
            self.color = setting.green
        self.move_button = [False, False, False, False]
        self.speed = 5"""


class StaticObjects():

    def __init__(self, map_width, map_height):
        # self.surface = setting.surface
        self.Static_objects = []  # the static object list
        for _ in range(2000):
            obj = StaticObject(map_width, map_height)
            self.Static_objects.append(obj)

    def crate_position_dst_data(self):
        locations = {}
        i = 0
        for obj in self.Static_objects:
            locations.update({'pos_' + str(i): obj.position})
            i = i +1
        return locations

    def draw(self, viewport_x, viewport_y, setting, player_rect, shots_rects):
        collision_list = []
        for static_obj in self.Static_objects:
            obj_x = static_obj.position[0] - viewport_x
            obj_y = static_obj.position[1] - viewport_y
            static_obj.rect_static_obj = pygame.Rect(static_obj.position[0], static_obj.position[1], static_obj.width,
                                                     static_obj.height)
            # checks collision with the shots
            shot_collision_result = self.shot_collisions(shots_rects, static_obj)
            if shot_collision_result is not None:
                collision_list.append(shot_collision_result)

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

        return collision_list

    def player_collisions(self, static_obj, player_rect):
        if static_obj.rect_static_obj.colliderect(player_rect):
            if not static_obj.collision_flag:
                static_obj.collision_flag = True
                self.hurt(static_obj)
                # Calculate the centers of both the player's and static object's rectangles
                player_center_x, player_center_y = player_rect.center
                static_obj_center_x, static_obj_center_y = static_obj.rect_static_obj.center

                # Calculate the horizontal and vertical distances between the centers
                dx = static_obj_center_x - player_center_x
                dy = static_obj_center_y - player_center_y

                # Determine the side of collision based on the sign of the horizontal and vertical distances
                if abs(dx) > abs(dy):
                    if dx > 0:
                        print("left")
                        static_obj.move_button[0] = True
                    else:
                        print("right")
                        static_obj.move_button[1] = True
                else:
                    if dy > 0:
                        print("top")
                        static_obj.move_button[2] = True
                    else:
                        print("bottom")
                        static_obj.move_button[3] = True

                return "player hit"
            else:
                return "player been hit"
        else:
            static_obj.collision_flag = False

    def shot_collisions(self, shots_rects, static_obj):
        for index, shot_rect in enumerate(shots_rects):
            if static_obj.rect_static_obj.colliderect(shot_rect):
                self.hurt(static_obj)
                return "shot index", index

    def hurt(self, static_obj):
        if static_obj in self.Static_objects:
            static_obj.HP.Damage += 10
            if static_obj.HP.Damage >= 2 * static_obj.width:
                static_obj.HP.ISAlive = False

    def give_ability(self):
        for static_obj in self.Static_objects:
            if not static_obj.HP.ISAlive:
                self.Static_objects.remove(static_obj)
                return static_obj.HeldAbility

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

# Example usage:
# setting = pygame.display.set_mode((800, 600))  # Example of creating a Pygame surface
# static_obj = StaticObject(setting, map_width, map_height, side_length, color)
