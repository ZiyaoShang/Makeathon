
from setting import *

import pygame
from Box import *
from Tree import *
from Water import *
from Factory import *
from House import *


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
        self.allSprites = pygame.sprite.Group()

        self.population = 4000
        self.seaLevel = 0
        self.resource = 2700
        self.carryingCapacity = 4100

        self.allWater = {}
        self.allFactories = pygame.sprite.Group()
        self.allTrees = pygame.sprite.Group()
        self.allHouses = pygame.sprite.Group()

        self.spriteDict = {}
        self.running = True
        self.box = Box(self.screen)
        pygame.key.set_repeat(300, 100)


    # Game loop
    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                    self.box.move(-1, 0)
                if keys[K_RIGHT]:
                    self.box.move(1, 0)
                if keys[K_UP]:
                    self.box.move(0, -1)
                if keys[K_DOWN]:
                    self.box.move(0, 1)
                if keys[K_RETURN] and keys[K_RSHIFT]:
                    print(self.box.x, self.box.y)
                    # BUTTONS APPEAR

                # USE KEYS TO DISPLAY TREES T -> Create Trees, D -> Delete Trees
                if keys[K_t]:
                    tree = Tree(self, self.box.x, self.box.y)
                    self.addSprite(self.spriteDict, self.allSprites, self.allTrees, tree)

                # factory two-tile resolution!!!
                if keys[K_f]:
                    factory = Factory(self, self.box.x, self.box.y, self.box.x - 1, self.box.y)
                    self.spriteDict[(self.box.x - 1, self.box.y)] = factory
                    self.addSprite(self.spriteDict, self.allSprites, self.allFactories, factory)
                    # self.allFactories.add(factory)

                if keys[K_d]:
                    self.delSprite(self.spriteDict)

                if keys[K_h]:
                    house = House(self, self.box.x, self.box.y)
                    self.addSprite(self.spriteDict, self.allSprites, self.allHouses, house)
                    print((len(self.allSprites), len(self.allHouses)))

                if keys[K_RETURN]:
                    self.newTurn()

    def newTurn(self):

        # add one turn for each constructing sprite,
        # they will change color when the construction is finished
        for sprite in self.spriteDict:

            pass
        numHouses = len(self.allHouses)
        numFactories = len(self.allFactories)
        numTrees = len(self.allTrees)

        # update resources (remove +1)
        self.resource = (numFactories + 1) * 300 + STARTRESOURCES - self.population / 20
        print(self.resource)
        # update capacity
        if self.resource > numHouses * 800:
            #remove + 5
            self.carryingCapacity = (numHouses + 5) * 800
        else:
            self.carryingCapacity = self.resource

        # update population (r max = 0.5)

        self.population += 0.5 * (self.carryingCapacity - self.population) / self.carryingCapacity * self.population

        # update seaLevel
        self.seaLevel += 1 + numTrees * 0.05

        print("seaLevel " + str(self.seaLevel) + "\n" + "population " + str(self.population) + "\n" + "capacity " + str(self.carryingCapacity)
              + "\n" + "resources " + str(self.resource) + "\n\n")

    def update(self):
        self.allSprites.update()
        self.allTrees.update()
        self.allFactories.update()
        self.allHouses.update()

    def draw(self):
        self.screen.fill(DARKGREY)
        self.draw_grid()
        self.box.move()
        self.allSprites.draw(self.screen)
        pygame.display.flip()


    def draw_grid(self):
        # Vertical Line
        for x in range(0, SCREENWIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, SCREENHEIGHT))

        # Horizontal Line
        for y in range(0, SCREENHEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (SCREENWIDTH, y))

    def addSprite(self, myDict, myGroup, specificGroup,sprite):
        x = self.box.x
        y = self.box.y
        checkIfOccupied = myDict.get((x, y))
        if not checkIfOccupied:
            self.allSprites.add(sprite)
            myGroup.add(sprite)
            specificGroup.add(sprite)
            myDict[(x, y)] = sprite

    def delSprite(self, myDict):
        x = self.box.x
        y = self.box.y
        checkIfOccupied = myDict.get((x, y))
        if (checkIfOccupied):
            del myDict[(x, y)]
            try:
                ## you might delete the left part
                other = checkIfOccupied.otherSquare
                del myDict[other]
            except:
                pass
            checkIfOccupied.kill()


    # edited
    # def initializeTerrain(self, initDict):
    #     # initDict contains the initial terrain, and has the same structure of "myDict",
    #     # but the values are int instead of booleans
    #     # e.g: 1=water, 2=building, 3=tree, 4=land...
    #     # We will be needing a dictionary for every kind of terrain, or we may need to change the value type of myDict
    #     # into integers (and modify the )
    #     for x in range(0, SCREENWIDTH, TILESIZE):
    #         for y in range(0, SCREENHEIGHT, TILESIZE):
    #             type = initDict.get(x, y)
    #             if type == 1:
    #                 tree = Tree(self, x, y)
    #                 self.addSprite(self.treeDict, self.allTrees, tree)
    #                 self.allSprites.add(tree)
    #                 self.allTrees.add(tree)
    #                 self.Treedict[(x, y)] = tree
    #
    #              pass
    # edited

game = Game()
game.run()
pygame.quit()

