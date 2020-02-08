import pygame
from setting import *
from SPRITETYPE import *
import math

class Sea(pygame.sprite.Sprite):
    tick = 0
    amplitude = 1.1
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y

        self.type = SPRITETYPE.SEA
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        picture = pygame.image.load("icons8-sea-waves-96.png")
        self.image = pygame.transform.scale(picture, (64, 64))
        self.offset = 0
        self.rect = None

        if y == 0:
            self.rect = self.image.get_rect(center=((x + 0.5) * TILESIZE, (y + 0.5) * TILESIZE))
            self.offset = Sea.amplitude * math.sin(2 * math.pi * self.x / 6)
            self.rect.move_ip(0, self.offset)
        if y != 0:
            reference = game.spriteDict[(x, 0)].rect.center[1]
            referenceDiff = reference - 0.5 * TILESIZE
            self.rect = self.image.get_rect(center=((x + 0.5) * TILESIZE, (y + 0.5) * TILESIZE + referenceDiff))


        # self.rect.move_ip(0, self.offset)


        # reference: "https://icons8.com/icons/set/sea-waves"



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

    def update(self):
        # if Sea.flag:
        self.offset = Sea.amplitude * math.sin(2 * math.pi * (self.x - 3 * Sea.tick) / 6)
        self.rect.move_ip(0, self.offset)


    @staticmethod
    def updateSeaTick():
        Sea.tick += 0.1

