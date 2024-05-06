import pygame

class HP():
    def __init__(self, x, y, radius, setting, damage=None):
        self.HealthBar = pygame.Rect(x - radius, (y+radius+10), 2 * radius, 10)
        self.LifeColor = setting.green
        if damage is None:
            self.Damage = 0
        else:
            self.Damage = damage
        self.DamageBar = pygame.Rect(x - radius, (y+radius+10), 2*radius, self.Damage)
        self.DamageColor = setting.red
        self.ISAlive = True
        self.FullHP = True
