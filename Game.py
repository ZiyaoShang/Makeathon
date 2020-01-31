
from setting import *

import pygame
from Box import *
from Tree import *
from Sea import *
from Factory import *
from House import *
from SPRITETYPE import *

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
        self.allSprites = pygame.sprite.Group()

        self.population = 4000
        self.seaLevel = 0
        self.resource = 2700
        self.carryingCapacity = 4100

        self.currentTurn = 0
        # counter of Sprites
        self.treeCount = 200
        self.houseCount = 5
        self.factoryCount = 1

        self.allSea = pygame.sprite.Group()
        self.allFactories = pygame.sprite.Group()
        self.allTrees = pygame.sprite.Group()
        self.allHouses = pygame.sprite.Group()

        self.spriteDict = {}
        self.constructionList = []
        self.running = True
        pygame.key.set_repeat(300, 100)
        # self.initializeTerrain()
        self.box = Box(self, self.screen)

        self.seaX = 0
        self.seaY = 10

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

                # testing sea over here:
                if keys[K_s]:
                    sea = Sea(self, self.box.x, self.box.y)
                    self.addSprite(self.spriteDict, self.allSprites, self.allSea, sea)

                if keys[K_RETURN]:
                    self.newTurn()

    def newTurn(self):

        # add one turn for each constructing sprite,
        # they will change color when the construction is finished
        for sprite in self.spriteDict:
            pass
        try:
            checkSpritesCompletion = lambda sprite: not sprite.nextTurn()
            self.constructionList = list(filter(checkSpritesCompletion, self.constructionList))
        except():
            pass
        print(len(self.constructionList))

        numHouses = self.houseCount
        numFactories = self.factoryCount
        numTrees = self.treeCount

        self.currentTurn += 1
        self.resource = numFactories * 300 + STARTRESOURCES - self.population / 20
        # update capacity
        if self.resource > numHouses * 800:
            self.carryingCapacity = numHouses * 800
        else:
            self.carryingCapacity = self.resource

        # update population (r max = 0.5)

        self.population += 0.5 * (self.carryingCapacity - self.population) / self.carryingCapacity * self.population

        # update seaLevel
        self.seaLevel += 1 + numTrees * 0.05
        self.currentTurn += 1
        print("seaLevel " + str(self.seaLevel) + "\n" + "population " + str(self.population) + "\n" + "capacity " + str(self.carryingCapacity)
              + "\n" + "resources " + str(self.resource) + "\n\n")
        # self.initializeTerrain()

        for x in range(0, int(1 + numTrees * 0.05)):
            self.seaRise()

    def update(self):
        self.allSprites.update()
        self.allTrees.update()
        self.allFactories.update()
        self.allHouses.update()

    def draw(self):
        self.screen.fill(DARKGREY)
        self.allSprites.draw(self.screen)
        self.draw_grid()
        self.box.move()
        pygame.display.flip()


    def draw_grid(self):
        # Vertical Line
        for x in range(0, SCREENWIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, SCREENHEIGHT))

        # Horizontal Line
        for y in range(0, SCREENHEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (SCREENWIDTH, y))

    def addSprite(self, myDict, myGroup, specificGroup, sprite):
        x = sprite.x
        y = sprite.y
        checkIfOccupied = myDict.get((x, y))
        if not checkIfOccupied:
            self.allSprites.add(sprite)
            myGroup.add(sprite)
            specificGroup.add(sprite)
            myDict[(x, y)] = sprite
            if sprite.type == SPRITETYPE.SEA:
                return
            self.constructionList.append(sprite)
            # print("addSprite()" + str(len(self.constructionList)))

    def delSprite(self, myDict):
        x = self.box.x
        y = self.box.y
        checkIfOccupied = myDict.get((x, y))
        if checkIfOccupied:
            if myDict[(x, y)].type == SPRITETYPE.SEA:
                return
            del myDict[(x, y)]
            try:
                ## you might delete the left part
                other = checkIfOccupied.otherSquare
                del myDict[other]
            except:
                pass
            checkIfOccupied.kill()


    # edited
    def initializeTerrain(self):
        # initDict contains the initial terrain, and has the same structure of "myDict",
        # but the values are int instead of booleans
        # e.g: 1=water, 2=building, 3=tree, 4=land...
        # We will be needing a dictionary for every kind of terrain, or we may need to change the value type of myDict
        # into integers (and modify the )
        initTerrin = []
        print("initialize")
        with open("Terrain.txt", "rt") as File:
            line = File.readline()
            while line:
                initTerrin.append(line)
                line = File.readline()
            File.close()
        # print(initTerrin)
        for x in range(0, SCREENWIDTHBYTILES):
            for y in range(0, SCREENHEIGHTBYTILES):
                type = int(initTerrin[y][x])
                # print(SPRITETYPE.SEA.value)
                if type == SPRITETYPE.TREE.value:
                    tree = Tree(self, x, y, -1)
                    self.addSprite(self.spriteDict, self.allSprites, self.allTrees, tree)
                    # self.Treedict[(x, y)] = tree
                elif type == SPRITETYPE.SEA.value:
                    sea = Sea(self, x, y)
                    self.addSprite(self.spriteDict, self.allSprites, self.allSea, sea)
                    # self.Seadict[(x, y)] = sea
                    # print("sea")
                elif type == SPRITETYPE.FACTORY.value:
                    factory = Factory(self, x - 1, y, x, y, -3)
                    self.spriteDict[(self.box.x - 1, self.box.y)] = factory
                    self.addSprite(self.spriteDict, self.allSprites, self.allFactories, factory)
                    # self.facTorydict[(x, y)] = factory
                elif type == SPRITETYPE.HOUSE.value:
                    house = House(self, x, y, -2)
                    self.addSprite(self.spriteDict, self.allSprites, self.allHouses, house)
            try:
                checkSpritesCompletion = lambda sprite: not sprite.nextTurn()
                self.constructionList = list(filter(checkSpritesCompletion, self.constructionList))
            except():
                pass
                # self.dict[(x, y)] = house

    def seaRise(self):
        for i in range(0, 2):
            # delete without checking occupation
            x = self.seaX
            y = self.seaY
            # temp = self.spriteDict[(x, y)]
            # if not temp:
            #     del self.spriteDict[(x, y)]
            #     try:
            #         checkIfOccupied = self.spriteDict.get((x, y))
            #         ## you might delete the left part
            #         other = checkIfOccupied.otherSquare
            #         del self.spriteDict[other]
            #     except:
            #         pass
            #     checkIfOccupied.kill()
            checkIfOccupied = self.spriteDict.get((x, y))
            if checkIfOccupied:
                # if self.spriteDict[(x, y)].type == SPRITETYPE.SEA:
                #     return
                del self.spriteDict[(x, y)]
                try:
                    ## you might delete the left part
                    other = checkIfOccupied.otherSquare
                    del self.spriteDict[other]
                except:
                    pass
                checkIfOccupied.kill()

            # add sea
            sea = Sea(self, x, y)
            self.addSprite(self.spriteDict, self.allSprites, self.allSea, sea)


            # move x, y
            if self.seaX == 29:
                self.seaX = 0
                self.seaY += 1
            else:
                self.seaX += 1
            pass





game = Game()
game.initializeTerrain()
game.run()
pygame.quit()
