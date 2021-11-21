import pygame
from pygame.rect import *

    
def eventProcess():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #유저가 닫기 누르면 꺼짐
            pygame.quit()
        if event.type == pygame.KEYDOWN:  #누르고 있는 동안 움직임
            if event.key == pygame.K_ESCAPE: #ESC누르면 꺼짐
                pygame.quit()

            if event.key == pygame.K_w:
                move.y = -1
            if event.key == pygame.K_s:
                move.y = 1
            if event.key == pygame.K_a:
                move.x = -1
            if event.key == pygame.K_d:
                move.x = 1

        if event.type == pygame.KEYUP:  #키에서 손때면 멈춤
            if event.key == pygame.K_w:
                move.y = 0
            if event.key == pygame.K_s:
                move.y = 0
            if event.key == pygame.K_a:
                move.x = 0
            if event.key == pygame.K_d:
                move.x = 0
        
                
def movePlayer1():
    recP1.x += move.x
    recP1.y += move.y

    #플레이어 행동 반경 설정
    if recP1.x < 0:
        recP1.x = 0
    if recP1.y < 0:
        recP1.y = 0

    if recP1.x > SCRREN_WIDTH-recP1.width:
        recP1.x = SCRREN_WIDTH-recP1.width
    if recP1.y > SCRREN_HEIGHT-recP1.height:
        recP1.y = SCRREN_HEIGHT-recP1.height
        

    screen.blit(Player1, recP1)
    
#쓰이는 색 정리
BLACK= ( 0,  0,  0)
WHITE= (255,255,255)
BLUE = ( 0,  0,255)
GREEN= ( 0,255,  0)
RED  = (255,  0,  0)

#변수 초기화
SCRREN_WIDTH = 1200
SCRREN_HEIGHT = 960
move = Rect(0,0,0,0)
done = True
clock = pygame.time.Clock()

#스크린 생성
pygame.init
screen = pygame.display.set_mode((SCRREN_WIDTH, SCRREN_HEIGHT))
pygame.display.set_caption('Game Title')

#플레이어 1 생성
Player1 = pygame.image.load('resources\Player1.png')
Player1 = pygame.transform.scale(Player1,(150,150))
recP1 = Player1.get_rect()
recP1.centerx = (SCRREN_WIDTH/2)
recP1.centery = (SCRREN_HEIGHT/2)

#메인 이벤트 루프
while done:
    #화면 지움
    screen.fill(WHITE)  
    #이벤트 처리
    eventProcess()
    #플레이어 1 이동
    movePlayer1()
    #화면 갱신
    pygame.display.flip()
    clock.tick(300)
