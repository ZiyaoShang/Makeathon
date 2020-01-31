import pygame
from setting import *
from SPRITETYPE import *

class House(pygame.sprite.Sprite):
    TURN = 2
    color = RED
    def __init__(self, game, x, y, modifier=0):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.k = 4000
        self.turn = 0

        self.type = SPRITETYPE.HOUSE
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=((x + 0.5) * TILESIZE, (y + 0.5) * TILESIZE))
        self.modifier = modifier


        if self.turn == House.TURN + self.modifier:
            self.completeBuilding()
        # color are all white when first built, when the turn has come,
        # change the color into RED and take in the values.

    def nextTurn(self):
        self.turn += 1
        if self.turn == House.TURN + self.modifier:
            self.completeBuilding()
            return True
        return False

    def completeBuilding(self):
        self.image.fill(House.color)
        self.game.houseCount += 1