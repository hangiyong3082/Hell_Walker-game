#-*- coding:utf-8 -*-
import pygame as pg, os, time, random, math, sys
from tkinter import *

pg.init()

root = Tk()

monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

#기본 세팅
screen_width = 1200
screen_height = 650
UIbar_height = 150
screen = pg.display.set_mode([screen_width,screen_height+UIbar_height])
pg.display.set_caption("Hell Walker")

background_color = (40,40,40)
black = (0,0,0)
set_color = (255,36,163)

clock = pg.time.Clock()
done = False

def change_dir(path): #경로 설정
    os.chdir(path)
change_dir('.')

def resource_path(relative_path):  #파일경로
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_img(path,img):  #이미지 함수
    return pg.image.load(os.path.join(path,img))

#폰트
gamefont = 'nanumgothic'
for i in pg.font.get_fonts():
    if i == '한컴산뜻돋움':
        gamefont = '한컴산뜻돋움'
        
#텍스트 함수
def Text(font,size,bold,italic,contents,antialias,color):
    font = pg.font.SysFont(font,size,bold,italic)
    text = font.render(contents,antialias,color)
    return text

#전역 변수
    #파일
assets = resource_path('assets')

volume_modify_max = 10
volume_modify = 3

def sound_set(proportion_sound):  #사운드 함수
    return proportion_sound/volume_modify_max*volume_modify

def menu():
    #배경
    screen.fill(black)
    pg.draw.rect(screen,set_color,(0,0,screen_width,screen_height+UIbar_height),5)
    #타이틀
    title_img = load_img(assets,'menu_title.png')
    title_glow = load_img(assets,'menu_title_glow.png')
    screen.blit(title_glow,((screen_width-title_img.get_size()[0])/2,0))
    screen.blit(title_img,((screen_width-title_img.get_size()[0])/2,0))
    #경계
    #pg.draw.line(screen,set_color,(50,title_img.get_size),screen_width-50,5)

while not done:
    screen.fill(background_color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    menu()

    pg.display.flip()
    clock.tick(60)
pg.quit()
    