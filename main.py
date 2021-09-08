import pygame
from game import Game

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREEN_WIDTH = 672
SCREEN_HEIGHT = 640

def main():
    # ініціація всього процесу запуску гри
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("PACMAN")
    #запуск нескінченного процесу, доки користувач не закриє вікно гри
    done = False
    clock = pygame.time.Clock()
    #створення ігрового об'єкту
    game = Game()
    while not done:
        #доки гравець не вийде з гри, відбувається зчитування його дій (натискання на клавіші тощо)
        done = game.process_events()
        #запуск роботи гри, її логічного процесу
        game.run_logic()
        #створення графіки та самого екрану гри
        game.display_frame(screen)
        clock.tick(30)
    #після завершення гравцем гри, відбувається вихід з неї
    pygame.quit()

if __name__ == '__main__':
    main()
