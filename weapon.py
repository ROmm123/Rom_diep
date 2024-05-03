import math
import pygame


class Weapon():

    def __init__(self, width, height, color, player, set):
        self.offset_distance = 50
        self.color = color
        self.weapon_surf = None
        self.rect_center_x = 0
        self.rect_center_y = 0
        self.angle = 0
        self.tangent_x = 0
        self.tangent_y = 0
        self.set = set
        self.player = player
        self.rect_width = width
        self.rect_height = height
        self.dx = 0
        self.dy = 0
        self.x = 400
        self.y = 300

    def calc_angle(self):
        # Calculate the angle between the player and the mouse
        self.dx = pygame.mouse.get_pos()[0] - self.set.screen_width // 2
        self.dy = pygame.mouse.get_pos()[1] - self.set.screen_height // 2
        self.angle = math.atan2(self.dy, self.dx)

    def calc_tangent_point(self):
        # Calculate the point on the circle tangent to the mouse position
        self.tangent_x = self.x + self.player.radius * math.cos(self.angle)
        self.tangent_y = self.y + self.player.radius * math.sin(self.angle)

    def calc_rect_pos(self):
        # Calculate rectangle position on the circular path
        self.rect_center_x = self.tangent_x + self.offset_distance * math.cos(self.angle)
        self.rect_center_y = self.tangent_y + self.offset_distance * math.sin(self.angle)
        self.rect_center_x += (self.player.radius - 15 - self.offset_distance) * math.cos(self.angle)
        self.rect_center_y += (self.player.radius - 15 - self.offset_distance) * math.sin(self.angle)

    def draw_rect(self):
        self.weapon_surf = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        pygame.draw.rect(self.weapon_surf, self.color, (0, 0, self.rect_width, self.rect_height))

    def rotate_surf(self):
        # Rotate the rectangle surface based on the angle
        self.weapon_surf = pygame.transform.rotate(self.weapon_surf, math.degrees(-self.angle))

    def draw_weapon(self):
        # Draw the rotated rectangle
        rect = self.weapon_surf.get_rect(center=(self.rect_center_x, self.rect_center_y))
        self.set.surface.blit(self.weapon_surf, rect)

    def run_weapon(self):
        self.calc_angle()
        self.calc_tangent_point()
        self.calc_rect_pos()
        self.draw_rect()  # Draw the new rectangle
        self.rotate_surf()
        self.draw_weapon()

    def run_enemy_weapon(self):
        self.calc_tangent_point()
        self.calc_rect_pos()
        self.draw_rect()  # Draw the new rectangle
        self.rotate_surf()
        self.draw_weapon()

    def remove(self):
        self.weapon_surf = None
