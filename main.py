from typing import TextIO
import pygame
import math
import random

from pygame import mixer

pygame.init()
mixer.init()

obrazovka = pygame.display.set_mode((1280,720))

pygame.display.set_caption("Ondra")

icona = pygame.image.load('files\icona.png')
pygame.display.set_icon(icona)

class Img:
    def __init__(self,source):
        self.source = source
        self.loaded = pygame.image.load('files/'+source)
        self.hitbox = False
        self.width = self.loaded.get_width()
        self.height = self.loaded.get_size()[1]
    def render(self,x,y):
        self.x = x
        self.y = y
        if self.hitbox:
            pygame.draw.rect(obrazovka, red, (self.x,self.y,self.loaded.get_width(),self.loaded.get_size()[1]))
        obrazovka.blit(self.loaded,(x,y))

class Room:
    def __init__(self):
        self.active = False

    def renderbackground(self,R, G, B):
        self.R = R
        self.G = G
        self.B = B
        obrazovka.fill((self.R, self.G, self.B))

    def switch(self):
        if self.active:
            self.active = False
        else:
            self.active = True

level1 = Room()
level2 = Room()
partyroom = Room()
level3 = Room()

collision = False
zakladnišířka = 100
zakladnivýška = 100
player = Img('square.png')
squareX = 500
squareY = 100
squarechangeX = 0
squarechangeY = 0

discoball1 = Img('disco1.png')
discoball2 = Img('disco2.png')
discoball3 = Img('disco3.png')
discoball4 = Img('disco4.png')
discoball5 = Img('disco5.png')

discotimer = 0

def disco(discotimer):
    X = 500
    discotimer += 0.01
    if discotimer <= 0:
        Y=-6
        discoball1.render(X,Y)
    elif discotimer >0 and discotimer <=1:
        Y=-4
        discoball2.render(X,Y)
    elif discotimer >1 and discotimer <=2:
        Y=-2
        discoball3.render(X,Y)
    elif discotimer >2 and discotimer <=3:
        Y=0
        discoball4.render(X,Y)
    elif discotimer >3 and discotimer <=4:
        Y=-2
        discoball5.render(X,Y)
    else:
        Y=-4
        discoball5.render(X,Y)
        discotimer = 0
    return discotimer

death = Img('death.jpg')

tolerace = 0

health = 5

cooldown = 0

oreoX = random.randint(1, 1179)
oreoY = random.randint(0, 619)

oreo = Img('oreo.png')

spikeX = 500
spikeY = 500

spike = Img('spike.png')

cedule = Img('cedule.png')

red = (255,0,0)

def isCollision(firstX,firstY,secondX,secondY, collision, widthP, heightP, widthT, heightT, tolerace):
    firstX += widthP / 2
    firstY += heightP / 2
    secondX += widthT / 2
    secondY += heightT / 2
    tolerance = (widthT/2) + (widthP/2) + tolerace
    D =  math.sqrt(pow((secondX - firstX),2) + pow((secondY - firstY),2))
    if D <= tolerance:
        collision = True
    elif collision == True:
        collision = False

    return collision

TeoX = 900
TeoY = 500

Teo = Img('Teo.png')

def Teohunt(X,Y,Xp, Yp):
    maxSpeed = 2
    if isCollision(Xp, Yp, X, Y,player.loaded.get_width(),player.loaded.get_size()[1],Teo.loaded.get_width(),Teo.loaded.get_size()[1], False,650) == True:
        Xp = player.loaded.get_width() + Xp
        Yp = player.loaded.get_size()[1] / 2 + Yp
        Xw = Teo.loaded.get_width() / 2 + X
        Yh = Teo.loaded.get_size()[1] / 2 + Y
        if (Xw - Xp) > 0:
            X -= random.randint(0,maxSpeed)
        elif (Xw - Xp) < 0:
            X += random.randint(0,maxSpeed)
        if (Yh - Yp) > 0:
            Y-= random.randint(0,maxSpeed)
        elif (Yh - Yp) < 0:
            Y+= random.randint(0,maxSpeed)
    Teo.render(X,Y)
    return X,Y

def drag(Xp,Yp,X,Y,collision):
    if isCollision(Xp, Yp, X, Y, collision,player.loaded.get_width(),player.loaded.get_size()[1],Teo.loaded.get_width(),Teo.loaded.get_size()[1],5) == True:
        Xp = X
        Yp = Y
    collision = isCollision(Xp, Yp, X, Y, collision,player.loaded.get_width(),player.loaded.get_size()[1],Teo.loaded.get_width(),Teo.loaded.get_size()[1],50)
    return collision,Xp,Yp

def control(x,y,speed,pressed_keys):
    keys = pressed_keys
    normalizedSpeed = speed
    if keys[pygame.K_LSHIFT]:
        normalizedSpeed += 1
    if keys[pygame.K_a] and x>0: 
        x -= normalizedSpeed
    if keys[pygame.K_d] and x+player.loaded.get_width()<1280:
        x += normalizedSpeed 
    if keys[pygame.K_w] and y>0: 
        y -= normalizedSpeed
    if keys[pygame.K_s] and y+player.loaded.get_size()[1]<720:
        y += normalizedSpeed

    return x,y

# TEXT
susenky = 0
font = pygame.font.Font('freesansbold.ttf', 40)
text = font.render('Kolik sušenek jsi snědl: '+ str(susenky), False, (0,0,0) )
textRect = text.get_rect()

healthbar = font.render('Životy: '+ str(health), False, (0,0,0))

discohudba = 0
hra = True
level1.active = True
dying = False
speed = 1
dscalex = 1080
dscaley = 500
dX = 100
dY = 100
timerend = 0
die = 0
R = 50
B = 50
G = 50
chyceno = False

while hra:

#   LEVEL 1

    if level1.active:
        mixer.music.set_volume(0)
        level1.renderbackground(160, 255, 220)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hra = False
                level1.active = False
        collision = isCollision(squareX,squareY,oreoX,oreoY, collision, player.loaded.get_width(), player.loaded.get_size()[1],oreo.loaded.get_width(),oreo.loaded.get_size()[1], tolerace)
        cedule.render(50,50)
        if collision:
            oreoX = random.randint(1, 719)
            oreoY = random.randint(0, 479)
            oreo.render(oreoX,oreoY)
            susenky += 1
            text = font.render('Kolik sušenek jsi snědl: '+ str(susenky), False, (0,0,0))
            if susenky <= 50:
                šířka = zakladnišířka + susenky*5
                výška = zakladnivýška + susenky*5
                speed += 0.1
            player.loaded = pygame.transform.smoothscale(player.loaded, (šířka, výška))

        else:
            oreo.render(oreoX,oreoY)

        player.render(squareX,squareY)
        
        if player.loaded.get_size()[1]+squareY >= 720:
            level1.switch()
            level2.switch()
            squareY = 2

        obrazovka.blit(text, (1, 1))  

    if mixer.music.get_busy()==False:
        if discohudba == 0:
            mixer.music.load('files\disco.mp3')
            mixer.music.play()
            discohudba = 1
        elif discohudba == 1:
            mixer.music.load('files\disco2.mp3')
            mixer.music.play()
            discohudba = 0

# LEVEL 2

    if level2.active:
        mixer.music.set_volume(0.1)
        if mixer.music.get_busy()==False:
            if discohudba == 0:
                mixer.music.load('files\disco.mp3')
                mixer.music.play()
                discohudba = 1
            elif discohudba == 1:
                mixer.music.load('files\disco2.mp3')
                mixer.music.play()
                discohudba = 0
        level2.renderbackground(160, 100, 225)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hra = False
                level2.active = False

        injury = isCollision(squareX,squareY,spikeX,spikeY, collision, player.loaded.get_width(), player.loaded.get_size()[1], spike.loaded.get_width(),spike.loaded.get_size()[1], tolerace)
        if injury: 
            if cooldown > 0:
                cooldown -= 1
            else:
                health -= 1
                cooldown = 500
        if health <= 0:
            level2.active = False
            dying = True
        spike.render(spikeX,spikeY)
        player.render(squareX, squareY)
        
        if squareY <= 1:
            level2.switch()
            level1.switch()
            squareY = 719 - player.loaded.get_size()[1]

        if squareX >= 1280 - player.loaded.get_width():
            level2.switch()
            partyroom.switch()
            squareX = 2

#   PARTY ROOOM

    if partyroom.active:
        if mixer.music.get_busy()==False:
            if discohudba == 0:
                mixer.music.load('files\disco.mp3')
                mixer.music.play()
                discohudba = 1
            elif discohudba == 1:
                mixer.music.load('files\disco2.mp3')
                mixer.music.play()
                discohudba = 0
        mixer.music.set_volume(0.5)
        partyroom.renderbackground(R,G,B)
        Rrandom = random.randint(-1,1)
        Grandom = random.randint(-1,1)
        Brandom = random.randint(-1,1)
        if (R + Rrandom) >= 255 or (R + Rrandom) <= 0:
            R = 100
        if (G + Grandom) >= 255 or (G + Grandom) <= 0:
            G = 100
        if (B + Brandom) >= 255 or (B + Brandom) <= 0:
            B = 100
        R += Rrandom
        G += Grandom
        B += Brandom
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hra = False
                partyroom.active = False
        chyceni = [False,0,0]
        if susenky < 50:
            chyceni = drag(squareX,squareY,TeoX, TeoY, collision)
            if chyceni[0] == True:
                chyceno = True
        else:
            chyceni[0] = False

        if discotimer >0 and discotimer <=1 and squareX>1:
            squareX -= random.randint(-5,10)*0.1
        elif discotimer >1 and discotimer <=2 and squareY>1:
            squareY -= random.randint(-5,10)*0.1
        elif discotimer >2 and discotimer <=3 and squareX<1180:
            squareX += random.randint(-5,10)*0.1
        elif discotimer >3 and discotimer <=4 and squareY<620:
            squareY += random.randint(-5,10)*0.1

        if squareX <= 0:
            partyroom.switch()
            level2.switch()
            squareX = 1279-player.loaded.get_width()
        player.render(squareX, squareY)
        Teopozice=Teohunt(TeoX,TeoY,squareX, squareY)
        if chyceni[0] == True:
            TeoX = chyceni[1]
            TeoY = chyceni[2]
        TeoX = Teopozice[0]
        TeoY = Teopozice[1]
        if chyceni[0] == True:
            TeoX -= 5
            squareX -= 5
            if squareX <= 5:
                partyroom.switch()
                level2.switch()
                health -= 1
                squareX = 700
        discotimer = disco(discotimer)

        if squareX >= 1280 - player.loaded.get_width():
            partyroom.switch()
            level3.switch()
            squareX = 2

        if not partyroom.active:
            TeoX = 900
            TeoY = random.randint(100,500)
            chyceno = False

#   LEVEL 3

    if level3.active:
        mixer.music.set_volume(0.1)
        if mixer.music.get_busy()==False:
            if discohudba == 0:
                mixer.music.load('files\disco.mp3')
                mixer.music.play()
                discohudba = 1
            elif discohudba == 1:
                mixer.music.load('files\disco2.mp3')
                mixer.music.play()
                discohudba = 0
        level3.renderbackground(100, 100, 100)
        player.render(squareX,squareY)
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        hra = False
                        level3.active = False
        if squareX <= 0:
            level3.switch()
            partyroom.switch()
            squareX = 1279-player.loaded.get_width()

#   DEATH

    if dying and die == 0:
        mixer.music.stop()
        mixer.music.load('files\death.mp3')
        mixer.music.set_volume(0.5)
        mixer.music.play()
        die = 1
    if dying:
        death.loaded = pygame.transform.smoothscale(death.loaded, (int(dscalex), int(dscaley)))
        dscalex += 0.05
        dscaley += 0.05
        dX -= 0.05
        dY -= 0.05
        timerend += 1
        if timerend >= 2000:
            dying = False
            hra = False
            pygame.quit
        obrazovka.fill((0, 0, 0))
        obrazovka.blit(death.loaded,(int(dX),int(dY)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hra = False
                dying = False

    if chyceno == False:
        squareX = control(squareX,squareY,speed,pygame.key.get_pressed())[0]
        squareY = control(squareX,squareY,speed,pygame.key.get_pressed())[1]
    if not dying:
        healthbar = font.render('Životy: ' + str(health), False, (0,0,0))
        obrazovka.blit(healthbar,(1100,1))

    pygame.display.update()