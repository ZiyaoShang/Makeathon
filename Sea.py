import pygame
from setting import *
from SPRITETYPE import *
class Sea(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y

        self.type = SPRITETYPE.SEA
        self.color = BLUE
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=((x + 0.5) * TILESIZE, (y + 0.5) * TILESIZE))

    # def nextTurn(self):
    #     self.turn += 1
    #     if self.turn == 1:
    #         self.completeBuilding()
    #         return True
    #     return False
    #
    # def completeBuilding(self):
    #     self.image.fill(Factory.color)
    #     self.game.factoryCount += 1