import pygame
import math
import settings

class NormalShot:
    def __init__(self, radius, color, setting):
        self.radius = radius
        self.color = color
        self.setting = setting
        self.surface = self.setting.surface
        self.speed = 3
        self.direction = [0, 0]
        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        self.green_circles = []
        self.remove_circles = []
        self.offset_distance = 50


    def draw(self):
        for circle in self.green_circles:
            pygame.draw.circle(self.setting.surface, self.setting.green, circle["position"], self.radius)

    def shoot(self, screen_position, center_x, center_y, player_position):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = screen_position[0] + mouse_pos[0]
        mouse_y = screen_position[1] + mouse_pos[1]

        # Calculate direction towards the mouse position
        self.direction[0] = mouse_x - player_position[0]
        self.direction[1] = mouse_y - player_position[1]

        # Normalize direction vector
        magnitude = math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        if magnitude != 0:
            self.direction[0] /= magnitude
            self.direction[1] /= magnitude

        # Set initial velocity based on direction
        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]

        # Calculate the starting position based on the center of the player
        start_x = center_x + self.offset_distance * self.direction[0]
        start_y = center_y + self.offset_distance * self.direction[1]

        # Add the green circle to the list with its initial position and velocity
        self.green_circles.append({"position": [start_x, start_y], "velocity": self.velocity})

    def update(self):

        for i, circle in enumerate(self.green_circles):
            # Update the position of the green circle based on its velocity
            circle["position"][0] += circle["velocity"][0]
            circle["position"][1] += circle["velocity"][1]

            # Draw the green circle
            self.draw()

            # If the green circle moves off-screen, mark it for removal
            if circle["position"][0] < 0 or circle["position"][0] > self.setting.screen[0] or \
                    circle["position"][1] < 0 or circle["position"][1] > self.setting.screen[1]:
                self.remove_circles.append(i)

            for index in self.remove_circles[::-1]:
                del self.green_circles[index]


    def run(self, player_position, center_x, center_y, screen_position):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.shoot(screen_position, center_x, center_y, player_position)
        self.update()

