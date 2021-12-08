import pygame
from enemies import *
import random

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREENWIDTH = 160
SCREENHEIGHT = 160

#визначення кольорів для подальшого використання
BLACK = (0,0,0)
WHITE = (255,255,255)

#клас гравець - пакмен
class Player(pygame.sprite.Sprite):
    changeX = 0
    changeY = 0
    explosion = False
    gameOver = False
    def __init__(self,x,y,filename, controlByGame = False):
        #ініціація створення спрайта гравця, задання кольору,розташування, додаткових спрайтів тощо
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y) # початкове положення гравця
        self.nextCoordX = -5
        self.nextCoordY = -5
        #спрайт та налаштування анімації ходьби
        img = pygame.image.load("walk.png").convert()
        #self.moveRightAnimation = Animation(img,32,32)
        #self.moveLeftAnimation = Animation(pygame.transform.flip(img,True,False),32,32)
        #self.moveUpAnimation = Animation(pygame.transform.rotate(img,90),32,32)
        #self.moveDownAnimation = Animation(pygame.transform.rotate(img,270),32,32)
        #спрайт та налаштування анімації вибуху
        img = pygame.image.load("explosion.png").convert()
        self.explosionAnimation = Animation(img,30,30)
        #збереження зображення гравця
        self.playerImage = pygame.image.load(filename).convert()
        self.playerImage.set_colorkey(BLACK)
        self.controlByGame = controlByGame
        self.isGoingByGame = False


    def update(self, blocksGroup):
        #метод запобішання перетину перешкод гравцем
        if not self.explosion:
            #перешкоджання гравецеві проходити крізь стіни всередині поля
            for block in pygame.sprite.spritecollide(self,blocksGroup,False):
                self.rect.x -= (block.rect.x - self.rect.x)*0.1
                self.rect.y -= (block.rect.y - self.rect.y)*0.1
                #self.changeX = 0
                #self.changeY = 0

            if (((self.rect.x) / 32) == self.nextCoordX or self.nextCoordY == ((self.rect.y) / 32)):
                self.nextX = -5
                self.nextY = -5
                self.changeX = 0
                self.changeY = 0
                self.isGoingByGame = False

            #перешкоджання гравцеві виходити за межі поля
            if self.rect.right < 32:
                self.rect.x -= (self.rect.x)*0.1
                self.changeX = 0
                self.changeY = 0
            elif self.rect.left > SCREENWIDTH-32:
                self.rect.x -= (SCREENWIDTH - self.rect.x)*0.1
                self.changeX = 0
                self.changeY = 0
            if self.rect.bottom < 32:
                self.rect.y -= (self.rect.y)*0.1
                self.changeX = 0
                self.changeY = 0
            elif self.rect.top > SCREENHEIGHT-32:
                self.rect.y -= (SCREENHEIGHT - self.rect.y)*0.1
                self.changeX = 0
                self.changeY = 0
            self.rect.x += self.changeX
            self.rect.y += self.changeY

            #ініціація виконання анімацій
            #if self.changeX > 0:
            #    self.moveRightAnimation.update(10)
            #    self.image = self.moveRightAnimation.getCurrentImage()
            #elif self.changeX < 0:
            #    self.moveLeftAnimation.update(10)
            #    self.image = self.moveLeftAnimation.getCurrentImage()
#
            #if self.changeY > 0:
            #    self.moveDownAnimation.update(10)
            #    self.image = self.moveDownAnimation.getCurrentImage()
            #elif self.changeY < 0:
            #    self.moveUpAnimation.update(10)
            #    self.image = self.moveUpAnimation.getCurrentImage()
        else:
            #ініціація анімації вибуху та закінчення гри для гравця
            #if self.explosionAnimation.index == self.explosionAnimation.getLength() -1:
            #   pygame.time.wait(500)
                self.gameOver = True
            #self.explosionAnimation.update(12)
            #self.image = self.explosionAnimation.getCurrentImage()

    def playerRun(self,point):
        x = ((self.rect.x)/32)
        y = ((self.rect.y)/32)

        if (point.Y) == x and (point.X) == y:
            self.changeX = 0
            self.changeY = 0
            self.isGoingByGame = False
        if abs((x) - point.Y) == 0:
            self.changeX = 0
            if y - point.X < 0:
                self.moveDown()
            if y - point.X > 0:
                self.moveUp()
        if (y) - point.X == 0:
            self.changeY = 0
            if x - point.Y < 0:
                self.moveRight()
            if x - point.Y > 0:
                self.moveLeft()

    #зміна координатів гравця в залежності від команди
    def moveRight(self):
        self.changeX = 2

    def moveLeft(self):
        self.changeX = -2

    def moveUp(self):
        self.changeY = -2

    def moveDown(self):
        self.changeY = 2
    
    #припинення руху гравця на полі
    def stopMoveRight(self):
        if self.changeX != 0:
            self.image = self.playerImage
        self.changeX = 0

    def stopMoveLeft(self):
        if self.changeX != 0:
            self.image = pygame.transform.flip(self.playerImage,True,False)
        self.changeX = 0

    def stopMoveUp(self):
        if self.changeY != 0:
            self.image = pygame.transform.rotate(self.playerImage,90)
        self.changeY = 0

    def stopMoveDown(self):
        if self.changeY != 0:
            self.image = pygame.transform.rotate(self.playerImage,270)
        self.changeY = 0

    def isPossibleToGo(self,field, y, x):
        x = round(x)
        y = round(y)
        environmentHight = len(field)
        environmentWidth = len(field[0])

        if x >= 0 and y < environmentWidth and y >= 0 and x < environmentHight and field[x][y] > 0:
            return True
        return False

    def GetCordsInMaze(self):
        return ((self.rect.x)/32),((self.rect.y)/32)

# 0:Up, 1:Down,2:right,3:down
    def RunToCoords(self, action):
        if (self.isGoingByGame == False):
            if (action == 0):
                self.nextCoordY = ((self.rect.y)/32)-1
                self.isGoingByGame = self.moveUp()
            if (action == 1):
                self.nextCoordY = ((self.rect.y)/32)+1
                self.isGoingByGame = self.moveDown()
            if (action == 2):
                self.nextCoordX = ((self.rect.x)/32)+1
                self.isGoingByGame = self.moveRight()
            if (action == 3):
                self.nextCoordX = ((self.rect.x)/32)-1
                self.isGoingByGame = self.moveLeft()

#клас анімацій (базових їх налаштувань)
class Animation(object):
    def __init__(self,img,width,height):
        # ініціація створення аніманції
        #завантаження спрайту
        self.sprite_sheet = img
        #створення списку зображень
        self.imageList = []
        self.loadImages(width,height)
        #стоврення змінної, що визначатиме порядок аніманцій
        self.index = 0
        #створення змінної, що визначатиме час роботи програми в необхідних завданнях
        self.clock = 1
        
    def loadImages(self,width,height):
        #завантаження та перебір всіх вказаних зображень
        for y in range(0,self.sprite_sheet.get_height(),height):
            for x in range(0,self.sprite_sheet.get_width(),width): 
                # load images into a list
                img = self.getImage(x,y,width,height)
                self.imageList.append(img)

    def getImage(self,x,y,width,height):
        #отримання, створення та відображення готового спрайта
        image = pygame.Surface([width,height]).convert()
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        image.set_colorkey((0,0,0))
        return image

    def getCurrentImage(self):
        #визначення спрайта, що задіяний
        return self.imageList[self.index]

    def getLength(self):
        #повернення довжини списку зображень
        return len(self.imageList)

    def update(self,fps=30):
        #метод оновлення станів для анімацій
        step = 30
        l = range(1,30,step)
        if self.clock == 30//fps:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            self.index += 1
            if self.index == len(self.imageList):
                self.index = 0

            
    
        
