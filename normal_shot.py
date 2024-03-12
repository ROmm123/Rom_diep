import pygame
import math

class NormalShot:
    def __init__(self, radius, color, setting):
        self.radius = radius
        self.color = color
        self.setting = setting
        self.surface = setting.surface
        self.speed = 5
        self.green_circles = []

    def draw(self):
        for circle in self.green_circles:
            pygame.draw.circle(self.surface, self.color, circle["position"], self.radius)

    def update(self,  screen_position):
        for circle in self.green_circles:
            # Update position of the green circle based on its velocity
            circle["position"][0] += circle["velocity"][0]
            circle["position"][1] += circle["velocity"][1]

            # Draw the green circle
            pygame.draw.circle(self.surface, self.color, (int(circle["position"][0] - screen_position[0]), int(circle["position"][1] - screen_position[1])), self.radius)

            # If the green circle moves off-screen, remove it
            if circle["position"][0] < 0 or circle["position"][0] > self.surface.get_width() or \
                    circle["position"][1] < 0 or circle["position"][1] > self.surface.get_height():
                self.green_circles.remove(circle)

    def shoot(self, player_position):
        # Calculate the direction towards the mouse position
        mouse_pos = pygame.mouse.get_pos()
        direction = (mouse_pos[0] - player_position[0], mouse_pos[1] - player_position[1])
        # Normalize direction vector
        magnitude = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        if magnitude != 0:
            direction = (direction[0] / magnitude, direction[1] / magnitude)
        # Set initial velocity based on direction
        velocity = (direction[0] * self.speed, direction[1] * self.speed)
        # Add the green circle to the list with its initial position and velocity
        self.green_circles.append({"position": list(player_position), "velocity": list(velocity)})

    def run(self, player_position, screen_position):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.shoot(player_position)
        self.draw()
        self.update(screen_position)

