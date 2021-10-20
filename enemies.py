import pygame
from labyrint import*
import pathfinding

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREENWIDTH = 672
SCREENHEIGHT = 640

#визначення кольорів для подальшого використання
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
    
#зображення поля гри у вигляді одиниць та нулів, де одиниці - місця, де гравець може ходити, нулі - блоки (стіни)
grid = ((1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1),
        (1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1),
        (1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1),
        (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
        (1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1),
        (1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1),
        (1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1),
        (1,0,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,0,0,1),
        (1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1),
        (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
        (1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1),
        (1,0,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,0,0,1),
        (1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1),
        (1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1),
        (1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,1,0,1),
        (1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1),
        (1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1),
        (1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1),
        (1,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,1),
        (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1))
#grid = generateMaze(int(SCREENWIDTH/32), int(SCREENHEIGHT/32))
#визначення довжини та ширини поля (кількості рядків та елементів в рядках)
wid = len(grid[0])
high = len(grid)

#клас блоків - спрайтів прямокутної форми, що не видно на зображенні, проте впливають на хід гри
class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,color,width,height):
        #ініціація стоврення спрайту
        pygame.sprite.Sprite.__init__(self)
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        #визначення розташування спрайту на мапі
        self.rect.topleft = (x,y)

#клас еліпсу, що зображує одну монетку (їжу) для пакмена
class Ellipse(pygame.sprite.Sprite):
    def __init__(self,x,y,color,width,height):
        #ініціація створення спрайту
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        #малювання фігури
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
        self.rect = self.image.get_rect()
        #визначення розташування спрайту на мапі
        self.rect.topleft = (x,y)

#клас привидів (ворогів пакмена)
class Slime(pygame.sprite.Sprite):
    def __init__(self,x,y,ghostType):
        #ініціація створення спрайту
        pygame.sprite.Sprite.__init__(self)
        #завантаження зображення спрайту
        self.image = pygame.image.load("slime.png").convert_alpha()
        self.rect = self.image.get_rect()
        #визначення розташування спрайту на мапі
        self.rect.topleft = (x,y)
        self.type = ghostType
        self.path = []
        self.step = 1
        self.currentPos = (0,0)
        self.nextPos = (0,0)

    changeX = 0
    changeY = 0 

    def update(self,point):
        self.nextPos = point
        if len(self.path) == 0 or self.nextPos != self.currentPos:
            self.path = pathfinding.findPathBFS(grid, (self.rect.y+16)/32,(self.rect.x+16)/32,point[0],point[1])
            self.currentPos = self.nextPos
            self.path.reverse()
        self.ghostRun(self.path)
        self.rect.x += self.changeX
        self.rect.y += self.changeY
                
    def ghostRun(self,path):
        if len(path) >= 1:
            nextPoint = path[0]
            i = ((self.rect.y)/32)
            j = ((self.rect.x)/32)
            if nextPoint[1] == j and nextPoint[0] == i:
                path.remove(nextPoint)
                self.changeX = 0
                self.changeY = 0
            else:
                if j - nextPoint[1] == 0:
                    self.changeX = 0
                    if i - nextPoint[0] < 0:
                        self.changeY = self.step
                    if i - nextPoint[0] > 0:
                        self.changeY = -self.step
                if i - nextPoint[0] == 0:
                    self.changeY = 0
                    if j - nextPoint[1] < 0:
                        self.changeX = self.step
                    if j - nextPoint[1] > 0:
                        self.changeX = -self.step

def drawEnviroment(screen):
    #метод створення ігрового поля
    engrid = enumerate(grid)
    #перебір елементів в заданій попередньо матриці по рядках та стовпцях
    for i,row in engrid:
        for j,item in enumerate(row):
            #якщо елемент рівний одиниці, то в залежності від його сусідів відбувається побудова стін або їхня відсутність
            if item == 1:
                if j+1<wid and grid[i][j+1] == 0:
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32+32,i*32], 3)
                elif j+1 == wid:
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32+32,i*32], 3)
                if grid[i][j-1] == 0:
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                elif j == 0:
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                if i+1<high and grid[i+1][j] == 0:
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32,i*32+32], 3)
                elif i + 1 == high:
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32,i*32+32], 3)
                if grid[i-1][j] == 0:
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                elif i == 0:
                    pygame.draw.line(screen, BLUE ,  [j*32, i*32], [j*32+32,i*32], 3)