import pygame
from setting import *
from SPRITETYPE import *
from Emotion import *

class Factory(pygame.sprite.Sprite):
    TURN = 3
    color = PURPLE
    def __init__(self, game, x1, y1, x2, y2, modifier = 0):
        super().__init__()
        self.game = game
        self.x = 0
        self.y = 0
        self.color = PURPLE
        self.image = None
        self.rect = None
        self.otherSquare = None
        self.modifier = modifier
        self.turn = 0
        self.type = SPRITETYPE.FACTORY
        self.emotion = Emotion.NORMAL
        self.pattern = 0 # 0 horizontal, 1 vertical

        if y1 != y2 and x1 != x2:
            return None

        elif y1 == y2:
            self.y = y1
            self.image = pygame.Surface((2 * TILESIZE, TILESIZE))
            self.pattern = 0

            #save the larger of the two as default x
            if x1 - x2 != -1 and x1 - x2 != 1:
                return None
            elif x1 - x2 == -1:
                self.x = x2
                self.rect = self.image.get_rect(center=((x2 * TILESIZE, (y1 + 0.5) * TILESIZE)))
                self.otherSquare = (x1, y1)
            elif x1 - x2 == 1:
                self.x = x1
                self.rect = self.image.get_rect(center=((x1 * TILESIZE, (y1 + 0.5) * TILESIZE)))
                self.otherSquare = (x2, y1)

        elif x1 == x2:
            self.x = x1
            self.image = pygame.Surface((TILESIZE, 2 * TILESIZE))
            self.pattern = 1

            if y1 - y2 != -1 and y1 - y2 != 1:
                return None
            elif y1 - y2 == -1:
                self.y = y2
                self.rect = self.image.get_rect(center=((x1 + 0.5) * TILESIZE, y2 * TILESIZE))
                self.otherSquare = (x1, y1)
            elif y1 - y2 == 1:
                self.y = y1
                self.rect = self.image.get_rect(center=((x1 + 0.5) * TILESIZE, y1 * TILESIZE))
                self.otherSquare = (x1, y2)

        self.image.fill(WHITE)


        if self.turn == Factory.TURN + self.modifier:
            self.completeBuilding()


    def nextTurn(self):
        self.turn += 1
        if self.turn == Factory.TURN + self.modifier:
            self.completeBuilding()
            return True
        return False

    def completeBuilding(self):
       # source : "https://icons8.com/icons/set/manufacturing" > Manufacturing
        picture = None
        if self.otherSquare[1] == self.y:
            picture = pygame.image.load("icons8-manufacturing-96.png")
            self.image = pygame.transform.scale(picture, (64, 32))
        else:
            picture = pygame.image.load("icons8-manufacturing-96vertical.png")
            self.image = pygame.transform.scale(picture, (32, 64))
        self.game.factoryCount += 1