import csv
import numpy as np
import pygame
from DQNAgent import Agent
from game import Game, WHITE
from minOrExpMax import getNearestFood
from enemies import Ellipse

ACTIONS = 4 #кількість можливих ходів: 0:вгору, 1:вниз, 2:праворуч, 3:ліворуч
STATECOUNT = 6 #кількість станів, що передаються
GAME_Cycles = 500 #кількість ітерацій для тренування

SCREENWIDTH = 160
SCREENHEIGHT = 160

#тренувальне поле
grid =           ((1,1,1,1,1),
                 (1,0,1,0,1),
                 (1,1,1,1,1),
                 (1,0,1,0,1),
                 (1,1,1,1,1))

#метод нормалізації станів 
def CaptureNormalisedState(playerXPos, playerYPos, ghostXpoz, ghostYpoz, nearestFoodX,nearestFoodY):
    gstate = np.zeros([STATECOUNT])
    gstate[0] = playerXPos / 10.0
    gstate[1] = playerYPos / 10.0
    gstate[2] = ghostXpoz / 10.0
    gstate[3] = ghostYpoz / 10.0
    gstate[4] = nearestFoodX / 10.0
    gstate[5] = nearestFoodY / 10.0
    return gstate


#метод тренувального процесу
def RunProcces():

    #створення агента гри
    TheAgent = Agent(STATECOUNT, ACTIONS)

    BestAction = 0

    #створення списку для їжі на полі
    dotsGroup = pygame.sprite.Group()

    # створення та додавання "їжі" на поле
    listOfXY = []
    pathDotsCount = 0
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item != 0:
                # заповнення списку точок, де можливе розташування їжі
                coordinates = [i, j]
                listOfXY.append(coordinates)
                pathDotsCount = pathDotsCount + 1
                # заповнення списку їжі
                dotsGroup.add(Ellipse(j * 32 + 12, i * 32 + 12, WHITE, 8, 8))

    #пошук координтатів найближчої їжі
    nearestFood = getNearestFood([0, 0],dotsGroup)
    
    #задання станів
    GameState = CaptureNormalisedState(0, 0, 2, 2,nearestFood[0],nearestFood[1])

    #задання початкового рахунку для гри
    globalScore = 0

    for gameTime in range(GAME_Cycles):

        #ініціація гри та середовища
        pygame.init()
        screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("PACMAN")
       
        clock = pygame.time.Clock()

        #змінна для підтвердження, що тренування виконане
        done = False

        #створення об'єкта гри
        game = Game()
        game.__init__()
        game.gameOver = False

        #цикл тренування
        while not done:
            
            done = game.processEvents()

            isPossibleToMove = not game.player.isGoingByGame
            if(isPossibleToMove):
                BestAction = TheAgent.Act(GameState)
                [localScore, playerXPos, playerYPos, nearestEnemy, nearestFood] = game.PlayerNextMove(BestAction)
                globalScore += localScore

                NextState = CaptureNormalisedState(playerXPos, playerYPos, nearestEnemy[0], nearestEnemy[1], nearestFood[0],nearestFood[1])

                #передача наступних станів для наступної ітерації
                TheAgent.CaptureSample((GameState, BestAction, globalScore, NextState))
                TheAgent.Process()
                GameState = NextState

                #зображення розвитку тренування у консолі
                print(f"Global score for training: {globalScore} Epsilon value:  {TheAgent.epsilon}")

                #запис історії до файлу
                with open('historyOfTraining.csv', 'a', encoding='UTF8') as file:
                    data = [f"score: {globalScore}", f"epsilon: {TheAgent.epsilon}"]
                    writer = csv.writer(file)
                    writer.writerow(data)

            #операції з нагородою для навчання гравця
            if(game.gameOver and game.status):
                globalScore += 500
            elif(game.gameOver and not game.status):
                globalScore -= 100

            #логіка гри
            game.runLogic()

            #зображення середовища
            game.displayFrame(screen)
           
            #кількість кадрів в секунду
            clock.tick(1000)

#запуск тренування
RunProcces()