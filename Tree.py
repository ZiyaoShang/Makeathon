import pygame
from setting import *
from SPRITETYPE import *

class Tree(pygame.sprite.Sprite):
    TURN = 1
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y

        self.type = SPRITETYPE.TREE
        self.color = GREEN
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=((x + 0.5) * TILESIZE, (y + 0.5) * TILESIZE))
        self.score = 10



