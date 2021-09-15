import pygame
from enemies import *
import random

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREENWIDTH = 672
SCREENHEIGHT = 640

#визначення кольорів для подальшого використання
BLACK = (0,0,0)
WHITE = (255,255,255)

#клас гравець - пакмен
class Player(pygame.sprite.Sprite):
    changeX = 0
    changeY = 0
    explosion = False
    gameOver = False
    def __init__(self,x,y,filename):
        #ініціація створення спрайта гравця, задання кольору,розташування, додаткових спрайтів тощо
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y) # початкове положення гравця
        #спрайт та налаштування анімації ходьби
        img = pygame.image.load("walk.png").convert()
        self.moveRightAnimation = Animation(img,32,32)
        self.moveLeftAnimation = Animation(pygame.transform.flip(img,True,False),32,32)
        self.moveUpAnimation = Animation(pygame.transform.rotate(img,90),32,32)
        self.moveDownAnimation = Animation(pygame.transform.rotate(img,270),32,32)
        #спрайт та налаштування анімації вибуху
        img = pygame.image.load("explosion.png").convert()
        self.explosionAnimation = Animation(img,30,30)
        #збереження зображення гравця
        self.playerImage = pygame.image.load(filename).convert()
        self.playerImage.set_colorkey(BLACK)

    def update(self,horizontalBlocks,verticalBlocks, blocksGroup):
        #метод запобішання перетину перешкод гравцем
        if not self.explosion:
            #перешкоджання гравецеві проходити крізь стіни всередині поля
            for block in pygame.sprite.spritecollide(self,blocksGroup,False):
                self.rect.x -= (block.rect.x - self.rect.x)*0.1
                self.rect.y -= (block.rect.y - self.rect.y)*0.1
                self.changeX = 0
                self.changeY = 0
            #перешкоджання гравцеві виходити за межі поля
            if self.rect.right <= 30:
                self.rect.left = 2
            if self.rect.left >= SCREENWIDTH - 30:
                self.rect.right = SCREENWIDTH - 2
            if self.rect.bottom <= 30:
                self.rect.top = 2
            if self.rect.top >= SCREENHEIGHT - 30:
                self.rect.bottom = SCREENHEIGHT - 2
            #зміна та збереження координатів гравця
            self.rect.x += self.changeX
            self.rect.y += self.changeY
            #заборона на спробу перетнути лінії вздовж дозволеної траекторії ходьби
            for block in pygame.sprite.spritecollide(self,horizontalBlocks,False):
                self.rect.centery = block.rect.centery
                self.changeY = 0
            for block in pygame.sprite.spritecollide(self,verticalBlocks,False):
                self.rect.centerx = block.rect.centerx
                self.changeX = 0
            #ініціація виконання анімацій
            if self.changeX > 0:
                self.moveRightAnimation.update(10)
                self.image = self.moveRightAnimation.getCurrentImage()
            elif self.changeX < 0:
                self.moveLeftAnimation.update(10)
                self.image = self.moveLeftAnimation.getCurrentImage()

            if self.changeY > 0:
                self.moveDownAnimation.update(10)
                self.image = self.moveDownAnimation.getCurrentImage()
            elif self.changeY < 0:
                self.moveUpAnimation.update(10)
                self.image = self.moveUpAnimation.getCurrentImage()
        else:
            #ініціація анімації вибуху та закінчення гри для гравця
            if self.explosionAnimation.index == self.explosionAnimation.getLength() -1:
                pygame.time.wait(500)
                self.gameOver = True
            self.explosionAnimation.update(12)
            self.image = self.explosionAnimation.getCurrentImage()
            
    #зміна координатів гравця в залежності від команди
    def moveRight(self):
        self.changeX = 3

    def moveLeft(self):
        self.changeX = -3

    def moveUp(self):
        self.changeY = -3

    def moveDown(self):
        self.changeY = 3
    
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

            
    
        
