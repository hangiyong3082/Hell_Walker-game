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
white = (255,255,255)
yellow = (255,228,0)
red = (255,0,0)

clock = pg.time.Clock()
done = False

#경로 설정
def change_dir(path): 
    os.chdir(path)
change_dir('.')

#파일경로
def resource_path(relative_path):  
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#이미지 함수
def load_img(path,img):  
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
def text_set(font,size,bold,italic,contents,antialias,color):
    font = pg.font.SysFont(font,size,bold,italic)
    text = font.render(contents,antialias,color)
    return text

#마우스와 스프라이트 충돌 (if문 조건절에 사용해야됨)
def collide_with_mouse(mouse_x,mouse_y,sprite_x,sprite_y,sprite_width,sprtie_height):
    return sprite_x <= mouse_x <= sprite_x + sprite_width \
            and sprite_y <= mouse_y <= sprite_y + sprtie_height

#사운드
def Sound(path,file,volume):
    sound = pg.mixer.Sound(os.path.join(path,file))
    pg.mixer.Sound.set_volume(sound, volume)
    sound.play()

#투명도가 있는 사각형
def rect_alpha(width,height,color,alpha):
    box = pg.Surface((width,height))  
    box.set_alpha(alpha)                
    box.fill(color)        
    return box

class Ball():
    def __init__(self):
        self.diameter = 10
        self.x,self.y = (screen_width-self.diameter)/2,(screen_height+UIbar_height-self.diameter)/2

    def draw(self):
        pg.draw.circle(screen,white,(self.x,self.y),self.diameter)
    
#전역 변수
    #파일
assets = resource_path('assets')

volume_modify_max = 10
volume_modify = 3

def sound_set(proportion_sound):  #사운드 함수
    return proportion_sound/volume_modify_max*volume_modify

ball = Ball()

while not done:
    screen.fill(background_color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    mouse_x = pg.mouse.get_pos()[0]
    mouse_y = pg.mouse.get_pos()[1]

    ball.draw()

    angle = math.atan2(mouse_y-ball.y,mouse_x-ball.x)
    degree = math.degrees(angle)*1

    DegreeLineSt_x = math.cos(angle)*100+ball.x
    DegreeLineSt_y = math.sin(angle)*100+ball.y
    DegreeLineEnd_x = ball.x+100
    DegreeLineEnd_y = ball.y

    pg.draw.line(screen,yellow,(ball.x,ball.y),(math.cos(angle)*1000+ball.x,math.sin(angle)*1000+ball.y),2)
    pg.draw.line(screen,red,(ball.x,ball.y),(screen_width,ball.y),2)
    pg.draw.line(screen,(255,187,0),(DegreeLineSt_x,DegreeLineSt_y),(DegreeLineEnd_x,DegreeLineEnd_y),2)

    T_ZeroDegree = text_set(gamefont,30,False,False,"0°",True,white)
    screen.blit(T_ZeroDegree,(screen_width-100,ball.y+10))

    T_degree = text_set(gamefont,30,False,False,f"{degree:0.3f}°",True,white)
    T_degree_width,T_degree_height = T_degree.get_size()
    T_degree_setting = math.radians(math.degrees(angle)/2)
    screen.blit(T_degree,(math.cos(T_degree_setting)*120+ball.x-T_degree_width/2,math.sin(T_degree_setting)*120+ball.y-T_degree_height/2))

    print(f"radian:{angle} pygame degree:{degree} real degree:{-degree}")

    pg.display.flip()
    clock.tick(144)
pg.quit()