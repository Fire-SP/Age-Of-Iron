import pygame
from noise import pnoise2
from random import randint
pygame.init()
done = False


# Important Variables
winWidth = 1280
winHeight = 720
screen = pygame.display.set_mode((winWidth, winHeight))

global mult
MaxX = 200 # Max X
MaxY = 200 # Max Y
size = MaxX * MaxY
tileSize = 5
focusSize = 5

focusX = 0
focusY = 0

land = []

gridSize = 0

# Constants
WATER = 0
SAND = 1
GRASS = 2
FORREST = 3
MOUNTAIN = 4

COLORS = [(46, 164, 223), (200,180,160), (82, 127, 25), (53, 76, 25), (230, 230, 230)]
LABELS = ["Water", "Sand", "Grass", "Forrest", "Mountain"]

# Helper functions
def doubleToSingle(x, y):
    return (MaxX * y) + x

def singleToDouble(i):
    x = i % MaxX
    y = int(i / MaxY)
    return (x, y)


class Tile():
    def __init__(self, type):
        self.type = type
        self.color = COLORS[self.type]
        self.label = LABELS[self.type]
        self.hasCopper = False
        self.hasTin = False
        self.hasIron = False

def init():
    # Init the land
    mult = 0.03
    offX = randint(-5000000, 5000000)
    offY = randint(-5000000, 5000000)
    CopperX = randint(-5000, 5000)
    CopperY = randint(-5000, 5000)
    TinX = randint(-5000, 5000)
    TinY = randint(-5000, 5000)
    IronX = randint(-5000, 5000)
    IronY = randint(-5000, 5000)
    for i in range(MaxX*MaxY):
        X, Y = singleToDouble(i)
        noise = pnoise2((X + offX)*mult, (Y + offY)*mult)
        Coppernoise = pnoise2((X +CopperX)*mult,(Y + CopperY)* mult)
        Tinnoise = pnoise2((X +CopperX)*mult,(Y + CopperY)* mult)
        Ironnoise = pnoise2((X +CopperX)*mult,(Y + CopperY)* mult)
        val = (noise+1)*50
        TYPE = 0

        if val > 80:
            TYPE = MOUNTAIN
        elif val > 60:
            TYPE = FORREST
        elif val > 40:
            TYPE = GRASS
        elif val > 35:
            TYPE = SAND
        else:
            TYPE = WATER

        land.append(Tile(TYPE))



    

def renderLand():

    for i in range(MaxX*MaxY):
        X, Y = singleToDouble(i)
        tile = land[i]
        focusIndex = doubleToSingle(focusX, focusY)
        pygame.draw.rect(screen, tile.color, (X*tileSize, Y*tileSize, tileSize-gridSize, tileSize-gridSize))


init()
screen = pygame.display.set_mode((winWidth, winHeight))
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    mouseX, mouseY = pygame.mouse.get_pos()

    focusX = int(mouseX / 20)
    focusY = int(mouseY / 20)
    print(focusX, focusY)

    #pygame.draw.rect(screen, (0, 0, 0),  (0, 0, focusX, focusY))
    renderLand()
    pygame.display.update()
