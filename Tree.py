import pygame
from setting import *
from SPRITETYPE import *

class Tree(pygame.sprite.Sprite):
    TURN = 1
    color = GREEN
    def __init__(self, game, x, y, modifier=0):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y

        self.type = SPRITETYPE.TREE
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=((x + 0.5) * TILESIZE, (y + 0.5) * TILESIZE))
        self.turn = 0
        self.modifier = modifier

        if self.turn == Tree.TURN + self.modifier:
            self.completeBuilding()
        # self.endTurn = game.currentTurn + Tree.TURN

    def nextTurn(self):
        self.turn += 1
        if self.turn == Tree.TURN + self.modifier:
            self.completeBuilding()
            return True
        return False

    def completeBuilding(self):
        # source : "https://icons8.com/icons/set/tree--v1"
        picture = pygame.image.load("icons8-tree-96.png")
        self.image = pygame.transform.scale(picture, (32, 32))
        self.game.treeCount += 1
