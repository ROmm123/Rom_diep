import pygame
import math
import sys
import settings

class NormalShot:
    def __init__(self, radius, color, deceleration, damage, setting):
        #self.player_id = player_id
        self.radius = radius
        self.color = color
        self.deceleration = deceleration
        self.damage = damage
        self.setting = setting
        self.surface = self.setting.surface
        self.rect = self.surface.get_rect()
        self.offset_distance = 50
        self.speed = 15
        self.remove_speed = 0.3
        self.direction = [0, 0]
        self.shot_button = [False, False]
        self.prev_key = False
        self.shots = []
        self.remove_shots = []
        self.velocity = []
        self.start_x = 0
        self.start_y = 0
        self.velocity=[0,0]
        self.shot_relative_vector = [0, 0]

    def get_shot_owner_id(self):
        return self.player_id


    def draw(self):
        # Draw the shot circle
        for circle in self.shots:
            pygame.draw.circle(self.setting.surface, self.color, circle["position"], self.radius)

    def shoot(self, player_position, angle, double):
        # calculate the starting position and direction of the shot
        mouse_pos = pygame.mouse.get_pos()
        self.direction[0] = mouse_pos[0] - player_position[0]  # break down mouse position into x and y components
        self.direction[1] = mouse_pos[1] - player_position[1]

        self.magnitude = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        if self.magnitude != 0:  # checks if zero vector
            self.direction[0] /= self.magnitude  # normalize the direction vector (0-1)
            self.direction[1] /= self.magnitude

        if self.direction[0] >= 0:
            player_position[0] += double
        else:
            player_position[0] -= double

        if self.direction[1] >= 0:
            player_position[1] += double
        else:
            player_position[1] -= double


        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        self.start_x = player_position[0] + self.offset_distance * math.cos(angle)   # calculates the starting position - the middle of the weapon
        self.start_y = player_position[1] + self.offset_distance * math.sin(angle)


        self.shots.append({"position": [self.start_x, self.start_y], "velocity": [self.velocity[0] , self.velocity[1]]})   #adds a shot to an array for it to print on the screen

    def npc_shoot(self, npc_position, screen_position, goal_x, goal_y, angle):
        # calculate the starting position and direction of the shot
        self.direction[0] = goal_x - npc_position[0]  # break down mouse position into x and y components
        self.direction[1] = goal_y - npc_position[1]

        magnitude = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        print(magnitude)
        if magnitude != 0:  # checks if zero vector
            self.direction[0] /= magnitude  # normalize the direction vector (0-1)
            self.direction[1] /= magnitude

        print("direction", self.direction)

        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        start_x = npc_position[0] + self.offset_distance * math.cos(angle)  # calculates the starting position - the middle of the weapon
        start_y = npc_position[1] + self.offset_distance * math.sin(angle)

        print("start pos:", start_x, start_y)

        self.shots.append({"position": [start_x, start_y], "velocity": [self.velocity[0], self.velocity[1]]})  # adds a shot to an array for it to print on the screen

    def calc_relative(self,screen_position,move_button,speed):
        self.shot_relative_vector = [0, 0]  # shot relative vector to control bullet movement

        if screen_position[0] > 0:

            if move_button[0] and not move_button[1]:

                self.shot_relative_vector[0] = speed

            if move_button[1] and not move_button[0]:
                self.shot_relative_vector[0] = -speed

        if screen_position[1] > 0:
            if move_button[2] and not move_button[3]:
                self.shot_relative_vector[1] = speed

            if move_button[3] and not move_button[2]:
                self.shot_relative_vector[1] = -speed

    def update(self):

        # updates the shots' position
        for i, circle in enumerate(self.shots):
            circle["velocity"][0] *= self.deceleration
            circle["velocity"][1] *= self.deceleration

            circle["position"][0] += circle["velocity"][0] + self.shot_relative_vector[0]
            circle["position"][1] += circle["velocity"][1] + self.shot_relative_vector[1]
            print(circle["velocity"])
            self.draw()

            # check shots to remove (if below the remove_speed)
            if (abs(circle["velocity"][0]) < self.remove_speed) and (abs(circle["velocity"][1]) < self.remove_speed):
                self.remove_shots.append(i)

        self.remove()

    def remove(self):
        # remove shots that have stopped moving
        if self.shots:
            for index in reversed(self.remove_shots):
                del self.shots[index]
            self.remove_shots.clear()

    def get_shot_rect(self, circle_position):
        rect_width = self.radius * 2
        rect_height = self.radius * 2
        rect_x = int(circle_position[0] - self.radius)
        rect_y = int(circle_position[1] - self.radius)

        return pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    def get_shot_rects(self, screen_position):
        return [self.get_shot_rect((int(circle["position"][0]) + screen_position[0], int(circle["position"][1]) + screen_position[1])) for circle in self.shots]


    def reset(self):
        self.start_x = None
        self.start_y = None
        self.shot_relative_vector = [None, None]
        self.velocity = [None, None]



