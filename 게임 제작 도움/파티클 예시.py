#-*- coding:utf-8 -*-
import pygame as pg, os, time, random, math, sys
from pygame.locals import *
from 함수 import *

pg.init()

#기본 세팅
screen_width = 1200
screen_height = 800
screen = pg.display.set_mode([screen_width,screen_height])
pg.display.set_caption("None")

background_color = (140,140,140)
black = (0,0,0)
white = (255,255,255)

clock = pg.time.Clock()
done = False

#폰트
gamefont = ['한컴산뜻돋움','nanumgothic','hy견고딕','gulim']
for f in gamefont:
    for i in pg.font.get_fonts():
        if f == i:
            try:gamefont = gamefont[gamefont.index(f)]
            except:pass
            break

change_dir('.')

#전역 변수
    #파일
assets = resource_path('assets')

volume_modify_max = 10
volume_modify = 3

spawnTime = 5
spawnTimeRate = 0

#튀는 효과 
class SplashParticle:
    def __init__(self) -> None:
        self.objects = []

    def Spawn(self,count:int,start:tuple,endY,xSpeed:tuple,ySpeed:tuple,decreaseSpeed:tuple,\
                color:tuple,size:tuple,sizeChangeRate,isBlend:bool,blendColor:tuple):
        """
        ☆ 인덱스 번호 및 작성법 ☆
            start[0] endY[1] xSpeed[2] ySpeed[3] downSpeed[4] 
            color[5] size[6] sizeChangeRate[7] isBlend[8] blendColor[9]
             여기에서
            start(x,y), xSpeed(최소,최대)/10, ySpeed(최소,최대)/10, decreaseSpeed(x,y), size(최소,최대)
        """
        for i in range(count):
            self.objects.append([list(start),endY,random.randint(xSpeed[0],xSpeed[1])/10,random.randint(ySpeed[0],ySpeed[1])/10,\
                        decreaseSpeed,color,random.randint(size[0],size[1]),sizeChangeRate,isBlend,blendColor])
    
    def Draw(self,surface):
        for i in self.objects:
            if i[8] == True:
                radius = i[6] * 1.7
                surface.blit(circle_surf(radius, i[9]), (int(i[0][0] - radius), int(i[0][1] - radius)), special_flags=BLEND_RGB_ADD)
            pg.draw.circle(surface,i[5],(i[0][0],i[0][1]),i[6])

    def Update(self):
        for i in self.objects:
            if i[0][1]+i[6] >= i[1] or i[6] <= 0:
                self.objects.remove(i)
            else:
                i[0][0] += i[2]
                i[0][1] -= i[3]
                i[2] -= i[4][0]
                i[3] -= i[4][1]
                i[6] -= i[7]  

#퍼지는 효과
class SpreadParticle:
    def __init__(self) -> None:
        self.objects = []

    def Spawn(self,count:int,start:tuple,speed:tuple,speedDecrease,degree:tuple,duration:tuple,\
                color:tuple,size:tuple,sizeChangeRate,isBlend:bool,blendColor:tuple):
        """
        ☆ 인덱스 번호 및 작성법 ☆
            start[0] speedDecrease[1] dx[2] dy[3] result_duration[4] color[5]
            result_size[6] sizeChange[7] isBlend[8] blendColor[9]
        """
        for i in range(count):
            result_speed = random.randint(speed[0],speed[1])
            result_duration = random.randint(duration[0],duration[1])
            result_size = random.randint(size[0],size[1])
            angle = math.radians(random.randint(-degree[1],-degree[0]))
            dx = math.cos(angle)*result_speed
            dy = math.sin(angle)*result_speed

            self.objects.append([list(start),speedDecrease,dx,dy,result_duration,color,result_size,sizeChangeRate,
                                 isBlend,blendColor])

    def Draw(self,surface):
        for i in self.objects:
            if i[8] == True:
                radius = i[6] * 1.7
                surface.blit(circle_surf(radius, i[9]), (int(i[0][0] - radius), int(i[0][1] - radius)), special_flags=BLEND_RGB_ADD)
            pg.draw.circle(surface,i[5],(i[0][0],i[0][1]),i[6])

    def Update(self):
        for i in self.objects:
            if i[4]<=0 or i[6] < 0:
                self.objects.remove(i)
            else:
                i[0][0] += i[2]
                i[0][1] += i[3]
                i[2] *= i[1]
                i[3] *= i[1]
                i[6] -= i[7]
                i[4] -= 1  
    
splashParticle = SplashParticle()
spreadParticle = SpreadParticle()

while not done:
    screen.fill(black)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True

    if spawnTimeRate >= spawnTime:
        splashParticle.Spawn(1,(170,screen_height/2),screen_height/2+50,(-15,15),(40,50),(0,0.2),(255, 255, 255),(7,8),0.1,True,(140, 62, 0))
        splashParticle.Spawn(1,(370,screen_height/2),screen_height/2+50,(-15,15),(40,50),(0,0.2),(214, 36, 17),(6,11),0.1,False,(79, 75, 6))
        splashParticle.Spawn(1,(570,screen_height/2),screen_height/2+50,(-15,15),(40,50),(0,0.2),(255,255,255),(7,8),0.1,True,(105, 18, 150))
        splashParticle.Spawn(1,(770,screen_height/2),screen_height/2+50,(-15,15),(40,50),(0,0.2),(255, 232, 0),(6,11),0.1,True,(146, 66, 0))
        splashParticle.Spawn(1,(970,screen_height/2),screen_height/2+50,(-15,15),(40,50),(0,0.2),(198, 227, 22),(7,8),0.1,True,(101, 93, 0))
        
        spreadParticle.Spawn(1,(300,150),(2,3),0.97,(0,90),(60,120),(255, 249, 76),(7,8),0.07,True,(114, 112, 44))
        spreadParticle.Spawn(1,(600,150),(2,3),0.97,(-180,180),(60,120),(167, 214, 214),(7,8),0.1,True,(32, 140, 140))
        spawnTimeRate = 0
    spawnTimeRate += 1
    splashParticle.Update()
    splashParticle.Draw(screen)
    spreadParticle.Update()
    spreadParticle.Draw(screen)
    
    pg.display.flip()
    clock.tick(60)
pg.quit()