import pygame
from game import Game

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREENWIDTH = 672
SCREENHEIGHT = 640

def main():
    # ініціація всього процесу запуску гри
    pygame.init()
    screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    pygame.display.set_caption("PACMAN")
    #запуск нескінченного процесу, доки користувач не закриє вікно гри
    done = False
    clock = pygame.time.Clock()
    #створення ігрового об'єкту
    game = Game()
    while not done:
        #доки гравець не вийде з гри, відбувається зчитування його дій (натискання на клавіші тощо)
        done = game.processEvents()
        #запуск роботи гри, її логічного процесу
        game.runLogic()
        #створення графіки та самого екрану гри
        game.displayFrame(screen)
        clock.tick(30)
    #після завершення гравцем гри, відбувається вихід з неї
    pygame.quit()

if __name__ == '__main__':
    main()
