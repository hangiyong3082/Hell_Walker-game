#-*- coding:utf-8 -*-
import pygame as pg, os, time, random, math, sys
from pygame.locals import *
from 함수 import *

#배경 파티클
class Particle:
    def __init__(self):
        self.objects = []
        self.color = (0,0,0)
        self.spawntime = 0
        self.VisibleTime = 240
        self.MaxAlpha = 150

    def spawn(self):
        if self.spawntime <= 0 and len(self.objects) <= 20:
            SideLength = random.randint(7,9)
            x_pos = random.randint(0,screen_width-SideLength)
            y_pos = random.randint(UIbar_height,screen_height-SideLength)
            dx = random.randrange(-100,100)/100
            dy = random.randrange(-100,100)/100
            c = random.randint(0,189)
            color = (c,c,c)
            self.spawntime = random.randint(0,30)
            self.objects.append([x_pos,y_pos,dx,dy,self.VisibleTime,0,SideLength,color])
        self.spawntime -= 1
    
    def Draw(self,surface):
        for i in self.objects:
            particle = AlphaRect(i[6],i[6],i[7],i[5])
            surface.blit(particle,(i[0],i[1]))

    def move(self,i):
        i[0] += i[2]
        i[1] += i[3]

    def visibletime(self,i):
        if i[4] >= self.VisibleTime-90 and i[5] < self.MaxAlpha:
            i[5] += 3
        if i[4] <= 0:
            self.objects.remove(i)
        if i[4] <= 60:
            i[5] -= 5
        i[4] -= 1

    def update(self):
        self.spawn()
        for i in self.objects:
            self.move(i)
            self.visibletime(i)

#메인화면 파티클
class MainMenuParticle:
    def __init__(self):
        #리스트
        self.objects = []
        #시작 좌표
        self.start_x, self.start_y = screen_width+100, -100
        #움직임
        self.move_xMin, self.move_xMax = 3,10
        self.move_yMin, self.move_yMax = 2,6
        #크기
        self.sizeMin, self.sizeMax = 2,5
        #투명도
        self.alphaMin, self.alphaMax = 10, 255
        #색깔
        self.color = [(216, 60, 60),(0, 174, 99)]
        #스폰 주기
        self.spawnCycle = 60/30 #60/n = 1초에 n개
        self.timeSpawn = 0 #스폰한 후 지난시간

    def Spawn(self):
        """
        x[0] y[1] dx[2] dy[3] size[4] color[5] alpha[6]
        """
        self.objects.append([self.start_x,self.start_y,random.randint(self.move_xMin, self.move_xMax)\
                            ,random.randint(self.move_yMin, self.move_yMax),random.randint(self.sizeMin, self.sizeMax)\
                            ,random.choice(self.color),random.randint(self.alphaMin, self.alphaMax)])

    def Draw(self,i,surface):
        surface.blit(AlphaRect(i[4],i[4],i[5],i[6]),(i[0],i[1]))

    def Move(self,i):
        i[0] -= i[2]
        i[1] += i[3]

    def Delete(self,i):
        if i[0]+i[4] < 0 or i[1] > screen_height+UIbar_height:
            self.objects.remove(i)

    def DeleteAll(self):
        self.objects.clear()

    def Work(self,surface):   
        for i in self.objects:
            self.Move(i)
            self.Draw(i,surface)
            self.Delete(i)

        if self.timeSpawn >= self.spawnCycle:
            self.Spawn()
            self.timeSpawn = 0

        self.timeSpawn += 1

#피튀기는 효과
class BloodSplash:
    def __init__(self):
        self.objects = []
        self.SideLength = 5
        self.SubtractionDegree = 0.1
        self.zombie_die = False

    def Spawn(self,object_x,object_y,amount,speed,color): #speed : 맞았을 때 1 죽었을 때 2
        self.objects.append([])
        for i in range(0,amount):
            self.objects[-1].append([object_x+(30-self.SideLength)/2,object_y+(30-self.SideLength)/2,\
                        random.randint(-100,100)/100,random.randint(-450,-200)/100,object_y+30,speed,color])
                        #x:[0], y:[0], x범위:[2], y범위:[3], 파티클 끝나는 지점:[4], speed[5], color:[6]
    def Draw(self,surface):
        for I in self.objects:
            for i in I:
                pg.draw.rect(surface,i[6],(i[0],i[1],self.SideLength,self.SideLength))

    def Move(self):
        for I in self.objects:
            for i in I:
                i[0] += i[2]
                i[1] += i[3]
                i[3] += self.SubtractionDegree*i[5]

    def Delete(self):
        for I in self.objects:
            for i in I:
                if i[1] > i[4]:
                    I.remove(i)
            if len(I) == 0:
                self.objects.remove(I)

    def Update(self):
        self.Move()
        self.Delete()

#수류탄 효과
class BombSplash:
    def __init__(self):
        self.color = [
            (255, 81, 163),
            (255, 102, 174),
            (255, 114, 181),
            (251, 128, 186),
            (254, 118, 182)
        ]
        self.object = []

    def Spawn(self,StartPoint_x,StartPoint_y,count,speed,DecreaseSpeed):
        degree = 0
        for i in range(count):
            R = 255
            G = random.randint(70,194)
            B = random.randint(0,119)
            RandomColor = (R,G,B)

            RandomSize = random.randint(30,50)
            x = middle(StartPoint_x,0,RandomSize)
            y = middle(StartPoint_y,0,RandomSize)

            degree += 360/count
            angle = math.radians(degree)
            dx = math.cos(angle)*speed
            dy = math.sin(angle)*speed

            self.object.append([])
            self.object[-1].append([x,y,dx,dy,DecreaseSpeed,RandomColor,RandomSize,256,0])
                                    #x:[0] y:[1] dx:[2] dy:[3] decrease speed:[4] random color:[5] random size:[6]
                                        #alpha:[7] time:[8]

    def Move(self,i,j):
        j[0] += j[2] #x += dx
        j[1] += j[3] #y += dy
        j[2] /= j[4] #dx -= decrease speed
        j[3] /= j[4] #dy -= decrease speed
        
    def Alpha(self,i,j):
        if j[8] > 20:
            j[7] -= 20
        j[8] += 1

    def Delete(self,i,j):
        if j[7] <= 0:
            self.object.remove(i)

    def Draw(self,surface):
        for i in self.object:
            for j in i:
                surface.blit(AlphaRect(j[6],j[6],j[5],j[7]),(j[0],j[1]))

    def Update(self):
        for i in self.object:
            for j in i:
                self.Move(i,j)
                self.Alpha(i,j)
                self.Delete(i,j)

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