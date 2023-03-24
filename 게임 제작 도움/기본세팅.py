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

while not done:
    screen.fill(background_color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    #내용
    pg.display.flip()
    clock.tick(60)
pg.quit()