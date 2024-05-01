import pygame.time
import random
class setting():

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.clock = pygame.time.Clock()
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.grey = (47, 47, 47)
        self.yellow = (255, 255, 0)
        self.rand_color = self.random_color()
        self.screen = (self.screen_width, self.screen_height)
        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.ability = ["Speed", "Size", "Health", "Shield"]
        self.normal_shot_cooldown = 500  # 0.5 second in milliseconds
        self.big_shot_cooldown = 3000  # 3 seconds in milliseconds
        self.ability_duration = 10000  # 10 seconds in milliseconds
        self.hit_damage = {"normal shot": 3, "big shot": 5, "coll": 3}
        self.hit_type = ("normal shot", "big shot", "coll")


    def random_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        if red == 255 and green == 255 and blue == 255:
            return self.random_color
        return red, green, blue  # Return the tuple representing the RGB color



    def update(self):
        pygame.display.update()
        self.clock.tick(60)
        fps = self.clock.get_fps()
        #print(f"Current FPS: {fps:.2f}")
