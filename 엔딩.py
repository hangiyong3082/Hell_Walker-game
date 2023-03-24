#-*- coding:utf-8 -*-
import pygame as pg, os, time, random, math, sys, webbrowser,json
from pygame.locals import *
from 함수 import *
from 파티클 import *

change_dir('.')

#파일
assets = resource_path('assets')
spritesFolder = assets+"\\Sprites"
audioFolder = assets+"\\Audio"
hitboxFolder = assets+"\\Hitbox"
effectsFolder = assets+"\\Effects"
mainmenuFolder = assets+"\\Menu"
uiFolder = assets+"\\UI"
fontsFolder = assets+"\\Fonts"

change_dir('.')

#파일
assets = resource_path('assets')
spritesFolder = assets+"\\Sprites"
audioFolder = assets+"\\Audio"
hitboxFolder = assets+"\\Hitbox"
effectsFolder = assets+"\\Effects"
mainmenuFolder = assets+"\\Menu"
uiFolder = assets+"\\UI"
fontsFolder = assets+"\\Fonts"

class EndingStory:
    def __init__(self): #기본변수 
            self.font = fontsFolder+"\\Hahmlet-Medium.ttf"
            self.bool = False
            self.lines = []
            self.currentLine = 0
            self.currentWord = 0
            self.timeOfOneLetter = 5
            self.tOOL_rate = 0
            self.waitingNextLine = 40
            self.wNL_rate = 0
            self.typingLine = fontText_set(self.font,15,"",True,(200,200,200))
      
            self.textsOfEachLines = (["That's how I was able to get out of the disgusting zombies.","나는 그렇게 역겨운 좀비들 사이에서 빠져나올 수 있었다."],
            ["If my friend hadn't come to rescue me then","친구가 그때 나를 구하러 오지 않았다면"],
            ["I couldn't have held out any longer.","나는 더 버티지 못했을 것이다."],
            ["Does hell feel like this?..........................","지옥이 이런 느낌일까?.........................."],
            ["During that terrible time,","나는 그 끔찍한 시간동안"],
            ["I think I walked through hell for a while......","잠깐 지옥을 걸었었던 것 같다......"])

    def draw(self,lg,screen_width,screen_height):
        #typing
        pos = [200,100]
        for t in self.lines:
            screen.blit(t,pos)
            pos[1] += 70
        screen.blit(self.typingLine,pos)

        #skip
        skip_l = ["press 'shift' to exit","'shift'를 눌러 나가기"]
        skip_f = fontsFolder+"\\HSBombaram2.1.ttf"
        skip_t = fontText_set(skip_f,25,skip_l[lg],True,(170,170,170))
        screen.blit(skip_t,(screen_width-skip_t.get_size()[0]-30,screen_height-50))
            
    def update(self,lg):
        if self.currentLine <= len(self.textsOfEachLines)-1:
            numberOfWord = len(self.textsOfEachLines[self.currentLine][lg])
            if self.currentWord == numberOfWord-1:
                if self.wNL_rate >= self.waitingNextLine:
                    self.lines.append(self.typingLine)
                    self.typingLine = fontText_set(self.font,15,"",True,(200,200,200))
                    self.currentLine += 1
                    self.currentWord = 0
                    self.wNL_rate = 0
                self.wNL_rate += 1
            else:
                if self.tOOL_rate >= self.timeOfOneLetter:
                    self.currentWord += 1
                    self.typingLine = fontText_set(self.font,27,
                                    self.textsOfEachLines[self.currentLine][lg][:self.currentWord+1],True,(200,200,200))
                    self.tOOL_rate = 0
                self.tOOL_rate += 1

class EndingCar(pg.sprite.Sprite):
    def __init__(self,startX,startY,endX,endY,speed,currentVolume,maxVolume) -> None:
        super().__init__()
        self.image = load_img(spritesFolder,'car.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midleft = (startX,startY)

        self.brackSound_play = 0
        self.hornSound_play = 0
        self.currentVolume,self.maxVolume = currentVolume,maxVolume

        self.endX,self.endY = endX,endY
        self.speed = speed

    def update(self,player,endingStroy,spreadParticle):
        if self.hornSound_play == 0:
                Sound(audioFolder,'car_horn.wav',set_sound(0.3,self.currentVolume,self.maxVolume))
                self.hornSound_play += 1
        if self.rect.midleft[0] <= self.endX:
            self.speed -= 0.2
            if self.brackSound_play == 0:
                Sound(audioFolder,'car_brack.wav',set_sound(0.5,self.currentVolume,self.maxVolume))
                spreadParticle.Spawn(10,self.rect.midleft,(2,3),0.97,(-180,180),(60,120),(200,200,200),(7,8),0.01,True,(100,100,100))
                self.brackSound_play += 1
        if self.speed <= 0:
            self.speed = 0
            if self.rect.colliderect(player.h_rect):
                Sound(audioFolder,'car_door.wav',set_sound(0.8,self.currentVolume,self.maxVolume))
                endingStroy.bool = True
                self.kill()
        self.rect.midleft = (self.rect.midleft[0]-self.speed,self.rect.midleft[1])
#spreadParticle = SpreadParticle()