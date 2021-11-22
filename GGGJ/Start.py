from os import X_OK, link
import pygame as pg
import time
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
        self.bgmusic = pg.mixer.Sound("resources\\bgmusic.mp3")
        self.online = False
        self.bgmusic.play(-1)
    #게임을 시작할 때 필요한 것들
    def new(self):
        self.score1 = 0
        self.score2 = 0
        self.coinsound = pg.mixer.Sound("resources\coinGet.mp3")
        self.hitsound = pg.mixer.Sound("resources\hit.mp3")
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
        
        self.startCountdown()
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
        #플레이어 이동
        self.player1.move()
        self.player2.move()
        #운석 이동
        for rock in self.rockSprite:
            rock.moveRock()
            if rock.rect.top >= SCREEN_HEIGHT:
                rock.kill()
        #코인 충돌 감지
        if pg.sprite.spritecollide(self.player1, self.coinSprite, True):
            self.score1 += 10
            self.coinsound.play()
        if pg.sprite.spritecollide(self.player2, self.coinSprite, True):
            self.score2 += 10
            self.coinsound.play()
        #운석 충돌 감지
        if pg.sprite.spritecollide(self.player1, self.rockSprite, True):
            self.score1 -= 10
            self.hitsound.play()
        if pg.sprite.spritecollide(self.player2, self.rockSprite, True):
            self.score2 -= 10
            self.hitsound.play()
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
        self.drawText("time: " + str(int(total_time - elapsed_time)), 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/12)
        if total_time - elapsed_time <= 0:
            self.playing = False
    #시작화면과 결과창에서 키입력 감지
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        waiting = False
                        self.showCheckScreen()
    #로컬 멀티인지 온라인인지 확인
    def isOnline(self):
        checking = True
        while checking:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_y:
                        checking = False
                        self.online = True
                    if event.key == pg.K_n:
                        checking = False
                        self.online = False
    #게임 시작 카운트 다운
    def startCountdown(self):
        sec = 3
        while sec:
            self.screen.fill(BLACK)
            self.drawText(str(sec), 50, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            pg.display.flip()
            time.sleep(1)
            sec -= 1
        self.time = pg.time.get_ticks()
    #시작화면 출력
    def showStartScreen(self):
        self.screen.fill(BLACK)
        self.drawBg("resources\\background.jpg")
        self.drawText("Game Title", 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/6)
        self.drawText("Press 'spacebar' to play", 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/6*5)
        pg.display.flip()
        self.wait_for_key()
    #로컬 멀티 / 온라인 확인 화면 출력
    def showCheckScreen(self):
        self.screen.fill(BLACK)
        self.drawImage("resources\Online.png", (300,300), SCREEN_WIDTH/4, SCREEN_HEIGHT/4)
        self.drawImage("resources\Local.png", (300,300), SCREEN_WIDTH/4*3, SCREEN_HEIGHT/4)
        self.drawText("Online 2p play press 'y'", 30, WHITE, SCREEN_WIDTH/4, SCREEN_HEIGHT/6*5)
        self.drawText("Local 2p play press 'n'", 30, WHITE, SCREEN_WIDTH/4*3, SCREEN_HEIGHT/6*5)
        pg.display.flip()
        self.isOnline()
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
        self.drawText("Press 'spacebar' to play again", 30, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/6*5)
        
        pg.display.flip()
        self.reset()
        self.wait_for_key()
    #재시작시 리셋    
    def reset(self):
        self.time = 0
        self.score1 = 0
        self.score2 = 0
        self.player1.dx = 0
        self.player1.dy = 0
        self.player2.dx = 0
        self.player2.dy = 0
        self.player1.rect.midtop = (SCREEN_WIDTH/20, SCREEN_HEIGHT/2)
        self.player2.rect.midtop = (SCREEN_WIDTH/20*19, SCREEN_HEIGHT/2)
    #점수 출력
    def drawScore(self):
        self.drawText("1P score : " + str(self.score1), 30 ,WHITE, SCREEN_WIDTH/12, SCREEN_WIDTH/12)
        self.drawText("2P score : " + str(self.score2), 30 ,WHITE, SCREEN_WIDTH/12*11, SCREEN_WIDTH/12)
    #이미지 출력
    def drawImage(self, path, size, x, y):
        image = pg.image.load(path)
        image = pg.transform.scale(image, size)
        imageRect = image.get_rect()
        imageRect.midtop = (x, y)
        self.screen.blit(image, imageRect)
    #배경 출력
    def drawBg(self, path):
        background = pg.image.load(path)
        backgroundRect = background.get_rect()
        self.screen.blit(background, backgroundRect)
    #텍스트 출력
    def drawText(self, text, size, color, x, y):
        font = pg.font.Font("resources\\andante.ttf", size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (x, y)
        self.screen.blit(textSurface, textRect)

g = Game()
g.showStartScreen()

while g.running:
    g.new()
    g.showEnd()

pg.quit()
