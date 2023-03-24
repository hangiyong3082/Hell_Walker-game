import pygame as pg, os, time, random, math, sys, webbrowser, pickle
from pygame.locals import *

screen_width = 1200
screen_height = 650
UIbar_height = 150
screen = pg.display.set_mode([screen_width,screen_height+UIbar_height])

def change_dir(path): #경로 설정
    os.chdir(path)

def resource_path(relative_path):  #파일경로
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_img(path,img):  #이미지 함수
    return pg.image.load(os.path.join(path,img))

#게임폰트
def AvailableGameFont_Set(gamefont:list) -> str:
    """
    gamefont ``list``
        -> available gamefont
    """
    for f in gamefont:
        for i in pg.font.get_fonts():
            if f == i:
                gamefont = f
                break

#텍스트 함수
def text_set(font,size,bold,italic,contents:str,antialias,color):
    """
    텍스트를 반환함
    """
    font = pg.font.SysFont(font,size,bold,italic)
    text = font.render(contents,antialias,color)
    return text

#점과 스프라이트 충돌 (if문 조건절에 사용해야됨)
def collide_with_point(point_x,point_y,sprite_x,sprite_y,sprite_width,sprtie_height):
    """
    점과 스프라이트 충돌할 때 처리하는 함수
     (if문 조건절에 사용해야 함)
    """
    return sprite_x <= point_x <= sprite_x + sprite_width \
            and sprite_y <= point_y <= sprite_y + sprtie_height

#사운드
def Sound(path,file,volume):
    sound = pg.mixer.Sound(os.path.join(path,file))
    pg.mixer.Sound.set_volume(sound, volume)
    sound.play()

#음악
def Music(path,file,volume,loops):
    music = pg.mixer.music.load(os.path.join(path,file))
    pg.mixer.music.set_volume(music, volume)
    music.play(loops)

#투명도가 있는 사각형
def AlphaRect(width,height,color,alpha):
    '''투명도가 있는 사각형'''
    box = pg.Surface((width,height))  
    box.set_alpha(alpha)                
    box.fill(color)        
    return box

#가운데 배치
def middle(standard_vector,standard_width,object_width):
    """
    오브젝트 가운데에 배치하는 오브젝트의 좌표값을 반환함
    """
    return standard_vector+(standard_width-object_width)/2

#사운드 함수
def set_sound(proportion_sound,volume,volume_max):  
    """
    ``proportion_sound`` : 상대적인 사운드 크기
    """
    return proportion_sound*(volume/volume_max)

def distinguish_sign(value):
    """
    양수면
        return : ``1``
    음수면
        return : ``-1``
    0이면 
        return : ``0``
    """
    result = 0
    if value > 0:result = 1
    elif value < 0:result = -1
    elif value == 0:result = 0

    return result

#점수 저장
def SaveScore(*lastest_score):
    """
    *lastest_score : 저장할 점수값을 차례대로 넣는다.
    """
    f = open("score data.txt",'rb')
    score_data = list(pickle.load(f))

    for i in range(len(lastest_score)):
        if lastest_score[i] > score_data[i]:
            score_data[i] = lastest_score[i]

    f = open("score data.txt",'wb')
    pickle.dump(score_data,f)

    f.close()

#설정 저장
def SaveSetting(*setting_data):
    f = open("setting data.txt",'wb')
    pickle.dump(setting_data,f)
    f.close()

#점수 불러오기
def LoadScore():
    #점수값이 있으면 로드, 없으면 0으로 저장
    try:
        f = open("score data.txt",'rb')
        score_data = list(pickle.load(f))
    except:
        f = open("score data.txt",'wb')
        score_data = [0,0]
        pickle.dump(score_data, f)
    f.close()
    return score_data

#설정 불러오기
def LoadSetting():
    try:
        f = open("setting data.txt",'rb')
        setting_data = list(pickle.load(f))
    except:
        f = open("setting data.txt",'wb')
        setting_data = [5,0,1]
        pickle.dump(setting_data, f)
    f.close()
    return setting_data

def circle_surf(radius, color):
    surf = pg.Surface((int(radius * 2), int(radius * 2)))
    pg.draw.circle(surf, color, (radius, radius),radius)
    surf.set_colorkey((0, 0, 0))
    return surf

def ellipse_surf(width,height,color,alpha):
    surf = pg.Surface((width,height))
    pg.draw.ellipse(surf, color, (width,height,width,height))
    surf.set_alpha(alpha)
    surf.set_colorkey((0,0,0))
    return surf