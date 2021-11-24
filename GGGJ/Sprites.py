import pygame as pg
import random
import os
from Setting import *

random.seed(1)

#Player class 생성
class Player(pg.sprite.Sprite):
    def __init__(self, game, link, x, y, dx=0, dy=0):
        pg.sprite.Sprite.__init__(self)
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.game = game
        self.image = pg.image.load(link)
        self.image = pg.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect()
        self.dx = dx
        self.dy = dy
        self.rect.midtop = (x, y)
        
     #플레이어 좌표 이동
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        #스크린 밖으로 안나가도록  설정
        if self.rect.right > SCREEN_WIDTH or self.rect.x < 0:
            self.rect.x -= self.dx
        if self.rect.bottom > SCREEN_HEIGHT or self.rect.y < 0:
            self.rect.y -= self.dy

#Coin class 생성
class Coin(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image = pg.image.load(self.path + '\\resources\\coin.png')
        self.image = pg.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH/5, SCREEN_WIDTH/5*4)    #coin x좌표 랜덤 설정
        self.rect.y = random.randrange(SCREEN_HEIGHT/5, SCREEN_HEIGHT/5*4)  #coin y좌표 랜덤 설정
        

#Items class 생성
class Items(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.game = game
        self.image = pg.image.load(self.path + '\\resources\\rock.png')
        self.image = pg.transform.scale(self.image,(75,75))
        self.rect = self.image.get_rect()
        self.dx = random.randrange(-2, 2)   #운석 x좌표 속도 랜덤 설정
        self.dy = random.randrange(3, 7)    #운석 y좌표 속도 랜덤 설정
        self.rect.x = random.randrange(SCREEN_WIDTH/5, SCREEN_WIDTH/5*4)    #운석 x좌표 랜덤 설정
        self.rect.y = random.randrange(-150, -50)                           #운석 y좌표 랜덤 설정
    
    
    def moveRock(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
