from random import Random
import pygame
from pygame.constants import GL_GREEN_SIZE
from player import Player
from enemies import *
from pathfinding import *

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREEN_WIDTH = 672
SCREEN_HEIGHT = 640

#визначення кольорів для подальшого використання
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

startI = 9
startJ = 0

#клас самої гри
class Game(object):
    def __init__(self):
        #ініціація створення гри, ігрового вікна тощо
        #тимчасове призупинення гри для процесу її створення
        self.game_over = True
        self.font = pygame.font.Font(None, 30)
        #створення змінної для визначення рахунку гравця
        self.score = 0
        #створення гравця
        self.player = Player(startJ*32,startI*32,"player.png")
        #стоворення блоків (шляхів), якими пересуватиметься гравець
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        #створення груп монеток (їжі) для гравця
        self.dots_group = pygame.sprite.Group()
        #створення допоміжних блоків, що зображатимуть стіни та не даватимуть гравцю їх перетинати
        self.blocks_group = pygame.sprite.Group()
        self.path_group = pygame.sprite.Group()
        #перетворення колекції поля для проходження по ній надалі
        gridforblocks = enumerate(grid)

        #перебір елементів поля для побудови шляхів пересування гравця (можливе лише там, де одиниці) та розташування стін (де нулі)
        for i,row in gridforblocks:
            for j,item in enumerate(row):
                if item == 1:
                    if (j+1<wid and grid[i][j+1] == 0) and (grid[i][j-1] == 0):
                        self.vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                    if (i+1<high and grid[i+1][j] == 0) and (grid[i-1][j] == 0):
                        self.horizontal_blocks.add(Block(j*32+8,i*32 + 8,BLACK,16,16))
                elif item == 0:
                    self.blocks_group.add(Block(j*32 + 8,i*32 + 8,BLUE,20,20))
        
        #створення ворогів (привидів)
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Slime(256,288,0,2))
        self.enemies.add(Slime(288,288,0,-2))
        self.enemies.add(Slime(320,288,0,2))
        self.enemies.add(Slime(352,288,0,2))
        self.enemies.add(Slime(384,288,2,0))

        #створення та додавання "їжі" на поле (всюди, де немає стін)
        listOfXY = []
        for i, row in enumerate(grid):
            for j, item in enumerate(row):
                if item != 0:
                    coordinates = [i, j]
                    listOfXY.append(coordinates)
        #           self.dots_group.add(Ellipse(j*32+12,i*32+12,WHITE,8,8))
        foodPosition = random.randint(0, len(listOfXY)-1)
        endI = listOfXY[foodPosition][0] 
        endJ = listOfXY[foodPosition][1] 
        self.dots_group.add(Ellipse(endJ* 32 + 5, endI* 32 + 5, WHITE, 24, 24))
        #self.path_group = bfs(startI, startJ, endI, endJ)
        #self.path_group = pathForDfs(startI, startJ, endI, endJ)
        #відновлення гри одразу після завершеня її створення
        self.game_over = False

    def process_events(self):
        #метод для зчитування подій, тобто дій гравця, таких як креування гравцем за допомогою клавіатури
        #якщо гравець зробив хоч щось відбувається наступне:
        for event in pygame.event.get(): 
            #якщо гравець натиснув на клавішу "вийти", гра завершується
            if event.type == pygame.QUIT:
                return True
            #якщо гравець натис будь-яку клавішу клавіатури, відбувається зчитування, яка саме клавіша задіяна
            if event.type == pygame.KEYDOWN:
                #при натисканні клавіші "Ентер" відбувається запуск нової гри
                if event.key == pygame.K_RETURN:
                    print(ucs())
                    self.__init__()
                #при натисанні клавіші праворуч, ліворуч, вгору чи вниз відбувається рух гравця у відповідному напрямку
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_UP:
                    self.player.move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                #при натисканні клавіші "ESCAPE" відбувається завершення гри
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True

            #якщо гравець відпускає клавішу клавіатури відбувається наступне:
            elif event.type == pygame.KEYUP:
                #при відпусканні клавіші праворуч, ліворуч, вгору чи вниз припиняється рух гравця у відповідному напрямку
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()
        return False

    def run_logic(self):
        #метод, що забезпечує процес проходу гри
        if not self.game_over:
            #доки статус гри "не завершено", відбувається оновлення стану гравця, його розташування
            self.player.update(self.horizontal_blocks,self.vertical_blocks, self.blocks_group)
            #при кожному зіткненні гравця з їжею відбувається зарахування балу для гравця та зникнення їжі
            block_hit_list = pygame.sprite.spritecollide(self.player,self.dots_group,True)
            if len(block_hit_list) > 0:
                self.score += 1
                print(len(self.dots_group))
            #якщо на полі не залишилось їжі, то гру завершено
            if len(self.dots_group) == 0:
                self.player.explosion = True
            #якщо гравцеь стикаєтьсяз ворогом, відбувається вибух гравця та завершення гри, зміна статусу гри на "завершено"
            block_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,True)
            if len(block_hit_list) > 0:
                self.player.explosion = True 
            self.game_over = self.player.game_over
    

    def display_frame(self,screen):
        #метод створення екрану гри, зображення поля, необхідних спрайтів, груп, текстів  тощо
        screen.fill(BLACK)
        self.horizontal_blocks.draw(screen)
        self.vertical_blocks.draw(screen)
        draw_enviroment(screen)
        self.dots_group.draw(screen)
        self.enemies.draw(screen)
        #drawPath(self.path_group, screen)
        screen.blit(self.player.image,self.player.rect)
        text = self.font.render("Score: " + str(self.score),True,GREEN)
        messagePart1 = self.font.render("Tap ENTER", True, GREEN)
        messagePart2 = self.font.render("to restart", True, GREEN)
        screen.blit(text,[180,53])
        screen.blit(messagePart1,[395,45])
        screen.blit(messagePart2,[405,65])
        pygame.display.flip()