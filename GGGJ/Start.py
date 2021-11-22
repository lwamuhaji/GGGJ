from os import X_OK, link
import pygame as pg
from tkinter import *
from Setting import *
from Class import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption('Game Title')
        self.clock = pg.time.Clock()
        self.running = True
    #게임을 시작할 때 필요한 것들
    def new(self):
        self.score1 = 0
        self.score2 = 0
        self.allSprite = pg.sprite.Group()
        self.playerSprite = pg.sprite.Group()
        self.coinSprite = pg.sprite.Group()
        self.rockSprite = pg.sprite.Group()
        self.player1 = Player(self, 'resources\Player1.png', SCREEN_WIDTH/20, SCREEN_HEIGHT/2)
        self.player2 = Player(self, 'resources\Player2.png', SCREEN_WIDTH/20*19, SCREEN_HEIGHT/2)
        #스프라이트 그룹 형성
        for i in range(COIN_COUNT):
            self.coin = Coin()
            self.allSprite.add(self.coin)
            self.coinSprite.add(self.coin)
        for i in range(ROCK_COUNT):
            self.rock = Items(self)
            self.allSprite.add(self.rock)
            self.rockSprite.add(self.rock)
        self.allSprite.add(self.player1, self.player2)
        self.playerSprite.add(self.player1, self.player2)
        
        self.run()
    #게임 실행 부분 코드
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
    #키 이벤트
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: #유저가 닫기 누르면 꺼짐
                pg.quit()
            if event.type == pg.KEYDOWN:  #누르고 있는 동안 움직임
                if event.key == pg.K_ESCAPE: #ESC누르면 꺼짐
                    pg.quit()
                #1P 움직임
                if event.key == pg.K_d:
                    self.player1.dx = SPEED1
                if event.key == pg.K_a:
                    self.player1.dx = -SPEED1
                if event.key == pg.K_s:
                    self.player1.dy = SPEED1
                if event.key == pg.K_w:
                    self.player1.dy = -SPEED1
                #2P 움직임
                if event.key == pg.K_RIGHT:
                    self.player2.dx = SPEED2
                if event.key == pg.K_LEFT:
                    self.player2.dx = -SPEED2
                if event.key == pg.K_DOWN:
                    self.player2.dy = SPEED2
                if event.key == pg.K_UP:
                    self.player2.dy = -SPEED2
            if event.type == pg.KEYUP:
                #1P 멈춤
                if event.key == pg.K_d:
                    self.player1.dx = 0
                if event.key == pg.K_a:
                    self.player1.dx = 0
                if event.key == pg.K_s:
                    self.player1.dy = 0
                if event.key == pg.K_w:
                    self.player1.dy = 0
                #2P 멈춤
                if event.key == pg.K_RIGHT:
                    self.player2.dx = 0
                if event.key == pg.K_LEFT:
                    self.player2.dx = 0
                if event.key == pg.K_DOWN:
                    self.player2.dy = 0
                if event.key == pg.K_UP:
                    self.player2.dy = 0
    #매 프레임 갱신해야하는 것들    
    def update(self):
        self.allSprite.update()
        self.player1.move()
        self.player2.move()
        #운석 이동
        for rock in self.rockSprite:
            rock.rect.x += rock.dx
            rock.rect.y += rock.dy
            if rock.rect.top >= SCREEN_HEIGHT:
                rock.kill()
        #코인 충돌 감지
        if pg.sprite.spritecollide(self.player1, self.coinSprite, True):
            self.score1 += 10
        if pg.sprite.spritecollide(self.player2, self.coinSprite, True):
            self.score2 += 10
        #운석 충돌 감지
        if pg.sprite.spritecollide(self.player1, self.rockSprite, True):
            self.score1 -= 10
        if pg.sprite.spritecollide(self.player2, self.rockSprite, True):
            self.score2 -= 10
        #코인 재성성
        while len(self.coinSprite) < 5:
            coin = Coin()
            self.allSprite.add(coin)
            self.coinSprite.add(coin)  
        #운석 재성성
        while len(self.rockSprite) < 5:
            rock = Items(self)
            self.allSprite.add(rock)
            self.rockSprite.add(rock)
    #화면에 출력    
    def draw(self):
        self.screen.fill(BLACK)
        self.allSprite.draw(self.screen)
        self.timer()
        self.drawScore()
        pg.display.flip()
    #타이머
    def timer(self):
        elapsed_time = (pg.time.get_ticks() - self.time) / 1000   
        self.drawText("timer: " + str(int(total_time - elapsed_time)), 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/12)
        if total_time - elapsed_time <= 0:
            self.time = 0
            self.showEnd()
    #시작화면과 결과창에서 키입력 감지
    def wait_for_key(self):
        waiting = True
        while waiting:
            waiting = True
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False
                    self.time = pg.time.get_ticks()
    #시작화면 출력
    def showStartScreen(self):
        self.screen.fill(BLACK)
        self.drawBg()
        self.drawText("Game Title", 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/6)
        self.drawText("Press a key to play", 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/6*5)
        pg.display.flip()
        self.wait_for_key()
    #결과창 출력
    def showEnd(self):
        self.screen.fill(BLACK)
        if not isActive:
            return
        self.drawText("Game End", 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/6)
        if self.score1 > self.score2:
            self.drawText("1P WIN!", 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
        elif self.score1 == self.score2:
            self.drawText("draw...", 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
        else:
            self.drawText("2P WIN!", 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
        self.drawText("Press a key to play again", 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/6*5)
        
        pg.display.flip()
        self.reset()
        self.wait_for_key()
    #재시작시 리셋    
    def reset(self):
        self.score1 = 0
        self.score2 = 0
        self.player1.rect.midtop = (SCREEN_WIDTH/20, SCREEN_HEIGHT/2)
        self.player2.rect.midtop = (SCREEN_WIDTH/20*19, SCREEN_HEIGHT/2)
    #점수 출력
    def drawScore(self):
        self.drawText("1P score : " + str(self.score1), 30 ,WHITE, SCREEN_WIDTH/12, SCREEN_WIDTH/12)
        self.drawText("2P score : " + str(self.score2), 30 ,WHITE, SCREEN_WIDTH/12*11, SCREEN_WIDTH/12)
    #배경 출력
    def drawBg(self):
        background = pg.image.load("resources\\background.jpg")
        backgroundRect = background.get_rect()
        self.screen.blit(background, backgroundRect)
    #텍스트 출력
    def drawText(self, text, size, color, x, y):
        font = pg.font.Font("resources\\andante.ttf", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.showStartScreen()

while g.running:
    g.new()
    g.showEnd()


pg.quit()