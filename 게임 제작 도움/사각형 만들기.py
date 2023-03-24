#-*- coding:utf-8 -*-
import pygame as pg, os, time, random, math, sys

pg.init()

print('')
print('spacebar : 수정하는 모서리 변경')
print('r : 가로 세로 다시설정')
print('방향키 위쪽 or 마우스 휠 위쪽 : 모서리 +10')
print('방향키 아래쪽 or 마우스 휠 아래쪽 : 모서리 -10')
rect_width,rect_height = 1,1
while rect_width%5 != 0 or rect_height%5 != 0:
    print('')
    print('10단위로!')
    try:
        rect_width,rect_height = map(int,input('가로 세로 >>> ').split())
    except:print('(오류)')

#기본 세팅
screen_width = 1200
screen_height = 800
UIbar_height = 0
screen = pg.display.set_mode([screen_width,screen_height+UIbar_height])
pg.display.set_caption("사각형 만들기")

background_color = (140,140,140)
black = (0,0,0)

clock = pg.time.Clock()
done = False

def text_set(font,size,bold,italic,contents,antialias,color):
    font = pg.font.SysFont(font,size,bold,italic)
    text = font.render(contents,antialias,color)
    return text

volume_modify_max = 10
volume_modify = 3

def sound_set(proportion_sound):  #사운드 함수
    return proportion_sound/volume_modify_max*volume_modify

mode = 0 #0:width 1:height
mode_text = 0

def up():
    global rect_width,rect_height
    if mode == 0:
        rect_width+=10     
    else:
        rect_height+=10
    print(rect_width,rect_height)   

def down():
    global rect_width,rect_height
    if mode == 0:
        if rect_width > 10:
            rect_width-=10              
    else:
        if rect_height > 10:
            rect_height-=10     
    print(rect_width,rect_height)   

while not done:
    screen.fill(background_color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                mode += 1
                if mode > 1:mode=0
                if mode == 0:mode_text='가로'
                else:mode_text='세로'
                print('변경 :'+mode_text)
            if event.key == pg.K_r:
                rect_width,rect_height = map(int,input('가로 세로 >>> ').split())
            if event.key == pg.K_UP:
                up()    
            if event.key == pg.K_DOWN:
                down()
        if event.type == pg.MOUSEBUTTONUP and event.button == pg.BUTTON_WHEELUP:        
            up()
        if event.type == pg.MOUSEBUTTONUP and event.button == pg.BUTTON_WHEELDOWN:   
            down()

    if mode == 0:mode_text='가로'
    else:mode_text='세로'

    text = text_set('hy견고딕',30,False,False,'변경 : '+mode_text,True,black)
    screen.blit(text,(screen_width - text.get_size()[0] - 30,screen_height - text.get_size()[1] - 30))

    text1 = text_set('hy견고딕',30,False,False,f"가로 : {rect_width}, 세로 : {rect_height}",True,black)
    screen.blit(text1,(30,screen_height - text.get_size()[1] - 30))

    if mode == 0:
        color = (180, 76, 0)
    else:
        color = (7, 78, 137)
    pg.draw.rect(screen,color,((screen_width-rect_width)/2,(screen_height-rect_height)/2,rect_width,rect_height),3)

    pg.display.flip()
    clock.tick(60)
pg.quit()