import pygame
from setting import *
from SPRITETYPE import *
class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y

        self.type = SPRITETYPE.WATER
        self.color = BLUE
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=((x + 0.5) * TILESIZE, (y + 0.5) * TILESIZE))
