import pygame
from setting import *

class Box:
    def __init__(self, screen, x=12, y=12):
        self.x = x
        self.y = y
        self.screen = screen


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
        self.__drawBox()
