#-*- coding:utf-8 -*-
import pygame as pg, os, time, random, math, sys
from 함수 import *

pg.init()

#기본 세팅
screen_width = 1200
screen_height = 650
UIbar_height = 150
screen = pg.display.set_mode([screen_width,screen_height+UIbar_height])
pg.display.set_caption("Hell Walker")

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

color = tuple(map(int,input(">>>").split(', ')))

while not done:
    screen.fill(background_color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    
    pg.draw.rect(screen,color,[middle(0,screen_width,100),middle(0,screen_height+UIbar_height,100),100,100])

    pg.display.flip()
    clock.tick(60)
pg.quit()