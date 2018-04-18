from noise import pnoise2
import pygame, random, time


"""
mult = 0.1

map = []

for i in range(50):
    for j in range(50):
        n = (pnoise2(i*mult, j*mult) + 1) * 127.5
        map.append(n)


print(map)
"""

ScreenHeight = 1000
ScreenWidth = 1200


black = (0, 0, 0)
sand = (200,180,160)
water = (46, 164, 223)
land = (82, 127, 25)
highland = (53, 76, 25)
desert = (237, 201, 175)


offsetX = random.randint(0, 50000)
offsetY = random.randint(0, 50000)




global ownedsquares
ownedsquares = 1

money = 0
maxmoney = 500

X = 20
Y = 20

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Times New Roman MS',30)
SelectImage = pygame.image.load("Select.png")
CoalVein = pygame.image.load("Coal Vein.png")
CopperVein = pygame.image.load("Copper Vein.png")
TinVein = pygame.image.load("Tin Vein.png")
IronVein = pygame.image.load("Iron Vein.png")
Display = pygame.display.set_mode((ScreenWidth,ScreenHeight))


class terrainGenerate():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.height = 0
        self.rowLength = 100
        self.terrain = []
        self.A = 0 #Choose Large part of list
        self.B = 0 #Choose subselections within list elements
        self.owner = 0
        self.loopcycle = 0
        self.generated = False
        self.enemygenerated = False
        self.materials = 0


    def landGen(self):
        for loop in range (0,2550):
            self.randomNum = random.randint(0,255)
            self.loopcycle += 1
            #self.height = random.randint(0,255)
            mult = 0.003
            self.height = (pnoise2((self.x+offsetX)*mult, (self.y+offsetY)*mult)+1)*127.5
    
            if self.randomNum == 1:
                self.materials = 1 # Coal Ore
            elif self.randomNum == 2:
                self.materials = 2 # Copper Vein
            elif self.randomNum == 3:
                self.materials = 3 # Tin Vein
            elif self.randomNum == 4:
                self.materials = 4 # Iron Vein
            else:
                self.materials = 0
                
            if self.loopcycle == 500 and self.generated == False:
                self.owner = 1
                self.generated = True
            elif self.loopcycle == 2000 and self.enemygenerated == False:
                self.owner = 2 # Enemy Owned
                self.enemygenerated = True
            else:
                self.owner = 0
            self.terrain.append([ self.x, self.y, self.height,self.owner,self.materials ])
            self.x += 20
            if self.x > 1000:
                self.x = 0
                self.y += 20
            
 

        #print("Done Loading Terrain, printing now.../n")


    def renderLand(self):
        global OreText
        for i in range(2550):
            Variation = 1
            z = self.terrain[i][2]
            color = (0, 0, 0)
            if z <= 90:
                color = water
            if z > 90 and z <= 110:
                color = sand
            if z > 110 and z <= 160:
                color = land
            if z > 160 and z <= 195:
                color = highland
            if z > 195:
                color = desert
            pygame.draw.rect(Display, color, (self.terrain[i][0], self.terrain[i][1], 20, 20))

            OreX = X 
            OreY = Y 
            Check = OreX + OreY * 51
            if self.terrain[i][2] > 90:
                if self.terrain[i][4] == 1:
                    Display.blit(CoalVein,(self.terrain[i][0],self.terrain[i][1]))

                elif self.terrain[i][4] == 2:
                    Display.blit(CopperVein,(self.terrain[i][0],self.terrain[i][1]))

                elif self.terrain[i][4] == 3:
                    Display.blit(TinVein,(self.terrain[i][0],self.terrain[i][1]))

                elif self.terrain[i][4] == 4:
                    Display.blit(IronVein,(self.terrain[i][0],self.terrain[i][1]))
                    
            


    def checkTerrain(self):
        biomeX = X /20
        biomeY = Y /20
        Check = biomeX + biomeY * 51
        biomeCheck = self.terrain[int(Check)][2]
        if biomeCheck <= 90:
            Biome = font.render('Ocean',True,(255,255,255))
        if biomeCheck > 90 and biomeCheck <=110:
            Biome = font.render('Beach',True,(255,255,255))
        if biomeCheck > 110 and biomeCheck <=160:
            Biome = font.render('Grassland',True,(255,255,255))
        if biomeCheck > 160 and biomeCheck <=180:
            Biome = font.render('Forest',True,(255,255,255))
        if biomeCheck > 180:
            Biome = font.render('Desert',True,(255,255,255))
        # print(Check)
        Display.blit(Biome,(1050,150))

    def checkOres(self):
        OreX = X /20
        OreY = Y /20
        Check = OreX + OreY * 51

        if self.materials == 1:
            OreText = font.render('Coal Chunk',True,(255,255,255))

        elif self.materials == 2:
            OreText = font.render('Coal Chunk',True,(255,255,255))

        elif self.materials == 3:
            OreText = font.render('Tin Chunk',True,(255,255,255))

        elif self.materials == 4:
            OreText = font.render('Iron Chunk',True,(255,255,255))
            
        else:
            OreText = font.render('None',True,(255,255,255))
        Display.blit(OreText,(1050,50))
        
            
class sideGUI():
    def __init__(self):
        print("It doesn't seem there is anything here")

    def renderGUI():
        pygame.draw.rect(Display, (100,100,100), (1030,0, 190, 1000))
        pygame.draw.rect(Display, (150,150,150), (1020,0, 10, 1000))

class playerEmpire():
    global ownedsquares
    def __init__(self,master):
        self.ownedsquares = 1
        for i in range(0,2550):
            if self.terrain[i][3] == 1:
                ownedSquares += 1



TGEN = terrainGenerate()
TGEN.__init__()
#playerEmpire.__init__()
TGEN.landGen()
#TGEN.smoothLand()

while True:
    Display.fill(black)
    maxmoney = maxmoney * ownedsquares
    money += 1 * ownedsquares
    if money > maxmoney:
        money = 5000
    #textsurface = font.render('Money : ' + str(money), False, (255, 255, 255))
    sideGUI.renderGUI()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if money - 500 < 0:
                        print("Not enough Gold")
                    else:
                        print("you bought something")
                        money -= 500

                if event.key == pygame.K_w:
                    Y -= 20
                if event.key == pygame.K_s:
                    Y += 20
                if event.key == pygame.K_a:
                    X -= 20
                if event.key == pygame.K_d:
                    X += 20

                if X < 0 or X > 1000:
                    X = 500
                if Y < 0 or Y > 1000:
                    Y = 500

    TGEN.checkTerrain()
    TGEN.renderLand()
    TGEN.checkTerrain()
    TGEN.checkOres()

    #GoldAmountText = font.render('Gold : ' + str(money),True,(255,255,255))
    XText = font.render('X : ' + str(int(X / 20)),True,(255,255,255))
    YText = font.render('Y : ' + str(int(Y / 20)),True,(255,255,255))
    #Display.blit(GoldAmountText,(1050,50))
    Display.blit(XText,(1050,100))
    Display.blit(YText,(1125,100))
    Display.blit(SelectImage,(X,Y))
    pygame.display.update()
