import pygame
from enemies import *

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREEN_WIDTH = 672
SCREEN_HEIGHT = 640

#визначення кольорів для подальшого використання
BLACK = (0,0,0)
WHITE = (255,255,255)

#клас гравець - пакмен
class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    explosion = False
    game_over = False
    def __init__(self,x,y,filename):
        #ініціація створення спрайта гравця, задання кольору,розташування, додаткових спрайтів тощо
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y) # початкове положення гравця
        #спрайт та налаштування анімації ходьби
        img = pygame.image.load("walk.png").convert()
        self.move_right_animation = Animation(img,32,32)
        self.move_left_animation = Animation(pygame.transform.flip(img,True,False),32,32)
        self.move_up_animation = Animation(pygame.transform.rotate(img,90),32,32)
        self.move_down_animation = Animation(pygame.transform.rotate(img,270),32,32)
        #спрайт та налаштування анімації вибуху
        img = pygame.image.load("explosion.png").convert()
        self.explosion_animation = Animation(img,30,30)
        #збереження зображення гравця
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)

    def update(self,horizontal_blocks,vertical_blocks, blocks_group):
        #метод запобішання перетину перешкод гравцем
        if not self.explosion:
            #перешкоджання гравецеві проходити крізь стіни всередині поля
            for block in pygame.sprite.spritecollide(self,blocks_group,False):
                self.rect.x -= (block.rect.x - self.rect.x)*0.1
                self.rect.y -= (block.rect.y - self.rect.y)*0.1
                self.change_x = 0
                self.change_y = 0
            #перешкоджання гравцеві виходити за межі поля
            if self.rect.right <= 30:
                self.rect.left = 2
            if self.rect.left >= SCREEN_WIDTH - 30:
                self.rect.right = SCREEN_WIDTH - 2
            if self.rect.bottom <= 30:
                self.rect.top = 2
            if self.rect.top >= SCREEN_HEIGHT - 30:
                self.rect.bottom = SCREEN_HEIGHT - 2
            #зміна та збереження координатів гравця
            self.rect.x += self.change_x
            self.rect.y += self.change_y
            #заборона на спробу перетнути лінії вздовж дозволеної траекторії ходьби
            for block in pygame.sprite.spritecollide(self,horizontal_blocks,False):
                self.rect.centery = block.rect.centery
                self.change_y = 0
            for block in pygame.sprite.spritecollide(self,vertical_blocks,False):
                self.rect.centerx = block.rect.centerx
                self.change_x = 0
            #ініціація виконання анімацій
            if self.change_x > 0:
                self.move_right_animation.update(10)
                self.image = self.move_right_animation.get_current_image()
            elif self.change_x < 0:
                self.move_left_animation.update(10)
                self.image = self.move_left_animation.get_current_image()

            if self.change_y > 0:
                self.move_down_animation.update(10)
                self.image = self.move_down_animation.get_current_image()
            elif self.change_y < 0:
                self.move_up_animation.update(10)
                self.image = self.move_up_animation.get_current_image()
        else:
            #ініціація анімації вибуху та закінчення гри для гравця
            if self.explosion_animation.index == self.explosion_animation.get_length() -1:
                pygame.time.wait(500)
                self.game_over = True
            self.explosion_animation.update(12)
            self.image = self.explosion_animation.get_current_image()
            
    #зміна координатів гравця в залежності від команди
    def move_right(self):
        self.change_x = 3

    def move_left(self):
        self.change_x = -3

    def move_up(self):
        self.change_y = -3

    def move_down(self):
        self.change_y = 3
    
    #припинення руху гравця на полі
    def stop_move_right(self):
        if self.change_x != 0:
            self.image = self.player_image
        self.change_x = 0

    def stop_move_left(self):
        if self.change_x != 0:
            self.image = pygame.transform.flip(self.player_image,True,False)
        self.change_x = 0

    def stop_move_up(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image,90)
        self.change_y = 0

    def stop_move_down(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image,270)
        self.change_y = 0

#клас анімацій (базових їх налаштувань)
class Animation(object):
    def __init__(self,img,width,height):
        # ініціація створення аніманції
        #завантаження спрайту
        self.sprite_sheet = img
        #створення списку зображень
        self.image_list = []
        self.load_images(width,height)
        #стоврення змінної, що визначатиме порядок аніманцій
        self.index = 0
        #створення змінної, що визначатиме час роботи програми в необхідних завданнях
        self.clock = 1
        
    def load_images(self,width,height):
        #завантаження та перебір всіх вказаних зображень
        for y in range(0,self.sprite_sheet.get_height(),height):
            for x in range(0,self.sprite_sheet.get_width(),width): 
                # load images into a list
                img = self.get_image(x,y,width,height)
                self.image_list.append(img)

    def get_image(self,x,y,width,height):
        #отримання, створення та відображення готового спрайта
        image = pygame.Surface([width,height]).convert()
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        image.set_colorkey((0,0,0))
        return image

    def get_current_image(self):
        #визначення спрайта, що задіяний
        return self.image_list[self.index]

    def get_length(self):
        #повернення довжини списку зображень
        return len(self.image_list)

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
            if self.index == len(self.image_list):
                self.index = 0

            
    
        
