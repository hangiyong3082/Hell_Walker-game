#-*- coding:utf-8 -*-
import pygame as pg, os, time, random, math, sys
from tkinter import *
import game

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
set_color = (255, 59, 152)

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
gamefont = ['한컴산뜻돋움','nanumgothic','hy견고딕','gulim']
for f in gamefont:
    for i in pg.font.get_fonts():
        if f == i:
            try:gamefont = gamefont[gamefont.index(f)]
            except:pass
            break
        
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

class Menu():
    def __init__(self):
        #타이틀
            #이미지
        self.title_img = load_img(assets,'menu_title.png')
        self.title_glow = load_img(assets,'menu_title_glow.png')
            #이미지 크기
        self.title_width,self.title_height = self.title_img.get_size()

        #값 수정 버튼
            #이미지  (위쪽 화살표가 기본 이미지)
        self.modify_img = load_img(assets, 'volume_up.png') # v : volume
        self.modify_img_flip = pg.transform.flip(self.modify_img,False,True)
            #이미지 크기
        self.modify_img_width,self.modify_img_height = self.modify_img.get_size()

        #볼륨
            #설명
        self.v_text = Text(gamefont,30,False,False,'음량설정',True,(255,255,255))
        self.v_text_width,self.v_text_height = self.v_text.get_size()
            #설명과 이미지의 거리
        self.v_space = 30
            #설명 좌표
        self.v_text_x = (screen_width -self.v_text_width -self.modify_img_width -self.v_space)/2
        self.v_text_y = load_img(assets,'menu_title.png').get_size()[1]+100
            #이미지 사이의 거리
        self.v_img_space = 90
            #이미지 좌표
        self.v_img_x = self.v_text_x + self.v_text_width + self.v_space
        self.v_img_up_y = self.v_text_y + (self.v_text_height - self.modify_img_height)/2 - self.v_img_space/2
        self.v_img_down_y = self.v_text_y + (self.v_text_height - self.modify_img_height)/2 + self.v_img_space/2
            #음량 값 텍스트
        self.v_text_num = Text(gamefont,25,False,False,f"{game.volume_modify}",True,(255,255,255))
        self.v_text_num_width,self.v_text_num_height = self.v_text_num.get_size()
            #음량 값 좌표
        self.v_text_num_x = self.v_img_x + (self.modify_img_width-self.v_text_num_width)/2
        self.v_text_num_y = self.v_text_y + (self.modify_img_height-self.v_text_num_height)/2

    def draw(self):
        #배경
        screen.fill(black)
        pg.draw.rect(screen,set_color,(0,0,screen_width,screen_height+UIbar_height),5)
        #타이틀
        screen.blit(self.title_glow,((screen_width-self.title_width)/2,0))
        screen.blit(self.title_img,((screen_width-self.title_width)/2,0))
        #경계
        pg.draw.line(screen,set_color,(50,self.title_height),(screen_width-50,self.title_height),5)
        #볼륨 설정
            #설명
        screen.blit(self.v_text,(self.v_text_x,self.v_text_y))
            #이미지
        screen.blit(self.modify_img,(self.v_img_x,self.v_img_up_y))
        screen.blit(self.modify_img_flip,(self.v_img_x,self.v_img_down_y))
            #음량 값
        screen.blit(self.v_text_num,(self.v_text_num_x,self.v_text_num_y))

    def update(self):
        self.v_text_num = Text(gamefont,25,False,False,f"{game.volume_modify}",True,(255,255,255))

menu = Menu()
while not done:
    screen.fill(background_color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.MOUSEBUTTONUP and event.button == pg.BUTTON_LEFT:
            #메인 메뉴
            if game.main_menu:
                if menu.v_img_x<=pg.mouse.get_pos()[0]<=menu.v_img_x+menu.modify_img_width \
                    and menu.v_img_up_y<=pg.mouse.get_pos()[1]<=menu.v_img_up_y+menu.modify_img_height:
                    if game.volume_modify < game.volume_modify_max:
                        game.volume_modify += 1
                elif menu.v_img_x<=pg.mouse.get_pos()[0]<=menu.v_img_x+menu.modify_img_width \
                    and menu.v_img_down_y<=pg.mouse.get_pos()[1]<=menu.v_img_down_y+menu.modify_img_height:
                    if game.volume_modify > 0:
                        game.volume_modify -= 1

    menu.draw()
    menu.update()

    pg.display.flip()
    clock.tick(60)
pg.quit()
    