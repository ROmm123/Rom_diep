import pygame
class HP():
    def __init__(self, x, y, halfbase, setting):
        self.HealthBar = pygame.Rect(x - halfbase, (y+halfbase+10), 2 * halfbase, 10)
        self.LifeColor = setting.green
        self.Damage = 0
        self.DamageBar = pygame.Rect(x - halfbase, (y+halfbase+10), 2*halfbase, self.Damage)
        self.DamageColor = setting.red
        self.ISAlive = True

