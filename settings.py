import pygame.time
class setting():

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.clock = pygame.time.Clock()
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0,255,00)
        self.green_fn = (0 , 255 , 0)
        self.screen = (800, 600)
        self.surface = pygame.display.set_mode(self.screen)

    def update(self):
        pygame.display.update()
        self.clock.tick(60)
        fps = self.clock.get_fps()
        #print(f"Current FPS: {fps:.2f}")
