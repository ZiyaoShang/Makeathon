
from setting import *

import pygame
from Box import *
from Tree import *
from Sea import *
from Factory import *
from House import *
from SPRITETYPE import *
from Emotion import *

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
        self.allSprites = pygame.sprite.Group()

        self.population = 4000
        self.seaLevel = 0
        self.seaIncrement = 1
        self.resource = 2700
        self.carryingCapacity = 4100
        self.emotion = Emotion.NORMAL

        self.currentTurn = 0
        # counter of Sprites
        self.startTreeCount = 0
        self.treeCount = 0
        self.houseCount = 0
        self.factoryCount = 0

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
        self.seaY = 0

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
                    tree = Tree(self, self.box.x, self.box.y, self.emotion.value)
                    self.addSprite(self.spriteDict, self.allSprites, self.allTrees, tree)

                # factory two-tile resolution!!!
                if keys[K_f]:
                    factory = Factory(self, self.box.x, self.box.y, self.box.x - 1, self.box.y, self.emotion.value)
                    self.spriteDict[(self.box.x - 1, self.box.y)] = factory
                    print("sprite")
                    self.addSprite(self.spriteDict, self.allSprites, self.allFactories, factory)
                    # self.allFactories.add(factory)

                if keys[K_d]:
                    self.delSprite(self.spriteDict)

                if keys[K_h]:
                    house = House(self, self.box.x, self.box.y, self.emotion.value)
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


        self.currentTurn += 1
        # self.resource = numFactories * 300 + STARTRESOURCES - self.population / 20
        self.resource += numFactories * 200 - self.population / 5
        # update capacity
        if self.resource > numHouses * 400:
            self.carryingCapacity = numHouses * 400
        else:
            self.carryingCapacity = self.resource

            ## manually decrease carrying capacity
        if 0 < self.carryingCapacity - self.population <= 10:
            self.carryingCapacity *= 0.9

        # update population (r max = 0.5)

        self.population += 0.8 * (self.carryingCapacity - self.population) / self.carryingCapacity * self.population

        # update seaLevel
        self.seaIncrement = (self.startTreeCount - self.treeCount) * 0.03
        self.seaIncrement = self.seaIncrement if self.seaIncrement >= 0 else 0
        self.seaLevel += self.seaIncrement

        # self.initializeTerrain()

        for x in range(0, int(self.seaIncrement + 1)):
            # print("drown")
            self.seaRise()

        if self.population < 1100:
            self.emotion = Emotion.LOW
            self.resource *= 0.8
        else:
            self.emotion = Emotion.NORMAL


        print("seaLevel " + str(self.seaLevel) + "\n" + "population " + str(self.population) + "\n" + "capacity " + str(
            self.carryingCapacity)
              + "\n" + "resources " + str(self.resource) + " " + str(numFactories) + "\n Emotion: " + str(self.emotion) + "\n\n")

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
        # print(checkIfOccupied)
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
            elif myDict[(x, y)].type == SPRITETYPE.TREE:
                self.treeCount -= 1
            del myDict[(x, y)]
            # print("delete")
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
        # print("initialize")
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
                    self.seaX =\
                        x
                    self.seaY = y
                    # self.Seadict[(x, y)] = sea
                    # print("sea")
                elif type == SPRITETYPE.FACTORY.value:
                    factory = Factory(self, x - 1, y, x, y, -3)
                    self.addSprite(self.spriteDict, self.allSprites, self.allFactories, factory)
                    self.spriteDict[(x - 1, y)] = factory
                    # self.factoryCount += 1
                    # self.facTorydict[(x, y)] = factory
                elif type == SPRITETYPE.HOUSE.value:
                    house = House(self, x, y, -2)
                    self.addSprite(self.spriteDict, self.allSprites, self.allHouses, house)
                    # self.houseCount += 1
            try:
                checkSpritesCompletion = lambda sprite: not sprite.nextTurn()
                self.constructionList = list(filter(checkSpritesCompletion, self.constructionList))
            except():
                pass
                # self.dict[(x, y)] = house
            # print(self.treeCount)
        self.startTreeCount = self.treeCount

            
    def seaRise(self):
        rise = 3
        if self.seaIncrement < 1/3:
            rise = 1
        elif self.seaIncrement < 2/3:
            rise = 2
        for i in range(0, rise):
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
                    if checkIfOccupied.type == SPRITETYPE.FACTORY:
                        # print("Sea: " + str((self.seaX, self.seaY)))
                        # print("deleteFactory")
                        other = checkIfOccupied.otherSquare
                        del self.spriteDict[other]
                        self.factoryCount -= 1
                    elif checkIfOccupied.type == SPRITETYPE.HOUSE:
                        self.houseCount -= 1
                    elif checkIfOccupied.type == SPRITETYPE.TREE:
                        self.treeCount -= 1
                except:
                    pass
                checkIfOccupied.kill()

            # add sea
            sea = Sea(self, x, y)
            self.addSprite(self.spriteDict, self.allSprites, self.allSea, sea)


            # move x, y
            if self.seaX == SCREENWIDTHBYTILES - 1:
                self.seaX = 0
                self.seaY += 1
            else:
                self.seaX += 1

            if self.seaX < SCREENWIDTHBYTILES and self.seaY < SCREENHEIGHTBYTILES:
                self.box.moveTo(self.seaX + 1, self.seaY + 1)
            elif self.seaX >= SCREENHEIGHTBYTILES:
                self.box.moveTo(self.seaX, self.seaY + 1)
            else:
                self.box.moveTo(self.seaX + 1, self.seaY)





game = Game()
game.initializeTerrain()
game.run()
pygame.quit()
