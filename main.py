import pygame
import time
from noise import pnoise2
from random import randint
pygame.init()
pygame.font.init()
done = False


# Important Variables
winWidth = 1280
winHeight = 720
clock = pygame.time.Clock()
screen = pygame.display.set_mode((winWidth, winHeight))
font = pygame.font.SysFont('Times New Roman MS',30)

global mult
MaxX = 100 # Max X
MaxY = 100 # Max Y
size = MaxX * MaxY
tileSize = 10
focusSize = 10

focusX = 0
focusY = 0

land = []
oreGEN = []

gridSize = 0

# Constants
WATER = 0
SAND = 1
GRASS = 2
FOREST = 3
MOUNTAIN = 4

COLORS = [(46, 164, 223), (200,180,160), (82, 127, 25), (53, 76, 25), (230, 230, 230)]
LABELS = ["Water", "Sand", "Grass", "Forest", "Mountain"]

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
    mult = 0.06
    oremult = 0.5
    offX = randint(-5000000, 5000000)
    offY = randint(-5000000, 5000000)
    CopperX = randint(0, 5000)
    CopperY = randint(0, 5000)
    TinX = randint(0, 5000)
    TinY = randint(0, 5000)
    IronX = randint(0, 5000)
    IronY = randint(0, 5000)
    for i in range(MaxX*MaxY):
        X, Y = singleToDouble(i)
        noise = pnoise2((X + offX)*mult, (Y + offY)*mult)
        Coppernoise = (pnoise2((X +CopperX)*oremult,(Y + CopperY)* oremult)+1) * 5
        Tinnoise = (pnoise2((X +TinX)*oremult,(Y + TinY)* oremult)+ 1) * 3
        Ironnoise = (pnoise2((X +IronX)*oremult,(Y + IronY)* oremult)+1) * 1.5
        val = (noise+1)*50
        TYPE = 0

        if val > 80:
            TYPE = MOUNTAIN
        elif val > 60:
            TYPE = FOREST
        elif val > 40:
            TYPE = GRASS
        elif val > 35:
            TYPE = SAND
        else:
            TYPE = WATER

        land.append(Tile(TYPE))
        oreGEN.append((Coppernoise, Tinnoise, Ironnoise))


def renderLand():

    for i in range(MaxX*MaxY):
        X, Y = singleToDouble(i)
        tile = land[i]
        focusIndex = doubleToSingle(focusX, focusY)
        pygame.draw.rect(screen, tile.color, (X*tileSize, Y*tileSize, tileSize-gridSize, tileSize-gridSize))

class GUI(): # Draws GUI, Very simple right now
    def Render():
        pygame.draw.rect(screen, (100,100,100), (1000,0, 300, 1000))
        pygame.draw.rect(screen, (150,150,150), (1000,0, 10, 1000))

class player():
    def __init__():
        inventory = [100,100,100,0,0,0]
        #           Wood,Stone,Food,Copper,Tin,Iron
              
init()
screen = pygame.display.set_mode((winWidth, winHeight))
done = False
while not done:
    screen.fill((0,0,0))
    GUI.Render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            exit()
    mouseX, mouseY = pygame.mouse.get_pos()
    XText = font.render('X : ' + str(int(mouseX / 20 )),True,(255,255,255)) # Writes X Position in tile Form
    YText = font.render('Y : ' + str(int(mouseY / 20 )),True,(255,255,255)) # Writes Y Position in tile Form

    focusX = int(mouseX / 20)
    focusY = int(mouseY / 20)
    print(oreGEN[mouseX + mouseY])
    screen.blit(XText,(1050,100))
    screen.blit(YText,(1125,100))

    #pygame.draw.rect(screen, (0, 0, 0),  (0, 0, focusX, focusY))
    renderLand()
    clock.tick(60)
    pygame.display.update()

