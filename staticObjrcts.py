import pygame
import random
from player import Player

class StaticObject(Player):  # Inherits from Player
    def __init__(self, setting, map_width, map_height, side_length, color):
        # Generate random coordinates of x,y pos in the map range
        x = random.randint(0, map_width - side_length)
        y = random.randint(0, map_height - side_length)
        print("pos of obs is" + str(x) + " " + str(y))
        super().__init__(x, y, side_length, color, setting)  # Pass setting as the last argument

    def draw(self):
        # Draw the square for the static object
        pygame.draw.rect(self.surface, self.color, (
            self.center_x - self.side_length // 2, self.center_y - self.side_length // 2, self.side_length,
            self.side_length))

# Example usage:
# setting = pygame.display.set_mode((800, 600))  # Example of creating a Pygame surface
# static_obj = StaticObject(setting, map_width, map_height, side_length, color)
