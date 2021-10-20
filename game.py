from random import Random
import pygame
from player import Player
from enemies import *
from pathfinding import *
from datetime import datetime
import minOrExpMax
import csv


#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREENWIDTH = 672
SCREENHEIGHT = 640

#визначення кольорів для подальшого використання
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

#задання початкових координатів для гравця
startI = 9
startJ = 0

#клас самої гри
class Game(object):
    def __init__(self):
        #ініціація створення гри, ігрового вікна тощо
        #тимчасове призупинення гри для процесу її створення
        self.gameOver = True
        self.font = pygame.font.Font(None, 30)
        #створення змінної для визначення рахунку гравця
        self.score = 0
        #створення груп монеток (їжі) для гравця
        self.dotsGroup = pygame.sprite.Group()
        #створення допоміжних блоків, що зображатимуть стіни та не даватимуть гравцю їх перетинати
        self.blocksGroup = pygame.sprite.Group()
        #створення списку для точок шляху
        self.pathGroup = pygame.sprite.Group()
        #перетворення колекції поля для проходження по ній надалі
        gridForBlocks = enumerate(grid)
        self.status = False
        #перебір елементів поля для побудови шляхів пересування гравця (можливе лише там, де одиниці) та розташування стін (де нулі)
        for i,row in gridForBlocks:
            for j,item in enumerate(row):
                if item == 0:
                    self.blocksGroup.add(Block(j*32 + 8,i*32 + 8,BLUE,24,24))
        
        #створення ворогів (привидів)
        ghostTypes = ("randGhost", "followingGhost")
        self.randGhosts = []
        self.followingGhosts = []
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Slime(256,288, ghostTypes[0]))
        self.enemies.add(Slime(288,288,ghostTypes[1]))
        self.enemies.add(Slime(320,288,ghostTypes[0]))
        # self.enemies.add(Slime(352,288,ghostTypes[0]))
        # self.enemies.add(Slime(384,288,ghostTypes[0]))
        for slime in self.enemies:
            if(slime.type == ghostTypes[0]):
                self.randGhosts.append(slime)
            else:
                self.followingGhosts.append(slime)

        #створення та додавання "їжі" на поле 
        listOfXY = []
        self.pathDotsCount = 0
        for i, row in enumerate(grid):
            for j, item in enumerate(row):
                if item != 0:
                    #заповнення списку точок, де можливе розташування їжі
                    coordinates = [i, j] 
                    listOfXY.append(coordinates)
                    self.pathDotsCount = self.pathDotsCount + 1
                    #заповнення списку їжі
                    self.dotsGroup.add(Ellipse(j*32+12,i*32+12,WHITE,8,8))
        
        #створення гравця
        # playerPosition = random.randint(0, len(listOfXY)-1)
        # startI = listOfXY[playerPosition][0] 
        # startJ = listOfXY[playerPosition][1] 
        self.player = Player(startJ*32,startI*32,"player.png", True)
        ##визначення випадкової точки для однієї монетки (кінцевої точки шляху)
        # foodPosition = random.randint(0, len(listOfXY)-1)
        # endI = listOfXY[foodPosition][0] 
        # endJ = listOfXY[foodPosition][1] 
        # endI = 15
        # endJ = 14
        # self.dotsGroup.add(Ellipse(endJ* 32 + 5, endI* 32 + 5, WHITE, 24, 24))
        # copiedList = listOfXY.copy()
        # listOfDotsForPath = []
        # listOfDotsForPath.append(copiedList[playerPosition])
        # copiedList.remove(copiedList[playerPosition])
        # listOfXY.remove(listOfXY[playerPosition])
        # # #проходження через точки
        # # amount = 4
        # amount = len(listOfXY)
        # for i in range(amount):
        #     foodPosition = random.randint(0, len(copiedList)-1)
        #     self.dotsGroup.add(Ellipse(copiedList[foodPosition][1]* 32 + 5, copiedList[foodPosition][0]* 32 + 5, WHITE, 24, 24))
        #     listOfDotsForPath.append(copiedList[foodPosition])
        #     copiedList.remove(copiedList[foodPosition])
        #вимірювання часу виконання пошуку
        #startTime = datetime.now()
        #виконання обраного пошуку шляху
        #self.pathGroup = bfs(startI, startJ, endI, endJ)
        #self.pathGroup = pathForDfs(startI, startJ, endI, endJ)
        #self.pathGroup = ucs(grid, startI, startJ, endI, endJ)
        #self.pathGroup = aStar(grid, startI, startJ, endI, endJ)
        #self.pathGroup = pathThroughDots(grid, listOfDotsForPath)
        #endTime = datetime.now() - startTime
        #вивід списку точок, з яких складається шлях, та часу виконання
        # print([i[::-1] for i in self.pathGroup[::-1]])
        #print("Time: ", endTime)
        self.algorithm = minOrExpMax.minimax
        self.bestNextPosition = self.algorithm(grid,self.player,self.enemies,self.dotsGroup)
        self.startTimeGame = datetime.now()


    def processEvents(self):
        if self.gameOver == True:
            return True
        #метод для зчитування подій, тобто дій гравця, таких як креування гравцем за допомогою клавіатури
        #якщо гравець зробив хоч щось відбувається наступне:
        for event in pygame.event.get(): 
            #якщо гравець натиснув на клавішу "вийти", гра завершується
            if event.type == pygame.QUIT:
                return True
            #якщо гравець натис будь-яку клавішу клавіатури, відбувається зчитування, яка саме клавіша задіяна
            if event.type == pygame.KEYDOWN:
                if self.player.gameControled == False:
                    #при натисанні клавіші праворуч, ліворуч, вгору чи вниз відбувається рух гравця у відповідному напрямку
                    if event.key == pygame.K_RIGHT:
                        self.player.moveRight()
                    elif event.key == pygame.K_LEFT:
                        self.player.moveLeft()
                    elif event.key == pygame.K_UP:
                        self.player.moveUp()
                    elif event.key == pygame.K_DOWN:
                        self.player.moveDown()
                    #при натисканні клавіші "ESCAPE" відбувається завершення гри
                    elif event.key == pygame.K_ESCAPE:
                        self.gameOver = True

            #якщо гравець відпускає клавішу клавіатури відбувається наступне:
            elif event.type == pygame.KEYUP:
                #при відпусканні клавіші праворуч, ліворуч, вгору чи вниз припиняється рух гравця у відповідному напрямку
                if event.key == pygame.K_RIGHT:
                    self.player.stopMoveRight()
                elif event.key == pygame.K_LEFT:
                    self.player.stopMoveLeft()
                elif event.key == pygame.K_UP:
                    self.player.stopMoveUp()
                elif event.key == pygame.K_DOWN:
                    self.player.stopMoveDown()
        return False

    def runLogic(self):
        #метод, що забезпечує процес проходу гри
        if not self.gameOver:
            #доки статус гри "не завершено", відбувається оновлення стану гравця, його розташування
            self.player.update(self.blocksGroup)
            #при кожному зіткненні гравця з їжею відбувається зарахування балу для гравця та зникнення їжі
            dotsHitList = pygame.sprite.spritecollide(self.player,self.dotsGroup,True)
            if len(dotsHitList) > 0:
                self.score += 1
            #якщо на полі не залишилось їжі, то гру завершено
            if len(self.dotsGroup) == 0:
                self.status = True
                self.player.explosion = True
            #якщо гравцеь стикаєтьсяз ворогом, відбувається вибух гравця та завершення гри, зміна статусу гри на "завершено"
            blockHitList = pygame.sprite.spritecollide(self.player,self.enemies,False)
            if len(blockHitList) > 0:
                self.player.explosion = True 
            self.gameOver = self.player.gameOver
    
            randIndex = random.randint(0, self.pathDotsCount)
            for ghost in self.randGhosts:
                currentPosition = ghost.currentPos
                if len(ghost.path) == 0:
                    for i, row in enumerate(grid):
                        for j, item in enumerate(row):
                            if(randIndex != 0):
                                randIndex -= 1
                                currentPosition = (j, i)
                ghost.update(currentPosition)

            for ghost in self.followingGhosts:
                currentPosition = ((self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32)
                ghost.update(currentPosition)

            if self.player.controlByGame:
                if self.player.isGoingByGame == False:
                    self.bestNextPosition = self.algorithm(grid,self.player,self.enemies,self.dotsGroup)
                    self.player.isGoingByGame = True
                self.player.playerRun(self.bestNextPosition)
        else:
            info = [self.status, datetime.now() - self.startTimeGame, self.score, self.algorithm.__name__]
            with open('statistics.csv', 'a', encoding='UTF8') as file:
                writer = csv.writer(file)
                writer.writerow(info)

    def displayFrame(self,screen):
        #метод створення екрану гри, зображення поля, необхідних спрайтів, груп, текстів  тощо
        screen.fill(BLACK)
        drawEnviroment(screen)
        self.dotsGroup.draw(screen)
        self.enemies.draw(screen)
        #зображення знайденого шляху на полі
        #drawPath(self, self.pathGroup, screen, True)
        screen.blit(self.player.image,self.player.rect)
        text = self.font.render("Score: " + str(self.score),True,GREEN)
        screen.blit(text,[180,10])
        pygame.display.flip()