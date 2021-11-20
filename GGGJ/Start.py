from os import X_OK, link
import sys
import pygame as pg
import random
import time


# 게임 화면 크기
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 960

#쓰이는 색 정리
BLACK= ( 0,  0,  0)
WHITE= (255,255,255)
BLUE = ( 0,  0,255)
GREEN= ( 0,255,  0)
RED  = (255,  0,  0)

# 기본 변수
COIN_COUNT = 5
PLAYER_COUNT = 2
SPEED1 = 5
SPEED2 = 5
SCORE1 = 0
SCORE2 = 0
clock = pg.time.Clock()
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
isActive = True
total_time = 180
start_ticks = pg.time.get_ticks()


# 오브젝트를 저장할 List
COINS = []
PLAYERS = []

class Player:
    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = ""
        
    def loadPlayer(self, link=''):
        self.image = pg.image.load(link)
        self.image = pg.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def drawPlayer(self):
        SCREEN.blit(self.image,[self.rect.x, self.rect.y])
        
     # x 좌표 이동
    def move_x(self):
        self.rect.x += self.dx

    # y 좌표 이동
    def move_y(self):
        self.rect.y += self.dy
        
    # 화면 밖으로 못 나가게 방지
    def checkScreen(self):        
        if self.rect.right > SCREEN_WIDTH or self.rect.x < 0:
            self.rect.x -= self.dx
        if self.rect.bottom > SCREEN_HEIGHT or self.rect.y < 0:
            self.rect.y -= self.dy
    def checkCollision(self, Coin, distance = 0):
        if (self.rect.top + distance < Coin.rect.bottom) and (Coin.rect.top < self.rect.bottom - distance) and (self.rect.left + distance < Coin.rect.right) and (Coin.rect.left < self.rect.right - distance):
            return True
        else:
            return False
    
    #최종 생성
    def start(self):
        self.drawPlayer()
        self.move_x()
        self.move_y()
        self.checkScreen()
    
#Coin class 생성
class Coin:
    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = ""
        
    def loadCoin(self):
        self.image = pg.image.load('resources\coin.png')
        self.image = pg.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH/5, SCREEN_WIDTH/5*4)
        self.rect.y = random.randrange(SCREEN_HEIGHT/5, SCREEN_HEIGHT/5*4)
    
    def drawCoin(self):
        SCREEN.blit(self.image, [self.rect.x, self.rect.y])
    
    def checkScreen(self):        
        if self.rect.right > SCREEN_WIDTH or self.rect.x < 0:
            self.rect.x -= self.dx
        if self.rect.bottom > SCREEN_HEIGHT or self.rect.y < 0:
            self.rect.y -= self.dy
        
    def checkCollision(self, Coin, distance = 0):
        if (self.rect.top + distance < Coin.rect.bottom) and (Coin.rect.top < self.rect.bottom - distance) and (self.rect.left + distance < Coin.rect.right) and (Coin.rect.left < self.rect.right - distance):
            return True
        else:
            return False
 
 # 3분 타이머
def timer():
    font = pg.font.SysFont("FixedSsy", 30, True, False)
    elapsed_time = (pg.time.get_ticks() - start_ticks) / 1000   
    timer = font.render("timer: " + str(int(total_time - elapsed_time)), True, (255,255,255))
    SCREEN.blit(timer, (SCREEN_WIDTH/3, SCREEN_HEIGHT/12))
    if total_time - elapsed_time <= 0:
        showEnd()
            
def wait_for_key():
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT: #유저가 닫기 누르면 꺼짐
                pg.quit()
            if event.type == pg.KEYDOWN:  #누르고 있는 동안 움직임
                if event.key == pg.K_ESCAPE: #ESC누르면 꺼짐
                    pg.quit()
            if event.type == pg.KEYUP:
                waiting = False
            

def showStartScreen():
    font = pg.font.SysFont("FixedSsy", 30, True, False)
    text_title = font.render("Game Title", True, WHITE)
    text_start = font.render("Press a key to play", True, WHITE)
    SCREEN.blit(text_title, [SCREEN_WIDTH/2, SCREEN_HEIGHT/6])
    SCREEN.blit(text_start, [SCREEN_WIDTH/2, SCREEN_HEIGHT/6*5])
    pg.display.flip()
    wait_for_key()

def showEnd():
    font = pg.font.SysFont("FixedSsy", 30, True, False)
    SCREEN.fill(BLACK)
    if not isActive:
        return
    
    text_over = font.render("Game End", True, WHITE)
    if SCORE1 > SCORE2:
        text_winner = font.render("1P WIN!", True, WHITE)
    elif SCORE1 == SCORE2:
        text_winner = font.render("Draw...", True, WHITE)
    else:
        text_winner = font.render("2P WIN!", True, WHITE)
    
    text_end = font.render("Press a key to play again", True, WHITE)
    SCREEN.blit(text_over, [SCREEN_WIDTH/2, SCREEN_HEIGHT/6])
    SCREEN.blit(text_winner, [SCREEN_WIDTH/2, SCREEN_HEIGHT/4])
    SCREEN.blit(text_end, [SCREEN_WIDTH/2, SCREEN_HEIGHT/4*3])
    pg.display.flip()
    
    wait_for_key()
        
 
def draw_score():
    # SCORE 기록
    global SCORE1, SCORE2
    font = pg.font.SysFont("FixedSsy", 30, True, False)
    text_score1 = font.render("1P score : " + str(SCORE1), True, WHITE)
    text_score2 = font.render("2P score : " + str(SCORE2), True, WHITE)
    SCREEN.blit(text_score1, [SCREEN_WIDTH/16, SCREEN_HEIGHT/12])
    SCREEN.blit(text_score2, [SCREEN_WIDTH/6*5, SCREEN_HEIGHT/12])
 
 
def main():
    # pygame 초기화 및 스크린 생성
    global SCREEN, COIN_COUNT, SCORE1, SCORE2, isActive
    pg.init()
    pg.display.set_caption('Game Title')
    
    player1 = Player(SCREEN_WIDTH/14,SCREEN_HEIGHT/2,0,0)
    player2 = Player((SCREEN_WIDTH/6)*5,SCREEN_HEIGHT/2,0,0)
    player1.loadPlayer('resources\Player1.png')
    player2.loadPlayer('resources\Player2.png')
    
    #코인 생성
    for i in range(COIN_COUNT):
        coin = Coin()
        coin.loadCoin()
        coin.checkScreen
        COINS.append(coin)
    
    showStartScreen()
        
    while isActive:
        for event in pg.event.get():
            if event.type == pg.QUIT: #유저가 닫기 누르면 꺼짐
                pg.quit()
            if event.type == pg.KEYDOWN:  #누르고 있는 동안 움직임
                if event.key == pg.K_ESCAPE: #ESC누르면 꺼짐
                    pg.quit()
                #1P 움직임
                if event.key == pg.K_d:
                    player1.dx = SPEED1
                if event.key == pg.K_a:
                    player1.dx = -SPEED1
                if event.key == pg.K_s:
                    player1.dy = SPEED1
                if event.key == pg.K_w:
                    player1.dy = -SPEED1
                #2P 움직임
                if event.key == pg.K_RIGHT:
                    player2.dx = SPEED2
                if event.key == pg.K_LEFT:
                    player2.dx = -SPEED2
                if event.key == pg.K_DOWN:
                    player2.dy = SPEED2
                if event.key == pg.K_UP:
                    player2.dy = -SPEED2
            if event.type == pg.KEYUP:
                #1P 멈춤
                if event.key == pg.K_d:
                    player1.dx = 0
                if event.key == pg.K_a:
                    player1.dx = 0
                if event.key == pg.K_s:
                    player1.dy = 0
                if event.key == pg.K_w:
                    player1.dy = 0
                #2P 멈춤
                if event.key == pg.K_RIGHT:
                    player2.dx = 0
                if event.key == pg.K_LEFT:
                    player2.dx = 0
                if event.key == pg.K_DOWN:
                    player2.dy = 0
                if event.key == pg.K_UP:
                    player2.dy = 0
        SCREEN.fill(BLACK)
        timer()
        #게임 코드

        #코인 생성
        for i in range(COIN_COUNT):
            COINS[i].drawCoin()
            
        #충돌 감지
        for i in range(COIN_COUNT):
            if player1.checkCollision(COINS[i], 0):
                COINS[i].loadCoin()
                SCORE1 += 10
            if player2.checkCollision(COINS[i], 0):
                COINS[i].loadCoin()
                SCORE2 += 10
        
        player1.start()
        player2.start()
        draw_score()
        pg.display.flip()
        
        # 초당 프레임 설정
        clock.tick(60)

if __name__ == '__main__':
    main()