import pygame
from setting import *
from SPRITETYPE import *

class House(pygame.sprite.Sprite):
    TURN = 2
    def __init__(self, game, x, y, modifier=0):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.k = 4000
        self.turn = House.TURN + modifier

        self.type = SPRITETYPE.HOUSE
        self.color = RED
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=((x + 0.5) * TILESIZE, (y + 0.5) * TILESIZE))


        # color are all white when first built, when the turn has come,
        # change the color into RED and take in the values.