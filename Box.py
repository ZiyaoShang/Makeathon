import pygame
from setting import *
from SPRITETYPE import *

class Box(pygame.sprite.Sprite):
    def __init__(self, game, screen, x=12, y=12):
        self.game = game
        self.x = x
        self.y = y
        self.screen = screen
        # self.image = pygame.Surface((TILESIZE, TILESIZE))
        # self.rect = self.image.get_rect(center=((x + 0.5) * TILESIZE, (y + 0.5) * TILESIZE))

    def __drawBox(self):
        pygame.draw.line(self.screen, YELLOW, (self.x * TILESIZE, self.y * TILESIZE), ((self.x + 1) * TILESIZE, self.y * TILESIZE), 5)
        pygame.draw.line(self.screen, YELLOW, ((self.x + 1) * TILESIZE, self.y * TILESIZE), ((self.x + 1) * TILESIZE, (self.y + 1) * TILESIZE), 5)
        pygame.draw.line(self.screen, YELLOW, ((self.x + 1) * TILESIZE, (self.y + 1) * TILESIZE), (self.x * TILESIZE, (self.y + 1) * TILESIZE), 5)
        pygame.draw.line(self.screen, YELLOW, (self.x * TILESIZE, (self.y + 1) * TILESIZE), (self.x * TILESIZE, self.y * TILESIZE), 5)

    def move(self, dx=0, dy=0):
        if(self.x + dx >= SCREENWIDTHBYTILES or self.x + dx < 0 or self.y + dy >= SCREENHEIGHTBYTILES or self.y + dy < 0):
            return
        self.x += dx
        self.y += dy
        # if pygame.sprite.spritecollideany(self, self.game.allSea, collided=None):
        #     self.x -= dx
        #     self.y -= dy
        checkSea = self.game.spriteDict.get((self.x, self.y))
        if checkSea:
            if checkSea.type == SPRITETYPE.SEA:
                self.x -= dx
                self.y -= dy

        self.__drawBox()
