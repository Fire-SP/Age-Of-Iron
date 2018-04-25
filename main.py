import pygame
import time
from noise import pnoise2
from random import randint
from PIL import Image, ImageDraw
pygame.init()
pygame.font.init()
done = False


# Important Variables
winWidth = 1280
winHeight = 720
clock = pygame.time.Clock()
screen = pygame.display.set_mode((winWidth, winHeight))
font = pygame.font.SysFont('Times New Roman MS',30)
# test = pygame.image.load("IMAGE.png")

global mult
MaxX = 100 # Max X
MaxY = 100 # Max Y
size = MaxX * MaxY
tileSize = 10
focusSize = 10

global clicked
clicked = False

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

SelectImage = pygame.image.load("img/Selection.png")
landImg = pygame.image.load("img/Selection.png")
# Helper functions
def createImage():
    global landImg
    img = Image.new('RGB', (1000, 1000), "black")
    pixels = img.load()

    for i in range(100):
        for j in range(72):
            landIndex = doubleToSingle(i, j)
            for k in range(10):
                for l in range(10):
                    pixels[i*10+k, j*10+l] = land[landIndex].color
            #pixels[i*10,j*10] = land[landIndex].color
        # pixels[imgX,imgY] = land[landIndex].color
    img.save("img/Land.png", "PNG")
    landImg = pygame.image.load("img/Land.png")


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
        clicked = True
        mouseX, mouseY = pygame.mouse.get_pos()
        OldX = mouseX
        OldY = mouseY
        while clicked == True:
            OnScreenRender()
            pygame.draw.rect(screen,(100,100,100),(int(OldX),int(OldY),150,300))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        clicked = False


        #This Is Broken

class player():

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

def placeBuilding():
    mouseX, mouseY = pygame.mouse.get_pos()
    X = int(mouseX/10)
    Y = int(mouseY/10)

    CityCap = 0
    #Try to Place City Center
    if CityCap < 1:
        print("City Cap Passed. ")
        if inventory[0] > 75 and inventory[1] > 50 and inventory[2] > 50:
            print("Resource Check Passed. ")
            I = inventory
            I[0] -= 75
            I[1] -= 50
            I[2] -= 50

def OnScreenRender():
    screen.fill((0,0,0))
    GUI.Render()
    #Init Mouse Location
    mouseX, mouseY = pygame.mouse.get_pos()
    X = int(mouseX/10)
    Y = int(mouseY/10)

    #print(oreGEN[mouseX + mouseY])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print (event.button)
            if event.button == 3:
                global clicked
                clicked = True
                GUI.RightClick()
            if event.button == 2:
                placeBuilding()

    #pygame.draw.rect(screen, (0, 0, 0),  (0, 0, focusX, focusY))
    #renderLand()

    screen.blit(landImg,(0,0))
    clock.tick(60)
    screen.blit(SelectImage,(X *10,Y *10))

    ################## SIDE BAR STUFF #############################
    posText = font.render('['+str(X)+','+str(Y)+']',True,(255,255,255))
    screen.blit(posText,(1200,10))

    # Show land type
    landIndex = doubleToSingle(X, Y)
    landType = font.render(land[landIndex].label, True, (255, 255, 255))
    screen.blit(landType, (1100, 200))

init()
createImage()
screen = pygame.display.set_mode((winWidth, winHeight))
done = False
while not done:

    OnScreenRender()
    pygame.display.update()
