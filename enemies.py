import pygame
import random

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREEN_WIDTH = 672
SCREEN_HEIGHT = 640

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
        (1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1),
        (0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0),
        (0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0),
        (0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0),
        (1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1),
        (0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0),
        (0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0),
        (0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0),
        (1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1),
        (1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1),
        (1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1),
        (1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1),
        (1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1),
        (1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1),
        (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1))
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
    def __init__(self,x,y,change_x,change_y):
        #ініціація створення спрайту
        pygame.sprite.Sprite.__init__(self)
        #задання початкового напряму для привида
        self.change_x = change_x
        self.change_y = change_y
        #завантаження зображення спрайту
        self.image = pygame.image.load("slime.png").convert_alpha()
        self.rect = self.image.get_rect()
        #визначення розташування спрайту на мапі
        self.rect.topleft = (x,y)
                
def draw_enviroment(screen):
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
    

