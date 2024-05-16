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
        self.green2 = (31, 198, 0)
        self.green3 = (8, 144, 0)
        self.green4 = (10, 93, 0)
        self.blue = (0, 0, 255)
        self.grey = (47, 47, 47)
        self.yellow = (255, 255, 0)
        self.rand_color = self.random_color()
        self.screen = (self.screen_width, self.screen_height)
        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.ability = ["Speed", "Size", "Shield", "Full HP", "30 HP", "15 HP", "5 HP"]
        self.normal_shot_cooldown = 500  # 0.5 second in milliseconds
        self.big_shot_cooldown = 3000  # 3 seconds in milliseconds
        self.ultimate_shot_cooldown = 6000  # 1 minute in milliseconds
        self.ability_duration = 10000  # 10 seconds in milliseconds
        self.hit_damage = {"normal shot": 3, "big shot": 8, "ultimate shot": 60, "coll": 3}
        self.hit_type = ("normal shot", "big shot", "ultimate shot", "coll")
        self.fps = "60"
        self.noam = "pictures/noam.png", "pictures/small_noam.png"
        self.alon = "pictures/alon.png", "pictures/small_alon.png"
        self.lidor = "pictures/lidor.png", "pictures/small_lidor.png"
        self.kidan = "pictures/kidan.png", "pictures/small_kidan.png"
        self.rom = "pictures/rom.png", "pictures/small_rom.png"
        self.avishay = "pictures/avishay.png", "pictures/small_avishay.png"
        self.list_of_images = (pygame.image.load(self.noam[0]), pygame.image.load(self.alon[0]), pygame.image.load(self.lidor[0]),
                            pygame.image.load(self.kidan[0]), pygame.image.load(self.rom[0]), pygame.image.load(self.avishay[0]))
        self.list_of_small_images = (
            pygame.image.load(self.noam[1]), pygame.image.load(self.alon[1]), pygame.image.load(self.lidor[1]),
            pygame.image.load(self.kidan[1]), pygame.image.load(self.rom[1]), pygame.image.load(self.avishay[1]))


    def random_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        if red == 255 and green == 255 and blue == 255:
            return self.random_color
        return red, green, blue  # Return the tuple representing the RGB color

    def darw_fps(self):
        font = pygame.font.Font("Power Smash.ttf", 30)
        fps_surface = font.render(self.fps, True, (40, 158, 255))
        text_rect = fps_surface.get_rect()
        self.surface.blit(fps_surface, (0, 0))

    def update(self):
        pygame.display.update()
        self.clock.tick(60)
        self.fps = str(int(self.clock.get_fps()))

    def rand_image(self):
        images = {
            self.noam: 0,
            self.alon: 1,
            self.kidan: 2,
            self.lidor: 3,
            self.rom: 4,
            self.avishay: 5
        }
        selected_image = random.choice(list(images.keys()))
        image_number = images[selected_image]
        return pygame.image.load(selected_image[0]), image_number

