import pygame as pg
import random
from Setting import *
from tkinter import *

#Player class 생성
class Player(pg.sprite.Sprite):
    def __init__(self, game, link, x, y, dx=0, dy=0):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(link)
        self.image = pg.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect()
        self.dx = dx
        self.dy = dy
        self.rect.midtop = (x, y)
        
     # 좌표 이동
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        if self.rect.right > SCREEN_WIDTH or self.rect.x < 0:
            self.rect.x -= self.dx
        if self.rect.bottom > SCREEN_HEIGHT or self.rect.y < 0:
            self.rect.y -= self.dy

#Coin class 생성
class Coin(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('resources\coin.png')
        self.image = pg.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH/5, SCREEN_WIDTH/5*4)
        self.rect.y = random.randrange(SCREEN_HEIGHT/5, SCREEN_HEIGHT/5*4)
        

#Items class 생성
class Items(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load('resources\\rock.png')
        self.image = pg.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH/5, SCREEN_WIDTH/5*4)
        self.rect.y = random.randrange(-150, -50)
        