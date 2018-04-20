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

inventory = [100,100,100,0,0,0]
#           Wood,Stone,Food,Copper,Tin,Iron

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

COLORS = [(46, 164, 223), (180,160,140), (82, 127, 25), (53, 76, 25), (230, 230, 230)]
LABELS = ["Water", "Sand", "Grass", "Forest", "Mountain"]

SelectImage = pygame.image.load("SelectionCursor.png")

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
        player.PrintResource()

    def RightClick():
        
        mouseX, mouseY = pygame.mouse.get_pos()
        OnScreenRender()
        pygame.draw.rect(screen,(100,100,100),(int(mouseX),int(mouseY),30,50))
        pygame.draw.rect(screen,(255,50,50),(int(mouseX)+25,int(mouseY),5,5))
        
        #This Is Broken

class player():
    def __init__():
        print("")
        

    def PrintResource():
        I = inventory
        WoodText = font.render('Wood : ' + str(int(I[0] )),True,(255,255,255))
        StoneText = font.render('Stone : ' + str(int(I[1])),True,(255,255,255))
        FoodText = font.render('Food : ' + str(int(I[2] )),True,(255,255,255))
        CopperText = font.render('Copper : ' + str(int(I[3] )),True,(255,255,255))
        TinText = font.render('Tin : ' + str(int(I[4] )),True,(255,255,255))
        IronText = font.render('Iron : ' + str(int(I[5])),True,(255,255,255))
        #actually printing...
        screen.blit(WoodText,(1015,10))
        screen.blit(StoneText,(1015,30))
        screen.blit(FoodText,(1015,50))
        screen.blit(CopperText,(1015,70))
        screen.blit(TinText,(1015,90))
        screen.blit(IronText,(1015,110))

def OnScreenRender():
    screen.fill((0,0,0))
    GUI.Render()
    mouseX, mouseY = pygame.mouse.get_pos()
    X = int(mouseX/10)
    Y = int(mouseY/10)
    XText = font.render('X : ' + str(int(mouseX / 10 )),True,(255,255,255)) # Writes X Position in tile Form
    YText = font.render('Y : ' + str(int(mouseY / 10 )),True,(255,255,255)) # Writes Y Position in tile Form
    focusX = int(mouseX / 10)
    focusY = int(mouseY / 10)
    print(oreGEN[mouseX + mouseY])
    screen.blit(XText,(1220,10))
    screen.blit(YText,(1220,30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print (event.button)
            if event.button == 3:
                clicked = True
                GUI.RightClick()

    #pygame.draw.rect(screen, (0, 0, 0),  (0, 0, focusX, focusY))
    renderLand()
    clock.tick(60)
    screen.blit(SelectImage,(X *10,Y *10))
    pygame.display.update()
    
init()
player.__init__()
screen = pygame.display.set_mode((winWidth, winHeight))
done = False
while not done:
                             
    OnScreenRender()
                
    

