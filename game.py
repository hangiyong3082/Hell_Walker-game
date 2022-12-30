#-*- coding:utf-8 -*-
import pygame as pg, os, time, random, math, sys, webbrowser, pickle
from 함수 import *

pg.init()

change_dir('.')

#기본 세팅
screen_width = 1200
screen_height = 650
UIbar_height = 150
screen = pg.display.set_mode([screen_width,screen_height+UIbar_height])
pg.display.set_caption("Hell Walker") 

background_color = (30,30,30)
black = (0,0,0)
white = (255,255,255)
set_color = (255, 59, 152)

clock = pg.time.Clock() 
done = False

#폰트
gamefont = ['hy견고딕','nanumgothic','gulim']

AvailableGameFont_Set(gamefont)

#점수값이 있으면 로드, 없으면 0으로 저장
try:
    f_s = open("score data.txt",'rb')
    score_data = list(pickle.load(f_s))
except:
    f_s = open("score data.txt",'wb')
    score_data = [0,0]
    pickle.dump(score_data, f_s)
f_s.close()

def ValueSetting() -> None: #차트 정리용
    """
    전역 변수 선언하는 곳
                    V V V
    """

#전역 변수
    #파일
assets = resource_path('assets')
    #클릭
press_x_list = []
press_y_list = []
press_left,press_right,press_up,press_down = (False,False,False,False)
click_left, click_right = False,False
    #무기
weapon = 1
special_weapon = False
    #좀비(근접)
zombie_melee_spawntime = 90
zombie_melee_crash_player_time = 60
crash_Zm_time = 0
crash_Zm_time_ = crash_Zm_time
    #좀비(원거리)
zombie_shoot_spawntime = 160
zombie_shoot_shooting_time = 110
    #전체 점수
score = 0
    #시간제 점수 시간
Time = 60
    #웨이브
wave_count = 0
    #수류탄 (have빼고 삭제 예정)
special_weapon_click = 1
special_weapon_availabletime = 0
special_weapon_have = 3
    #업그레이드
Upgrading = False
    #사운드
volume_max = 10
volume = 5
    #게임
Graphic = 1 # 0:저품질 1:고품질
ResetGame = False
FPS = 60
fps_proportion = 60/FPS
lg = 1 #language 0:eng 1:kr

#플레이어
class Player:
    def __init__(self):
        global max_health
        self.img = load_img(assets,'player.png').convert()
        self.rect = self.img.get_rect()
        self.width,self.height = self.img.get_size()
        self.x = screen_width/2-self.width/2
        self.y = screen_height/2-self.height/2+UIbar_height
        self.max_health = 5
        self.health = self.max_health
        self.speed_init = 2.7
        self.normal_speed = self.speed_init
        self.speed = self.normal_speed
        self.sprites = []
        self.walk_sound_initval = 25  #사운드용
        self.walk_sound = self.walk_sound_initval
        self.move_condition = False
        #히트박스
        self.hitbox = load_img(assets,'player_hitbox.png').convert_alpha()
        self.h_rect = self.hitbox.get_rect()
        self.h_width,self.h_height = self.hitbox.get_size()
        #체력 적을 때
        self.AlmostDie_img = load_img(assets,'AlmostDie.png').convert_alpha()
        self.AlmostDie_width,self.AlmostDie_height = self.AlmostDie_img.get_size()
        #맞았을 때 효과
        self.ph_e_img = load_img(assets,'player_hurt.png').convert()
        self.ph_e_appear = False
        self.ph_e_transparent_initval = 150
        self.ph_e_transparent = self.ph_e_transparent_initval

    def move(self):
        #좌우 방향키와 상하 방향키를 같이 누른다면 속도 감소
        self.decrease_speed = self.normal_speed*0.8
        if len(press_x_list) > 0 and len(press_y_list) > 0:
            self.speed = self.decrease_speed*fps_proportion
        else:
            self.speed = self.normal_speed*fps_proportion

        if len(press_x_list) > 0:
                press_x_list[-1] = self.speed*distinguish_sign(press_x_list[-1])
        if len(press_y_list) > 0:
            press_y_list[-1] = self.speed*distinguish_sign(press_y_list[-1])  

        #메인
            #좌우
        if (press_left,press_right) == (False,False):
            press_x_list.clear()
        if len(press_x_list) > 2:
            del press_x_list[0]        
        if len(press_x_list) > 0:
            self.x += press_x_list[-1]
            #상하
        if (press_up,press_down) == (False,False):
            press_y_list.clear()
        if len(press_y_list) > 2:
            del press_y_list[0]        
        if len(press_y_list) > 0:
            self.y += press_y_list[-1]

        #벽에 닿았을 때
        if self.x < 0:self.x += self.speed
        if self.x > screen_width-self.width:self.x -= self.speed
        if self.y < UIbar_height:self.y += self.speed
        if self.y > screen_height+UIbar_height-self.height:self.y -= self.speed

    def draw(self):
        screen.blit(self.img,[self.x,self.y])

        if self.health <= 1:
            screen.blit(self.AlmostDie_img,(middle(self.x,self.width,self.AlmostDie_width),\
                                                middle(self.y,self.height,self.AlmostDie_height)))

    def sound(self,volume):
        if len(press_x_list) != 0 or len(press_y_list) != 0:
            self.move_condition = True
        else:
            self.move_condition = False

        if self.move_condition:
            if self.walk_sound <= 0:
                self.walk_sound = self.walk_sound_initval

                walk_sound = pg.mixer.Sound(os.path.join(assets,'walk_sound.wav'))
                pg.mixer.Sound.set_volume(walk_sound, volume)
                walk_sound.play()

            self.walk_sound -= 1
        else:
            self.walk_sound = self.walk_sound_initval

    def hurt_effect(self):
        if self.ph_e_appear:
            if self.ph_e_transparent > 0:
                self.ph_e_img.set_alpha(self.ph_e_transparent)
                screen.blit(self.ph_e_img,(player.x,player.y))
                self.ph_e_transparent -= 2
            else:
                self.ph_e_transparent = self.ph_e_transparent_initval
                self.ph_e_img.set_alpha(self.ph_e_transparent)
                self.ph_e_appear = False

    def update(self):
        self.move()
        self.centerx = self.x + self.width/2
        self.centery = self.y + self.height/2
        self.rect.topleft = (self.x,self.y)
        #히트박스
        self.h_x = middle(self.x,self.width,self.h_width)
        self.h_y = middle(self.y,self.height,self.h_height)
        self.h_rect.topleft = (self.h_x,self.h_y)

#체력이 적을 때 화면 흐리게
def Almostdie():  
    if player.health <= 1:
        screen.blit(rect_alpha(screen_width,screen_height+UIbar_height,(0,0,0),100),[0,0])

#맞았을 때 화면 전체적으로 효과
class PlayerHurt:
    def __init__(self):
        self.EffectThick = 70
        self.ph_e_transparent_initval = 150
        self.ph_e_transparent = 0

    def effect(self):
        if self.ph_e_transparent > 0:
            TopAndBottom = rect_alpha(screen_width,self.EffectThick,(255,0,0),self.ph_e_transparent)
            RightAndLeft = rect_alpha(self.EffectThick,screen_height+UIbar_height-(self.EffectThick*2),(255,0,0),self.ph_e_transparent) 
            screen.blit(TopAndBottom,(0,0)) #top
            screen.blit(TopAndBottom,(0,screen_height+UIbar_height-self.EffectThick)) #bottom
            screen.blit(RightAndLeft,(0,self.EffectThick)) #right
            screen.blit(RightAndLeft,(screen_width-self.EffectThick,self.EffectThick)) #left

            self.ph_e_transparent -= 3
            
#공격 방향 표시
class Atteck_dir:
    def __init__(self):
        self.img = []
        self.img.append([load_img(assets,'atteck_dir_gun.png').convert_alpha(),0,0,(34,177,76)])
        self.img.append([load_img(assets,'atteck_dir_knife.png').convert_alpha(),0,0,(70,235,125)])
        for s in self.img:
            s[1] = s[0].get_size()[0]
            s[2] = s[0].get_size()[1]
    
    def draw(self):
        current_img = self.img[weapon]
        if special_weapon == False:
            current_img[0].set_colorkey((current_img[3]))
            screen.blit(self.result,(self.x-current_img[1]/2,self.y-current_img[2]/2))
            
    def update(self):
        current_img = self.img[weapon]
        self.angle = math.atan2(mouse_y-player.centery, mouse_x-player.centerx)
        self.degree = math.degrees(self.angle)*-1
        self.x = 50*math.cos(self.angle) + player.centerx
        self.y = 50*math.sin(self.angle) + player.centery
        self.result = pg.transform.rotate(current_img[0],self.degree)
        self.result.set_colorkey(current_img[3])
        
#무기가 수류탄일 때 마우스에 타겟 이미지
class Target_mouse:
    def __init__(self):
        self.img = load_img(assets,'target.png').convert_alpha()
        self.width, self.height = self.img.get_size()
        self.img.set_colorkey((0,0,0))
    def draw(self):
        if not Upgrading:
            if special_weapon == True:
                pg.mouse.set_visible(False)
                screen.blit(self.img, [mouse_x-self.width/2,mouse_y-self.height/2])            
            else:
                pg.mouse.set_visible(True)

#총알
class Bullet:
    def __init__(self):
        self.img = load_img(assets,'bullet.png').convert_alpha()
        self.width,self.height = self.img.get_size()
        self.rect = self.img.get_rect()
        self.speed = 10
        self.speed_increase = 0.13
        self.fire_term_init = 60
        self.fire_term = self.fire_term_init
        self.list = []

    def atteck(self): 
        global score
        for B in self.list:
            self.rect.topleft = (B[0],B[1])
            for Zm in zombie_melee.list:  #zombie_melee
                zombie_melee.rect.topleft = (Zm[0],Zm[1])
                if zombie_melee.rect.colliderect(self.rect):
                    Zm[5] -= 1
                    if Zm[5] > 0:
                        blood_splash.spawn(Zm[0],Zm[1],3,4,(189, 206, 216))
                    try:
                        self.list.remove(B)
                    except:pass
            for Zs in zombie_shoot.list:  #zombie_shoot
                zombie_shoot.rect.topleft = (Zs[0],Zs[1])
                if zombie_shoot.rect.colliderect(self.rect):
                    Zs[5] -= 1
                    try:
                        self.list.remove(B)
                    except:pass              
    
    def draw(self):
        for B in self.list:
            screen.blit(self.img,(B[0],B[1]))

    def sound(self,volume):
        if self.fire_term <= 0 and weapon == 0 and special_weapon == False:
            if self.fire_term_init <= 30:
                volume = volume*(self.fire_term_init/30)
            Sound(assets,'gun_sound.wav',volume)

    def update(self):
        self.atteck()
        self.x = atteck_dir.x
        self.y = atteck_dir.y
        if self.fire_term <= 0 and weapon == 0 and special_weapon == False:
            self.angle = math.atan2(mouse_y-player.centery, mouse_x-player.centerx)
            self.degree = math.degrees(self.angle)*-1
            self.dx = 0 #math.cos(self.angle)*self.speed
            self.dy = 0 #math.sin(self.angle)*self.speed
            self.list.append([self.x-self.width/2, self.y-self.height/2, self.dx, self.dy, 
                                    self.angle, self.speed])
            self.fire_term = self.fire_term_init
        for B in self.list:
            if B[0] >= screen_width or B[0] <= -self.width:
                self.list.remove(B)
            elif B[1] >= screen_height+UIbar_height or B[1] <= -self.height+UIbar_height:
                self.list.remove(B)         
        for B in self.list:
            B[5] += self.speed_increase
            B[2] = math.cos(B[4])*B[5]
            B[3] = math.sin(B[4])*B[5]
            B[0] += B[2]
            B[1] += B[3]
        if weapon == 0 and special_weapon == False:
            self.fire_term -= 1
        else:
            self.fire_term = self.fire_term_init
    
#칼
class Knife:
    def __init__(self):
        self.img = load_img(assets,'knife_hitbox.png').convert_alpha()
        self.width, self.height = self.img.get_size()
        self.cooltime = 0
        self.cooltime_init = 120
        self.AtteckingTime_init = 10
        self.AtteckingTime = 0
        self.increase_size = 0

    def Atteck(self):
        global score
        self.img = pg.transform.scale(self.img,\
                (self.width+self.increase_size,self.height+self.increase_size))
        #공격, 히트박스 위치 설정
        if self.cooltime > 0:
            self.cooltime -= 1

        if click_left == True and self.cooltime == 0 and weapon == 1 and special_weapon == False:
            self.AtteckingTime = self.AtteckingTime_init
            self.cooltime = self.cooltime_init
            
        if self.AtteckingTime > 0:
            self.AtteckingTime -= 1
            self.angle = math.atan2(mouse_y-player.centery, mouse_x-player.centerx)
            self.x = (50+self.increase_size)*math.cos(self.angle) \
                                                + player.centerx -(self.width+self.increase_size)/2
            self.y = (50+self.increase_size)*math.sin(self.angle) \
                                                + player.centery -(self.height+self.increase_size)/2        
        #데미지 줌
            self.rect = self.img.get_rect()
            self.rect.topleft = (self.x,self.y)
            
            for Zmk in zombie_melee.list:  #zombie_melee
                Zmk_rect = zombie_melee.img.get_rect()
                Zmk_rect.topleft = (Zmk[0], Zmk[1])
                if self.rect.colliderect(Zmk_rect):
                    Zmk[5] -= 2

            for Zs in zombie_shoot.list:   #zombie_shoot
                Zs_rect = zombie_shoot.img.get_rect()
                Zs_rect.topleft = (Zs[0], Zs[1])
                if self.rect.colliderect(Zs_rect):
                    Zs[5] -= 2
                
        #히트박스 위치 초기화
        if self.AtteckingTime == 0:
            self.x, self.y = None, None

    def draw(self):
        if self.AtteckingTime > 0:
            screen.blit(self.img,(self.x, self.y))

    def sound(self,volume):
        if click_left == True and self.cooltime == self.cooltime_init and weapon == 1 and special_weapon == False:
            Sound(assets,'knife_sound.wav',volume)

    def update(self):
        self.Atteck()   

#특수무기(수류탄)
class Bomb:
    def __init__(self):
        self.img = load_img(assets,'bomb.png').convert()
        self.img.set_colorkey((255,255,255))     
        self.width, self.height = self.img.get_size()   
        self.f_img = load_img(assets,'fallingpos.png').convert_alpha()
        self.f_img.set_colorkey((0,0,0)) 
        self.fallingpos = []
        self.bomblist = []
        self.explode = []
        self.explode_draw = []
        self.bomb_arrive = False #사운드용
        #히트박스
        self.h_img = load_img(assets,'explode_hitbox.png').convert_alpha()
        self.h_img.set_colorkey((255,255,255))
        self.h_width, self.h_height = self.h_img.get_size()   
        self.rect = self.h_img.get_rect()
        #폭발 모션
        self.e_img = []
        self.e_img.append(load_img(assets,'explode_1.png').convert_alpha())
        self.e_img.append(load_img(assets,'explode_2.png').convert_alpha())
        self.e_img.append(load_img(assets,'explode_3.png').convert_alpha())
        self.e_img.append(load_img(assets,'explode_4.png').convert_alpha())
        self.e_img[0].set_colorkey((255,255,255))
        self.e_img[1].set_colorkey((255,255,255))
        self.e_img[2].set_colorkey((255,255,255))
        self.e_img[3].set_colorkey((255,255,255))
        self.e_currenttime = 0
        
    def falling(self):
        global special_weapon_click,special_weapon_availabletime,special_weapon_have
        #떨어지는 모션
        if special_weapon == True:
            if click_left == True and special_weapon_click == 1 and special_weapon_availabletime == 0\
                and special_weapon_have > 0 and mouse_y > UIbar_height:
                special_weapon_click = 0    
                special_weapon_availabletime = 30              
                self.fallingpos.append([mouse_x,mouse_y])
                self.bomblist.append([mouse_x,UIbar_height-self.height-10,0]) #x[0] y[1] degree[2]   
                special_weapon_have -= 1
        #사용가능 시간 간격
        if special_weapon_availabletime > 0:
            special_weapon_availabletime -= 1 
        #메인
        for f in self.fallingpos:
            self.bomblist[self.fallingpos.index(f)][1] += 15

            if f[1]-self.height <= self.bomblist[self.fallingpos.index(f)][1]:
                self.bomblist.remove(self.bomblist[self.fallingpos.index(f)])
                self.explode.append([f[0]-self.h_width//2,f[1]-self.h_height//2])
                self.explode_draw.append([f[0]-self.h_width//2,f[1]-self.h_height//2,12,0,3,-1])
                                        #x[0], y[1], 폭발모션시간[2], 에니메이션 1장당 시간[3], [3]의 초기값[4], 애니메이션 사진[5]
                bomb_splash.spawn(f[0],f[1],15,7,1.045)
                self.fallingpos.remove(f)  

                self.explode.clear()

                self.bomb_arrive = True
        
    def draw(self):
        for f in self.fallingpos: #도착 지점
            screen.blit(self.f_img,(f[0]-self.f_img.get_size()[0]/2,f[1]-self.f_img.get_size()[1]/2))

        for b in self.bomblist: #수류탄
            b[2] += 2
            result = pg.transform.rotate(self.img,b[2])
            screen.blit(result,(b[0]-self.width//2,b[1]))

        for ed in self.explode_draw: #폭발
            if ed[2] <= 0:
                self.explode_draw.remove(ed)               
                break
            if ed[3] <= 0:
                ed[5] += 1
                ed[3] = ed[4]   
            if Graphic == 0:
                pg.draw.circle(screen,(229, 56, 203),(ed[0]+self.h_width/2,ed[1]+self.h_width/2),self.h_width/2)
                pg.draw.circle(screen,(239, 133, 223),(ed[0]+self.h_width/2,ed[1]+self.h_width/2),self.h_width/3)
            else:
                screen.blit(self.e_img[ed[5]],(ed[0],ed[1]))
            ed[2] -= 1
            ed[3] -= 1        
    
    def damage(self,zm,zs):
        global score  
        for e in self.explode_draw:
            self.rect.topleft = e[0],e[1]
            for m in zm.list:
                zm.rect.topleft = m[0],m[1]
                if zm.rect.colliderect(self.rect):
                    m[5] -= 2
                    
            for s in zs.list:
                zs.rect.topleft = s[0],s[1]
                if zs.rect.colliderect(self.rect):
                    s[5] -= 2

    def sound(self,volume):
        if self.bomb_arrive:
            Sound(assets,'bomb_sound.wav',volume)
            self.bomb_arrive = False
        
    def update(self):
        self.falling()
        self.damage(zombie_melee,zombie_shoot)
    
#좀비(근접)
class Zombie_melee:
    def __init__(self):
        self.img = load_img(assets,'zombie_1.jpg').convert()
        self.img_Lflip = pg.transform.flip(self.img,True,False)
        self.width, self.height = self.img.get_size()
        self.rect = self.img.get_rect()
        self.speed = 2
        self.health = 2
        self.crash_player_time = 0
        self.list = []
        self.spawntime = zombie_melee_spawntime
        self.x , self.y = 0,0
        self.die = False #사운드용
        #체력 표시
        self.HealthText_list = []
        #크래시박스
        self.crashbox = load_img(assets,'zombie_1_crashbox.png').convert_alpha()
        self.c_rect = self.crashbox.get_rect()
        self.c_width,self.h_height = self.crashbox.get_size()
        #플레이어 데미지 사운드
        self.ph_sound = False

    def spawn(self):
        if wave.zm_spawncount//1 > 0:
            if self.spawntime <= 0:
                first_random = random.randint(1,4)
                if first_random == 1:
                    x_pos = random.randint(0,screen_width-self.width)
                    y_pos = -self.height+UIbar_height       
                elif first_random == 2:
                    x_pos = random.randint(0,screen_width-self.width)
                    y_pos = screen_height+UIbar_height       
                elif first_random == 3:
                    x_pos = -self.width
                    y_pos = random.randint(UIbar_height,screen_height-self.height)
                elif first_random == 4:
                    x_pos = screen_width
                    y_pos = random.randint(UIbar_height,screen_height-self.height)
                self.x = x_pos
                self.y = y_pos
                self.angle = 0
                self.dx = 0
                self.dy = 0
                self.list.append([self.x,self.y,self.dx,self.dy,self.angle,self.health,
                                    self.crash_player_time,random.choice([True,False]),0,0,0])
                                # x:[0] y:[1] dx:[2] dy[3] angle[4] health[5] crash_player_time[6]
                                    #Lflip?:[7] HealthText_set:[8] HealthText_x,y:[9],[10] 
                self.spawntime = 1000//wave.zm_spawn
                wave.zm_spawncount -= 1*fps_proportion
                
                #만약 무한모드라면
                '''zm_count += 1'''
        self.spawntime -= 1

    def Atteck_Die(self):
        global score,zombie_blood_list

        for Zmp in self.list:
            #atteck
            Zmp_rect = self.img.get_rect()
            Zmp_rect.topleft = (Zmp[0],Zmp[1])
            if Zmp_rect.colliderect(player.h_rect):
                if Zmp[6] == 0:
                    player.health -= 1
                    blood_splash.spawn(player.x,player.y,3,3,(255,0,0))
                    score -= 100
                    Zmp[6] = zombie_melee_crash_player_time        
                    self.ph_sound = True  
                    player.ph_e_appear = True   
                    player.ph_e_transparent = player.ph_e_transparent_initval
                    player_hurt.ph_e_transparent = player_hurt.ph_e_transparent_initval
            if Zmp[6] != 0:
                Zmp[6] -= 1
            #die
            if Zmp[5] <= 0:
                score += 100
                wave.killzombie += 1
                wave.Z_left -= 1
                zombie_blood.list.append([Zmp[0]-(zombie_blood.width-self.width)/2,Zmp[1]+25,zombie_blood.ShowingTime])
                blood_splash.spawn(Zmp[0],Zmp[1],7,1.7,(255,0,0))
                lastzombie_effect.spawn(middle(Zmp[0],self.width,0),middle(Zmp[1],self.height,0),10,0.35,lastzombie_effect.color)
                self.die = True
                self.list.remove(Zmp)

    def move(self):   
        for Zm in self.list: #Zm:근접좀비
            Zm[0] += Zm[2] 
            Zm[1] += Zm[3]
            Zm[4] = math.atan2(player.y-Zm[1],player.x-Zm[0]) #라디안
            Zm[2] = math.cos(Zm[4])*self.speed*fps_proportion
            Zm[3] = math.sin(Zm[4])*self.speed*fps_proportion   

    def HealthText(self):
        #순서대로 실행 돼야함
        for zm in self.list:
            zm[8] = text_set(gamefont,15,False,False,'🛡' if zm[5]>1 else '',False,white)
            text_width,text_height = zm[8].get_size()
            zm[9] = zm[0]
            zm[10] = zm[1]
                
    def draw(self):
        global Graphic
        
        for Zm in self.list:
            if Zm[7] == True:
                if Graphic == 0:
                    pg.draw.rect(screen,(5, 167, 0),(Zm[0],Zm[1],self.width,self.height))
                else:
                    screen.blit(self.img_Lflip,(Zm[0],Zm[1]))
            else:
                if Graphic == 0:
                    pg.draw.rect(screen,(5, 167, 0),(Zm[0],Zm[1],self.width,self.height))
                else:
                    screen.blit(self.img,(Zm[0],Zm[1]))
    
            screen.blit(Zm[8],(Zm[9],Zm[10]))

    def sound(self,volume_die,volume_ph,volume_LastZombie):
        if self.die:
            Sound(assets,'zombie_die_sound.wav',volume_die)
            if wave.Z_left == 0:
                lastzombie_effect.sound(volume_LastZombie)
            self.die = False
            
        if self.ph_sound:
            Sound(assets,'player_hurt_sound.wav',volume_ph)
            self.ph_sound = False

    def update(self):
        self.spawn()
        self.move()
        self.Atteck_Die()
        self.HealthText()

        self.c_x = self.x + (self.width-self.c_width)/2
        self.c_y = self.y + (self.height-self.h_height)/2
        self.c_rect.topleft = (self.c_x,self.c_y)
        
#좀비(원거리)
class Zombie_shoot:
    def __init__(self):
        #zombie
        self.img = load_img(assets,'zombie_2.jpg').convert()
        self.width, self.height = self.img.get_size()
        self.rect = self.img.get_rect()
        self.speed = 2
        self.health = 1
        self.list = []
        self.bullet = []
        self.crash = False
        self.spawntime = zombie_shoot_spawntime
        self.x, self.y = 0,0
        self.die = False #사운드용
        #bullet
        self.b_img = load_img(assets,'zombie_bullet.png').convert()
        self.b_rect = self.b_img.get_rect()
        self.b_width, self.b_height = self.b_img.get_size()
        self.b_speed = 7
        self.shooting_time = zombie_shoot_shooting_time
        #플레이어 데미지 사운드
        self.ph_sound = False

    def spawn(self):
        if wave.zs_spawncount//1 >0:
            if self.spawntime <= 0:
                first_random = random.randint(1,4)
                if first_random == 1:
                    x_pos = random.randint(0,screen_width-self.width)
                    y_pos = -self.height+UIbar_height       
                elif first_random == 2:
                    x_pos = random.randint(0,screen_width-self.width)
                    y_pos = screen_height+UIbar_height       
                elif first_random == 3:
                    x_pos = -self.width
                    y_pos = random.randint(UIbar_height,screen_height+UIbar_height-self.height)
                elif first_random == 4:
                    x_pos = screen_width
                    y_pos = random.randint(UIbar_height,screen_height+UIbar_height-self.height)
                self.x = x_pos
                self.y = y_pos
                self.angle = 0
                self.dx = 0
                self.dy = 0
                self.list.append([self.x,self.y,self.dx,self.dy,self.angle,self.health,self.bullet,self.shooting_time,self.crash])
                                # x:[0] y:[1] dx:[2] dy[3] angle[4] health[5] bullet[6] shooting_time[7] crash[8]
                self.spawntime = 1000//wave.zs_spawn
                wave.zs_spawncount -= 1*fps_proportion                
                #만약 무한모드라면
                '''zs_count += 1'''
        self.spawntime -= 1

    def Basic(self):
        global score, wave_killzombie
        for Zs in self.list:
            #move 
            if not 100 <= Zs[0] <= screen_width-100 - self.width or \
                not 100+UIbar_height <= Zs[1] <= screen_height+UIbar_height-100 - self.height:
                Zs[0] += Zs[2] 
                Zs[1] += Zs[3]
            Zs[4] = math.atan2(player.y-Zs[1],player.x-Zs[0])
            Zs[2] = math.cos(Zs[4])*self.speed
            Zs[3] = math.sin(Zs[4])*self.speed          
            #spawn bullet
            if Zs[7] == 0:
                self.b_x = Zs[0] + (self.width - self.b_width)/2
                self.b_y = Zs[1] + (self.height - self.b_height)/2
                self.b_dx = math.cos(Zs[4])*self.b_speed
                self.b_dy = math.sin(Zs[4])*self.b_speed
                Zs[7] = zombie_shoot_shooting_time
                Zs[6].append([self.b_x,self.b_y,self.b_dx,self.b_dy])
            Zs[7] -= 1
            #die
            if Zs[5] <= 0:
                score += 100
                wave.killzombie += 1
                wave.Z_left -= 1
                zombie_blood.list.append([Zs[0]-(zombie_blood.width-self.width)/2,Zs[1]+25,zombie_blood.ShowingTime])
                blood_splash.spawn(Zs[0],Zs[1],7,1.7,(255,0,0))
                lastzombie_effect.spawn(middle(Zs[0],self.width,0),middle(Zs[1],self.height,0),10,0.35,lastzombie_effect.color)
                self.die = True
                self.list.remove(Zs)
    
    def Bullet(self):
        global score
        
        for Zb in self.bullet:
            self.b_rect.topleft = Zb[0], Zb[1]
            if Zb[0] >= screen_width or Zb[0] <= -self.b_width:
                self.bullet.remove(Zb)
            elif Zb[1] >= screen_width+UIbar_height or Zb[1] <= -self.b_width+UIbar_height:
                self.bullet.remove(Zb)
            #move
            Zb[0]+=Zb[2]
            Zb[1]+=Zb[3]
            #atteck
            if self.b_rect.colliderect(player.h_rect):
                self.bullet.remove(Zb)
                player.health -= 1
                blood_splash.spawn(player.x,player.y,3,3,(255,0,0))
                score -= 100    
                self.ph_sound = True
                player.ph_e_appear = True     
                player.ph_e_transparent = player.ph_e_transparent_initval    
                player_hurt.ph_e_transparent = player_hurt.ph_e_transparent_initval           
        
    def draw(self):
        for Zs in self.list:
            if Graphic == 0:
                pg.draw.rect(screen,(181, 223, 29),(Zs[0],Zs[1],self.width,self.height))
            else:
                screen.blit(self.img,(Zs[0],Zs[1]))

        for Zb in self.bullet:
            if Graphic == 0:
                pg.draw.rect(screen,(181, 223, 29),(Zb[0],Zb[1],self.b_width,self.b_height))
                pg.draw.rect(screen,(215, 33, 19),(Zb[0],Zb[1],self.b_width,self.b_height),2)
            else:
                screen.blit(self.b_img,(Zb[0],Zb[1]))

    def sound(self,volume_bullet,volume_die,volume_ph,volume_LastZombie):
        for Zs in self.list:
            if Zs[7] == 0:
                Sound(assets,'zombie_bullet_sound.wav',volume_bullet)
        if self.die:
            Sound(assets,'zombie_die_sound.wav',volume_die)
            if wave.Z_left == 0:
                lastzombie_effect.sound(volume_LastZombie)
            self.die = False
        if self.ph_sound:
            Sound(assets,'player_hurt_sound.wav',volume_ph)
            self.ph_sound = False
          
    def update(self):
        self.spawn()
        self.Basic()
        self.Bullet()

#체력바
class PlayerHealth_UI:
    def __init__(self):
        self.img = load_img(assets,'PlayerHealth_UI.png').convert_alpha()
        self.board_width,self.board_height = 350,50
        self.board_x = middle(0,screen_width,self.board_width)
        self.board_y = 50
        self.HealthColor = (238, 61, 61)
        self.LineColor = (104, 36, 36)
        self.DecimalPoint_discrimination = int(player.health)+1 if round(player.health,1) != 0 else int(player.health)

    def draw(self):
        #체력 표시
        pg.draw.rect(screen,self.HealthColor,[self.board_x,self.board_y,\
                        self.board_width*(player.health/player.max_health),self.board_height])
        #부가 이미지
        #screen.blit(self.img,[self.board_x,self.board_y])
        #보드
        pg.draw.rect(screen,self.LineColor,[self.board_x,self.board_y,self.board_width,self.board_height],3)
        #세로선
        line_x = self.board_x
        for i in range(int(player.max_health)-1 if player.health-int(player.max_health) == 0 else int(player.max_health)):
            line_x += self.board_width/int(player.max_health) if player.max_health-int(player.max_health) == 0 else int(player.max_health)+1
            pg.draw.line(screen,self.LineColor,(line_x,self.board_y),(line_x,self.board_y+self.board_height-3),2)

#칼 쿨타임바
class KnifeCooltime_UI:
    def __init__(self):
        self.board_width,self.board_height = 190, 25
        self.board_x = middle(ph_ui.board_x+ph_ui.board_width,\
                    screen_width-(ph_ui.board_x+ph_ui.board_width),self.board_width) #UI클래스의 T_knife
        self.board_y = 55
        self.board_color = (77, 135, 135)

    def draw(self):
        pg.draw.rect(screen,(126, 222, 226),[self.board_x,self.board_y,\
                    self.board_width*(knife.cooltime/knife.cooltime_init),self.board_height])
        pg.draw.rect(screen,self.board_color,[self.board_x,self.board_y,self.board_width,self.board_height],3)

#좀비 죽었을 때 핏자국
class ZombieBlood:
    def __init__(self):
        self.list = []
        self.width,self.height = 20,10
        self.ShowingTime = 180

    def update(self):
        for i in self.list:
            if i[2] > 0:
                i[2] -= 1
            else:
                self.list.remove(i)

    def draw(self):
        for i in self.list:
            screen.blit(rect_alpha(self.width,self.height,(255,0,0),150),[i[0],i[1]])

#배경 파티클
class Particle:
    def __init__(self):
        self.object = []
        self.color = (0,0,0)
        self.spawntime = 0
        self.VisibleTime = 240
        self.MaxAlpha = 150

    def spawn(self):
        if self.spawntime <= 0 and len(self.object) <= 20:
            SideLength = random.randint(5,7)
            x_pos = random.randint(0,screen_width-SideLength)
            y_pos = random.randint(UIbar_height,screen_height-SideLength)
            dx = random.randrange(-100,100)/100
            dy = random.randrange(-100,100)/100
            c = random.randint(0,189)
            color = (c,c,c)
            self.spawntime = random.randint(0,30)
            self.object.append([x_pos,y_pos,dx,dy,self.VisibleTime,0,SideLength,color])
        self.spawntime -= 1
    
    def draw(self):
        for i in self.object:
            particle = rect_alpha(i[6],i[6],i[7],i[5])
            screen.blit(particle,(i[0],i[1]))

    def move(self,i):
        i[0] += i[2]
        i[1] += i[3]

    def visibletime(self,i):
        if i[4] >= self.VisibleTime-90 and i[5] < self.MaxAlpha:
            i[5] += 3
        if i[4] <= 0:
            self.object.remove(i)
        if i[4] <= 60:
            i[5] -= 5
        i[4] -= 1

    def update(self):
        self.spawn()
        for i in self.object:
            self.move(i)
            self.visibletime(i)

#웨이브에서 마지막 좀비를 죽였을 때 효과
class LastZombie_Effect:
    def __init__(self):
        self.color = (255,255,255)
        self.object = []

    def spawn(self,x:float,y:float,speed:float,increase_speed:float,color:tuple):
        """
        웨이브에서 마지막 좀비일 때 스폰
            (``if문 내장``)
        """
        if wave.Z_left == 0:
            size = 0
            self.object.append([x,y,size,speed,increase_speed,color])
                            #x:[0], y:[1], size[2], speed[3], increase_speed[4], color[5]

    def delete(self,i):
        if i[2] > screen_width:
            self.object.remove(i)

    def size_update(self,i):
        i[2] += i[3]
        i[3] += i[4]

    def sound(self,volume):
        Sound(assets,'LastZombie_sound.wav',volume)

    def draw(self):
        for i in self.object:
            pg.draw.circle(screen,i[5],(i[0],i[1]),i[2],3)

    def update(self):
        for i in self.object:
            self.size_update(i)
            self.delete(i)
    
#카드 선택할 때 효과
class CardSelect_Effect:
    def __init__(self):
        self.color = {'upgrade':(112, 163, 188),'heal':(79, 210, 102),'grenade':(255, 148, 0)}
        self.object = []
        self.speed = 10
        self.increase_speed = 0.04

    def spawn(self,x:float,y:float,speed:float,increase_speed:float,color):
        size = screen_width/3
        self.object.append([x,y,size,speed,increase_speed,color])
                        #x:[0], y:[1], size[2], speed[3], increase_speed[4], color[5]

    def Upgrade(self):
        return cardselect_effect.spawn(0,0,cardselect_effect.speed,cardselect_effect.increase_speed,cardselect_effect.color['upgrade'])

    def Heal(self):
        return cardselect_effect.spawn(0,0,cardselect_effect.speed,cardselect_effect.increase_speed,cardselect_effect.color['heal'])

    def Grenade(self):
        return cardselect_effect.spawn(0,0,cardselect_effect.speed,cardselect_effect.increase_speed,cardselect_effect.color['grenade'])

    def delete(self,i):
        if i[2] <= 0:
            self.object.remove(i)

    def size_update(self,i):
        i[2] -= i[3]
        i[3] += i[4]
    
    def move(self,i):
        i[0] = middle(player.x,player.width,0)
        i[1] = middle(player.y,player.h_height,0)

    def sound(self,volume):
        #Sound(assets,'LastZombie_sound.wav',volume)
        pass

    def draw(self):
        for i in self.object:
            pg.draw.circle(screen,i[5],(i[0],i[1]),i[2],3)

    def update(self):
        for i in self.object:
            self.size_update(i)
            self.move(i)
            self.delete(i)

#피튀기는 효과
class BloodSplash:
    def __init__(self):
        self.object = []
        self.SideLength = 5
        self.SubtractionDegree = 0.1
        self.zombie_die = False

    def spawn(self,object_x,object_y,amount,speed,color): #speed : 맞았을 때 1 죽었을 때 2
        self.object.append([])
        for i in range(0,amount):
            self.object[-1].append([object_x+(30-self.SideLength)/2,object_y+(30-self.SideLength)/2,\
                        random.randint(-100,100)/100,random.randint(-450,-200)/100,object_y+30,speed,color])
                        #x:[0], y:[0], x범위:[2], y범위:[3], 파티클 끝나는 지점:[4], speed[5], color:[6]
    def draw(self):
        for I in self.object:
            for i in I:
                pg.draw.rect(screen,i[6],(i[0],i[1],self.SideLength,self.SideLength))

    def move(self):
        for I in self.object:
            for i in I:
                i[0] += i[2]
                i[1] += i[3]
                i[3] += self.SubtractionDegree*i[5]

    def delete(self):
        for I in self.object:
            for i in I:
                if i[1] > i[4]:
                    I.remove(i)
            if len(I) == 0:
                self.object.remove(I)

    def update(self):
        self.move()
        self.delete()

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

    def spawn(self,StartPoint_x,StartPoint_y,count,speed,DecreaseSpeed):
        degree = 0
        for i in range(count):
            R = 255
            G = random.randint(80,130)
            B = random.randint(150,180)
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

    def move(self,i,j):
        j[0] += j[2] #x += dx
        j[1] += j[3] #y += dy
        j[2] /= j[4] #dx -= decrease speed
        j[3] /= j[4] #dy -= decrease speed
        
    def alpha(self,i,j):
        if j[8] > 20:
            j[7] -= 20
        j[8] += 1

    def delete(self,i,j):
        if j[7] <= 0:
            self.object.remove(i)

    def draw(self):
        for i in self.object:
            for j in i:
                screen.blit(rect_alpha(j[6],j[6],j[5],j[7]),(j[0],j[1]))

    def update(self):
        for i in self.object:
            for j in i:
                self.move(i,j)
                self.alpha(i,j)
                self.delete(i,j)

#좀비 충돌
def Crash_Zombie(zm,zs):
        a_index, b_index = 0,0
        for Zm1 in zm.list:
            for Zm2 in zm.list:
                if a_index != b_index:
                    Zm1_rect,Zm2_rect = zm.crashbox.get_rect(), zm.crashbox.get_rect()
                    Zm1_rect.topleft,Zm2_rect.topleft = (Zm1[0],Zm1[1]), (Zm2[0],Zm2[1])
                    if Zm1_rect.colliderect(Zm2_rect):
                        Zm1_angle = math.atan2(Zm1[1]-Zm2[1],Zm1[0]-Zm1[0]) #math.cos또는sin(Zm1_angle)*zm.speed

                        ZombieCrash_RandomMove = random.choice([0,1]) #랜덤 움직임 정하는 값

                        ZombieCrashMove_x = math.cos(Zm1_angle)*zm.speed*2
                        ZombieCrashMove_y = math.sin(Zm1_angle)*zm.speed*2

                        if math.dist((Zm1[0],Zm1[1]),(player.x , player.y)) \
                            < math.dist((Zm2[0],Zm2[1]),(player.x , player.y)):
                            Zm2[2] = -Zm1[2]
                            Zm2[3] = -Zm1[3]
                        else:
                            Zm1[2] = -Zm2[2]
                            Zm1[3] = -Zm2[3] 
                b_index += 1
            b_index = 0
            a_index += 1 
        a_index, b_index = 0,0  
        for Zs1 in zs.list:
            for Zs2 in zs.list:
                if a_index != b_index:
                    Zs1_rect,Zs2_rect = zs.img.get_rect(), zs.img.get_rect()
                    Zs1_rect.topleft,Zs2_rect.topleft = (Zs1[0],Zs1[1]), (Zs2[0],Zs2[1])
                    if Zs1_rect.colliderect(Zs2_rect):
                        Zs1[8],Zs2[8] = True,True
                        #Zm1_angle = math.atan2(Zs1[1]-Zm2[1],Zs1[0]-Zs1[0]) #math.cos또는sin(Zm1_angle)*zm.speed
                        if math.dist((Zs1[0],Zs1[1]),(player.x , player.y)) \
                            < math.dist((Zs2[0],Zs2[1]),(player.x , player.y)):
                            Zs2[2] = 0
                            Zs2[3] = 0
                            Zs1[2] = 0
                            Zs1[3] = 0                 
                    else:
                        Zs1[8],Zs2[8] = False,False
                b_index += 1
            b_index = 0
            a_index += 1 

#시간마다 점수 (현재 사용 안 함)
def Timegoing():
    global Time,score
    if Time <= 0:
            score += 10
            Time = 60
    Time -= 1

#클릭(이미 코드에 넣어서 굳이 없애진 않지만 click event로 하는게 훨씬 나음)
def Click(u):
    if click_left:
        u.pressing_mouse = u.pressing_mouse_initialval
    else:
        if u.pressing_mouse > 0:
            u.pressing_mouse -= 1

#UI
class UI:
    def __init__(self):
        self.T_health = ["health","체력"]
        self.T_knife = [["knife cooltime",25],["칼 쿨타임",30]]
        self.T_grenade = ["grenade","수류탄 개수"]
        self.T_wave = ["wave","웨이브"]
        self.T_score = ["score","점수"]
        self.T_WaveTime = ['wave time remaining','웨이브 남은 시간']
        self.T_ZombieLeft = ['zombies left','남은 좀비']

    def draw(self):
        #화면 테두리
        pg.draw.rect(screen,(140,140,140),[0,0,screen_width,screen_height+UIbar_height],3)
        #UI바
        pg.draw.rect(screen,(0,0,0),[0,0,screen_width,UIbar_height],0)
        pg.draw.rect(screen,set_color,[0,0,screen_width,UIbar_height],3)
        #체력
        '''text_health = text_set(gamefont, 50, False, False,f"{self.T_health[lg]} : {player.health:0.1f}/{max_health}", True, (254, 46, 66))
        screen.blit(text_health, (screen_width/2-(text_health.get_rect())[2]/2,50))'''
        #칼 쿨타임
        text_k_cooltime = text_set(gamefont, self.T_knife[lg][1], False, True,f"{self.T_knife[lg][0]}", True, (126, 222, 226))
        screen.blit(text_k_cooltime, (middle(ph_ui.board_x+ph_ui.board_width,\
                    screen_width-(ph_ui.board_x+ph_ui.board_width),text_k_cooltime.get_size()[0]),20))
        #수류탄 개수
        text_bomb = text_set(gamefont, 30, False, True,f"{self.T_grenade[lg]} : {special_weapon_have}", True, (227, 134, 7))
        screen.blit(text_bomb, (middle(ph_ui.board_x+ph_ui.board_width,\
                    screen_width-(ph_ui.board_x+ph_ui.board_width),text_bomb.get_size()[0]),90))
        #웨이브
        text_wave = text_set(gamefont, 30, False, True,f"{self.T_wave[lg]} : {wave_count}", True, set_color)
        screen.blit(text_wave, (180,30))
        #점수
        text_score = text_set(gamefont, 30, False, True,f"{self.T_score[lg]} : {score}", True, (243, 240, 108))
        screen.blit(text_score, (180,80))
        #웨이브 시간
        text_wavetime = text_set(gamefont, 20, False, False,f"{self.T_WaveTime[lg]} {wave.time//60}", True, (255,255,255))
        screen.blit(text_wavetime, (screen_width/2-(text_wavetime.get_rect())[2]/2,20))
        #남은 좀비 수
        text_zombie_left = text_set(gamefont, 18, False, False, f"{int(wave.Z_left)} {self.T_ZombieLeft[lg]}", True, (71,200,62))
        screen.blit(text_zombie_left, (screen_width/2-(text_zombie_left.get_rect())[2]/2,110))

#게임
def Game():
    global wave_time,Upgrading
    if main_menu.bool == False:
        if Upgrading == False and pause.bool == False:
            #시간
            #Timegoing()
            #업데이트
            player.update()
            atteck_dir.update()
            bullet.update() 
            knife.update()
            zombie_melee.update()
            zombie_shoot.update()
            bomb.update()
            zombie_blood.update()
            particle.update()
            blood_splash.update()
            bomb_splash.update()
            lastzombie_effect.update()
            cardselect_effect.update()
            
            #사운드 (wave사운드는 맨 Wave함수와 묶음)
            bullet.sound(set_sound(0.1,volume,volume_max))
            bomb.sound(set_sound(0.5,volume,volume_max))
            knife.sound(set_sound(0.3,volume,volume_max))
            zombie_shoot.sound(set_sound(0.5,volume,volume_max),set_sound(0.5,volume,volume_max),set_sound(0.3,volume,volume_max),set_sound(0.5,volume,volume_max))
            zombie_melee.sound(set_sound(0.5,volume,volume_max), set_sound(0.3,volume,volume_max),set_sound(0.5,volume,volume_max))
            player.sound(set_sound(0.4,volume,volume_max))
        
        #그리기
        lastzombie_effect.draw()
        cardselect_effect.draw()
        zombie_blood.draw()
        bullet.draw()
        atteck_dir.draw()
        zombie_shoot.draw()
        player.draw()
        player.hurt_effect()
        zombie_melee.draw()
        knife.draw()
        blood_splash.draw()
        bomb_splash.draw()
        bomb.draw()
        particle.draw()
        ui.draw()
        ph_ui.draw()
        kc_ui.draw()
        target_mouse.draw()
        
        #클릭
        #Click(upgrade)

        #체력이 적을 때 효과
        #Almostdie()
        
        #맞았을 때 효과
        player_hurt.effect()

        #일시정지 메뉴
        if pause.bool == True:
            pause.draw()

#웨이브
class Wave:
    def __init__(self):
        #스폰 수
        self.zm_spawn = 3
        self.zs_spawn = 0
        self.zm_spawn_startval = self.zm_spawn
        self.zs_spawn_startval = self.zs_spawn
        self.zm_spawncount = self.zm_spawn
        self.zs_spawncount = self.zs_spawn
        #남은 좀비 수
        self.Z_left = 0
        #웨이브
        self.time = 0
        self.killzombie = 0
        self.fontalpha = 255
        self.fontdraw = False
        #카드 나오는 시간
        self.WaitForCard = 60

    def SetWave(self):
        global wave_count

        wave_count += 1
        self.WaitForCard = 60
        self.fontdraw = True
        self.time = 3600
        self.fontalpha = 230
        self.killzombie = 0

        self.zm_spawn = self.zm_spawn_startval + 1.3*wave_count
        self.zs_spawn = self.zs_spawn_startval + 0.55*wave_count
        self.zm_spawncount = self.zm_spawn
        self.zs_spawncount = self.zs_spawn

        self.Z_left += self.zm_spawn//1 + self.zs_spawn//1

        zombie_melee.spawntime = 1000//self.zm_spawn
        zombie_shoot.spawntime = 1000//self.zs_spawn

        upgrade.card_count = random.randint(2,3)
        upgrade.card_appear = True

    def sound(self,volume):
        Sound(assets,'wave change.wav',volume)

    def draw(self):
        global wave_count

        if self.fontalpha > 0 and self.fontdraw:
            self.fontalpha -= 2.3

            T_ZombieLeft = ["zombies left","좀비 남음"]

            text_wave = text_set('Times new Roman',150, True, False,f"WAVE {wave_count}", True, set_color)
            text_ZombieLeft = text_set(gamefont,30, False, True,f"{int(self.Z_left)} {T_ZombieLeft[lg]}", True, (213,213,213))
            text_wave.set_alpha(self.fontalpha)
            text_ZombieLeft.set_alpha(self.fontalpha)
            screen.blit(text_wave,(middle(0,screen_width,text_wave.get_size()[0]),\
                        middle(0,screen_height+UIbar_height,text_wave.get_size()[1])))
            screen.blit(text_ZombieLeft,(middle(0,screen_width,text_ZombieLeft.get_size()[0]),\
                        middle(0,screen_height+UIbar_height,text_ZombieLeft.get_size()[1]-200)))
        else:
            self.fontdraw = False

    def work(self):
        if self.time == 0 or self.Z_left == 0:
            if self.WaitForCard > 0:
                if wave_count == 0:
                    zombie_melee.list.clear()
                    zombie_shoot.list.clear()
                    zombie_shoot.bullet.clear()
                self.WaitForCard -= 1
            else:
                if Upgrading == False:
                    self.SetWave()
                    self.sound(set_sound(0.7,volume,volume_max))
        self.draw()

#업그레이드
class Upgrade:
    def __init__(self):
        self.width,self.height = 150,300
        self.middlecard_x = screen_width/2-self.width/2
        self.y = (UIbar_height+screen_height-self.height)/2
        self.space = 70
        self.pos = []
        self.card = []
        self.card_appear = True
        self.select_card = -1
        self.pressing_mouse_initialval = 2
        self.pressing_mouse = 0 #눌렀을 때 초기값 됨, 뗐을 때 0까지 1틱당 1씩 줄어듬
        self.add_card = False
        #레벨 제한이 필요한 업그레이드
        self.maxlevel = 10
        self.firegun_level = 0
        self.knife_size_level = 0
        self.knife_cooltime_level = 0
        self.health_level = 0
        self.speed_level = 0
        #업그레이드 후 업그레이드 항목 표시
        self.UpgradeItem_text_VisibleTime = 0
        self.UpgradeItem_text_alpha = 255
        #랜덤 카드 개수
        self.card_count = random.randint(2,3)
        
    def random(self):
        while not len(self.card) == self.card_count:
            get_random = random.randint(0,7)
            if len(self.card) != 0:
                if not get_random in self.card:
                    self.add_card = True
                    for r in [4,5]: #4,5 겹치지 않게하기
                        if r == get_random:
                            if [4,5][[4,5].index(r)-1] in self.card:
                                self.add_card = False  

                if self.add_card == True:
                    self.card.append(get_random)
                    self.add_card = False
            else:
                self.card.append(get_random)

    def select_process(self):
        global between_wave,Upgrading,special_weapon                
        
        for c in self.pos:        
            if collide_with_point(mouse_x,mouse_y,c[0],c[1],self.width,self.height):
                Upgrading = False
                self.select_card = self.card[self.pos.index(c)]
                knife.cooltime = 0
                self.pos.clear()    
                self.card.clear() 
                self.UpgradeItem_text_VisibleTime = 120
                self.UpgradeItem_text_alpha = 255  

        self.select()

    def select(self):
        global knife_atteck_term,special_weapon_have,max_health,knife_increase_size
        sc = self.select_card
        if sc == 0:  #공격 속도 증가
            sc0 = 5.5
            cardselect_effect.Upgrade()
            if self.firegun_level < self.maxlevel:
                self.firegun_level += 1
                bullet.fire_term_init -= sc0
            else:
                special_weapon_have += 1
        elif sc == 1:  #칼 크기 증가
            sc1 = 8
            cardselect_effect.Upgrade()
            if self.knife_size_level < self.maxlevel:
                self.knife_size_level += 1
                self.increase_size += sc1
            else:
                special_weapon_have += 1
        elif sc == 2: #칼 쿨타임 감소
            sc2 = 9
            cardselect_effect.Upgrade()
            if self.knife_cooltime_level < self.maxlevel:
                self.knife_cooltime_level += 1
                knife.cooltime_init -= sc2
            else:
                special_weapon_have += 1
        elif sc == 3: #수류탄 +2
            special_weapon_have += 2
            cardselect_effect.Grenade()
        elif sc == 4: #힐(최대체력의 50%)
            player.health += player.max_health//2
            if player.health > player.max_health:
                player.health = player.max_health
            cardselect_effect.Heal()
        elif sc == 5: #힐(100%)
            player.health = player.max_health
            cardselect_effect.Heal()
        elif sc == 6: #최대 체력 증가
            sc6 = 1
            cardselect_effect.Upgrade()
            if self.health_level < self.maxlevel:
                health_percent = player.health/player.max_health
                player.max_health += sc6
                player.health = player.max_health*health_percent
                self.health_level += 1
            else:  #레벨이 최대일 때
                special_weapon_have += 1
        elif sc == 7: #이동속도 증가
            sc7 = 0.3
            cardselect_effect.Upgrade()
            if self.speed_level < self.maxlevel:
                self.speed_level += 1
                player.normal_speed += sc7
            else:
                special_weapon_have += 1

    def UpgradeList(self):
        T_SSpeed = [("increase shooting speed",11),("총 공격 속도 증가",15)]
        T_KSize = [("increase knife size",14),("칼 크기 증가",15)]
        T_KCool = [("decrease knife cooltime",10),("칼 쿨타임 감소",15)]
        T_G = [("grenade +2",15),("수류탄 +2",15)]
        T_Hh = [("heal (50% of max health)",10),("힐(최대체력의 50%)",15)]
        T_Hf = [("heal (100%)",15),("힐 (100%)",15)]
        T_MH = [("increase max health",12),("최대 체력 증가",15)]
        T_PS = [("increase moving speed",11),("이동 속도 증가",15)] 

        self.upgrade_list = []
        self.upgrade_list.append([(T_SSpeed[lg][0],T_SSpeed[lg][1]),f"{self.firegun_level}/{self.maxlevel} level"]) #0
        self.upgrade_list.append([(T_KSize[lg][0],T_KSize[lg][1]),f"{self.knife_size_level}/{self.maxlevel} level"]) #1
        self.upgrade_list.append([(T_KCool[lg][0],T_KCool[lg][1]),f"{self.knife_cooltime_level}/{self.maxlevel} level"]) #2
        self.upgrade_list.append([(T_G[lg][0],T_G[lg][1])]) #3
        self.upgrade_list.append([(T_Hh[lg][0],T_Hh[lg][1])]) #4
        self.upgrade_list.append([(T_Hf[lg][0],T_Hf[lg][1])]) #5
        self.upgrade_list.append([(T_MH[lg][0],T_MH[lg][1]),f"{self.health_level}/{self.maxlevel} level"]) #6
        self.upgrade_list.append([(T_PS[lg][0],T_PS[lg][1]),f"{self.speed_level}/{self.maxlevel} level"]) #7

    def UpgradeItem_Text(self):
        if self.UpgradeItem_text_VisibleTime > 0:
            text = text_set(gamefont,self.upgrade_list[self.select_card][0][1],False,True,\
                                self.upgrade_list[self.select_card][0][0],True,(50,216,255))
            text_width,text_height = text.get_size()

            if self.UpgradeItem_text_VisibleTime <= 30:
                text.set_alpha(self.UpgradeItem_text_alpha)
                self.UpgradeItem_text_alpha -= 10
                
            screen.blit(text,(middle(0,screen_width,text_width),600))

            self.UpgradeItem_text_VisibleTime -= 1
        
    def draw(self):   
        effect_SpaceWithBox = 20
        for c in self.pos: 
            pg.draw.rect(screen,(0,0,0),[c[0],c[1],self.width,self.height],0)
            pg.draw.rect(screen,set_color,[c[0],c[1],self.width,self.height],3)
            #효과
            if collide_with_point(mouse_x,mouse_y,c[0],c[1],self.width,self.height):
                pg.draw.rect(screen,(192,192,192),[c[0]-effect_SpaceWithBox,c[1]-effect_SpaceWithBox,\
                                self.width+effect_SpaceWithBox*2,self.height+effect_SpaceWithBox*2],3)

        for cd in self.card:
            cd_index = self.card.index(cd)
            text_ug_des = text_set(gamefont, self.upgrade_list[self.card[cd_index]][0][1], False, False,\
                                    f"{self.upgrade_list[self.card[cd_index]][0][0]}",True,(255,255,255))
            try:
                middle_font_x = self.pos[cd_index][0]+(self.width-text_ug_des.get_size()[0])/2
                middle_font_y = self.pos[cd_index][1]+(self.height-text_ug_des.get_size()[1])/2
                screen.blit(text_ug_des, (middle_font_x,middle_font_y)) 

                text_ug_level = text_set(gamefont, 15, False, False, f"{self.upgrade_list[self.card[cd_index]][1]}", True, (0,216,255))
                screen.blit(text_ug_level, (middle_font_x+(text_ug_des.get_size()[0]-text_ug_level.get_size()[0])/2,middle_font_y+30)) 
                
                T_ML = ["+1 grenade when choosing highest level card","최고 레벨인 카드를 선택할 시 수류탄 +1"]
                text_detail_des = text_set(gamefont, 25, False, True, T_ML[lg], True, (166,166,166))
                screen.blit(text_detail_des, ((screen_width-text_detail_des.get_size()[0])/2,500+UIbar_height))    
            except:pass
    
    def sound(self,volume):
        if wave.WaitForCard == 0 and self.card_appear == True:
            card_sound = pg.mixer.Sound(os.path.join(assets,'card_sound.wav'))
            pg.mixer.Sound.set_volume(card_sound, volume)
            card_sound.play()
            self.card_appear = False

    def work(self):
        global Upgrading
        #self.UpgradeItem_Text()
        self.sound(set_sound(2,volume,volume_max))

        if wave.WaitForCard <= 0:
            Upgrading = True

            pg.mouse.set_visible(True) 

            self.random()
            self.draw()

        elif wave.WaitForCard == 1:
            self.UpgradeList()

            if self.card_count == 2:
                self.pos.append([screen_width/2-self.width-self.space/2,self.y])
                self.pos.append([screen_width/2+self.space/2,self.y])

            if self.card_count == 3:        
                self.pos.append([self.middlecard_x-self.width-self.space,self.y])
                self.pos.append([self.middlecard_x,self.y])
                self.pos.append([self.middlecard_x+self.width+self.space,self.y])

#게임 오버
class GameOver:
    def __init__(self):
        self.gameover_sound_play = 0
        self.bool = False
        #재시작 버튼
            #박스
        self.rb_box_width,self.rb_box_height = 230,70
        self.rb_box_x = middle(0,screen_width,self.rb_box_width)
        self.rb_box_y = 500
            #텍스트
        self.rb_text = text_set(gamefont,30,False,False,'재시작',True,white)
        self.rb_text_width,self.rb_text_height = self.rb_text.get_size()
        self.rb_text_x = middle(self.rb_box_x,self.rb_box_width,self.rb_text_width)
        self.rb_text_y = middle(self.rb_box_y,self.rb_box_height,self.rb_text_height)

    def draw(self):
        global special_weapon,gameover_sound_play,score_data
        if player.health <= 0:
            screen.fill((background_color))

            #line
            pg.draw.rect(screen,(91,91,91),(0,0,screen_width,screen_height+UIbar_height),7)
            #text
            text_die_message = text_set(gamefont,30,False,True,"더 이상 버티지 못하였습니다...",True,(180,180,180))
            screen.blit(text_die_message,(screen_width/2-(text_die_message.get_rect())[2]/2,UIbar_height+30))
            
            text_totalwave = text_set(gamefont, 70, False,False,f"wave : {wave_count}",True,set_color)
            screen.blit(text_totalwave, (screen_width/2-(text_totalwave.get_rect())[2]/2,\
                screen_height/2-(text_totalwave.get_rect())[3]/2+UIbar_height/2-70))

            text_totalscore = text_set(gamefont, 50, False, True,f"점수 : {score}",True, (243, 240, 108))
            screen.blit(text_totalscore, (screen_width/2-(text_totalscore.get_rect())[2]/2,\
                screen_height/2-(text_totalscore.get_rect())[3]/2+UIbar_height/2+30))      

            #재시작 버튼
            pg.draw.rect(screen,(51,51,51),(self.rb_box_x,self.rb_box_y,self.rb_box_width,self.rb_box_height))     
            pg.draw.rect(screen,white,(self.rb_box_x,self.rb_box_y,self.rb_box_width,self.rb_box_height),3)
            screen.blit(self.rb_text,(self.rb_text_x,self.rb_text_y))

    def click(self):
        global ResetGame

        if collide_with_point(mouse_x,mouse_y,self.rb_box_x,self.rb_box_y,self.rb_box_width,self.rb_box_height):
            ResetGame = True
            self.bool = False
            self.gameover_sound_play = 0

    def sound(self,volume):
        if self.gameover_sound_play <= 2:
            self.gameover_sound_play += 1
        if self.gameover_sound_play == 2:
            Sound(assets,'player_die_sound.wav',volume)

    def work(self):
        pg.mouse.set_visible(True)

        self.draw()
        self.sound((set_sound(1.7,volume,volume_max)))  

        SaveScore(wave_count,score)

#일시정지 메뉴
class Pause:
    def __init__(self):
        self.bool = False
        self.restart = False
        self.mainmenu = False
        #색깔
        self.board_color = black
        self.boardLine_color = (189,189,189)
        self.BoxLine_color = (255,255,255)
        self.Box_color = (51,51,51)
        #크기
        self.board_width,self.board_height = 450, 340
        self.RestartBox_width,self.RestartBox_height = 190, 70
        self.MainmenuBox_width,self.MainmenuBox_height = 240, 70
        #버튼끼리의 거리
        self.box_space = 30
        #좌표 (1.판 2.버튼)
            #판
        self.board_x = (screen_width-self.board_width)/2
        self.board_y = (screen_height+UIbar_height-self.board_height)/2
            #재시작 버튼
        self.RestartBox_x = middle(self.board_x,self.board_width,self.RestartBox_width)
        self.RestartBox_y = middle(self.board_y,self.board_height,self.RestartBox_height)-self.RestartBox_height/2-self.box_space/2
            #메인메뉴 버튼
        self.MainmenuBox_x = middle(self.board_x,self.board_width,self.MainmenuBox_width)
        self.MainmenuBox_y = middle(self.board_y,self.board_height,self.MainmenuBox_height)+self.MainmenuBox_height/2+self.box_space/2

        #텍스트 
            #설정,크기
        T_P = ["pause","일시정지"]
        self.T_pause = text_set(gamefont,25,False,False,T_P[lg],True,self.BoxLine_color)
        self.T_pause_width,self.T_pause_height = self.T_pause.get_size()

        T_R = ["restart","재시작"]
        self.T_Restart = text_set(gamefont,25,False,False,T_R[lg],True,(255,255,255))
        self.T_Restart_width,self.T_Restart_height = self.T_Restart.get_size()

        T_M = ["main menu","메인 메뉴"]
        self.T_Mainmenu = text_set(gamefont,25,False,False,T_M[lg],True,(255,255,255))
        self.T_Mainmenu_width,self.T_Mainmenu_height = self.T_Mainmenu.get_size()
        
        T_E = ["press 'ESC' to cancle","ESC로 취소"]
        self.T_description = text_set(gamefont,25,False,False,T_E[lg],True,(140,140,140))
        self.T_description_width,self.T_description_height = self.T_description.get_size()
            #좌표
        self.T_pause_x = middle(self.board_x,self.board_width,self.T_pause_width)
        self.T_pause_y = self.board_y+15

        self.T_Restart_x = middle(self.RestartBox_x,self.RestartBox_width,self.T_Restart_width)
        self.T_Restart_y = middle(self.RestartBox_y,self.RestartBox_height,self.T_Restart_height)

        self.T_Mainmenu_x = middle(self.MainmenuBox_x,self.MainmenuBox_width,self.T_Mainmenu_width)
        self.T_Mainmenu_y = middle(self.MainmenuBox_y,self.MainmenuBox_height,self.T_Mainmenu_height)

        self.T_description_x = middle(self.board_x,self.board_width,self.T_description_width)
        self.T_description_y = self.board_y+self.board_height-self.T_description_height-30

    def draw(self):
        #배경
        screen.blit(rect_alpha(screen_width,screen_height+UIbar_height,black,100),(0,0))
        #판
        pg.draw.rect(screen,self.board_color,(self.board_x,self.board_y,self.board_width,self.board_height))
        pg.draw.rect(screen,self.boardLine_color,(self.board_x,self.board_y,self.board_width,self.board_height),3)
        #버튼 (박스)
            #재시작
        pg.draw.rect(screen,self.Box_color,(self.RestartBox_x,self.RestartBox_y,self.RestartBox_width,self.RestartBox_height))
        pg.draw.rect(screen,self.BoxLine_color,(self.RestartBox_x,self.RestartBox_y,self.RestartBox_width,self.RestartBox_height),3)
            #메인 메뉴
        pg.draw.rect(screen,self.Box_color,(self.MainmenuBox_x,self.MainmenuBox_y,self.MainmenuBox_width,self.MainmenuBox_height))
        pg.draw.rect(screen,self.BoxLine_color,(self.MainmenuBox_x,self.MainmenuBox_y,self.MainmenuBox_width,self.MainmenuBox_height),3)
        #텍스트
        screen.blit(self.T_pause,(self.T_pause_x,self.T_pause_y))
        screen.blit(self.T_Restart,(self.T_Restart_x,self.T_Restart_y))
        screen.blit(self.T_Mainmenu,(self.T_Mainmenu_x,self.T_Mainmenu_y))
        screen.blit(self.T_description,(self.T_description_x,self.T_description_y))

    def click(self):
        global main_menu_bool,ResetGame,score_data

        mouse_x = pg.mouse.get_pos()[0]
        mouse_y = pg.mouse.get_pos()[1]

        #재시작
        if collide_with_point(mouse_x,mouse_y,self.RestartBox_x,self.RestartBox_y,self.RestartBox_width,self.RestartBox_height):
            ResetGame = True
            self.bool = False
            pg.mixer.stop()
        #메인메뉴
        if collide_with_point(mouse_x,mouse_y,self.MainmenuBox_x,self.MainmenuBox_y,self.MainmenuBox_width,self.MainmenuBox_height):    
            ResetGame = True
            self.bool = False
            pg.mixer.stop()
            main_menu.bool = True

#메뉴       
class Main_Menu:
    def __init__(self):
        gray = (189,189,189)
        self.bool = True
        #배경
        self.bg_img = load_img(assets,'menu_bg.png').convert_alpha()
        #타이틀
            #이미지
        self.title_img = load_img(assets,'menu_title.png').convert_alpha()
        self.title_glow = load_img(assets,'menu_title_glow.png').convert_alpha()
            #이미지 크기
        self.title_width,self.title_height = self.title_img.get_size()

        #최고 점수 (hw:high wave, hs:high score)
        self.hws_space = 100
            #최고 웨이브
        self.hw_text = text_set('hy목각파임b',20,False,True,f"최고 웨이브 >> {score_data[0]}",True,(75, 192, 89))
        self.hw_width,self.hw_height = self.hw_text.get_size()
        self.hw_x = middle(0,screen_width,self.hw_width)-self.hw_width/2-self.hws_space/2
        self.hw_y = 160
            #최고 점수
        self.hs_text = text_set('hy목각파임b',20,False,True,f"최고 점수 >> {score_data[1]}",True,(75, 192, 89))
        self.hs_width,self.hs_height = self.hs_text.get_size()
        self.hs_x = middle(0,screen_width,self.hs_width)+self.hw_width/2+self.hws_space/2
        self.hs_y = 160

        #값 수정 버튼
            #이미지  (위쪽 화살표가 기본 이미지)
        self.modify_img = load_img(assets, 'volume_up.png').convert()
        self.modify_img_flip = pg.transform.flip(self.modify_img,False,True)
            #이미지 크기
        self.modify_img_width,self.modify_img_height = self.modify_img.get_size()


        #볼륨  (v : volume)
            #설명
        T_volume = ['volume','음량설정']
        self.v_text = text_set(gamefont,30,False,False,T_volume[lg],True,gray)
        self.v_text_width,self.v_text_height = self.v_text.get_size()
            #설명과 이미지의 거리
        self.v_space = 30
            #설명 좌표
        self.v_text_x = 150
        self.v_text_y = self.title_height+70
            #이미지 사이의 거리
        self.v_img_space = 90
            #이미지 좌표
        self.v_img_x = self.v_text_x + self.v_text_width + self.v_space
        self.v_img_up_y = middle(self.v_text_y,self.v_text_height,self.modify_img_height) - self.v_img_space/2
        self.v_img_down_y = middle(self.v_text_y,self.v_text_height,self.modify_img_height) + self.v_img_space/2
            #음량 값 텍스트
        self.v_text_num = text_set(gamefont,25,False,False,f"{volume}",True,(255,255,255))
        self.v_text_num_width,self.v_text_num_height = self.v_text_num.get_size()
            #음량 값 좌표
        self.v_text_num_x = middle(self.v_img_x,self.modify_img_width,self.v_text_num_width)
        self.v_text_num_y = middle(self.v_text_y,self.modify_img_height,self.v_text_num_height)


        #무기 변경 방식 설정 (c:change),(s:subject),(b:button),(n:change weapon as numberkey),(r:change weapon as mouse rightclick)
            #설정 설명 텍스트,크기
        T_change = ['How to change weapons','무기 변경 방식']
        T_change_size = [20,30]

        self.c_text_s = text_set(gamefont,T_change_size[lg],False,False,T_change[lg],True,gray)
        self.c_text_s_width,self.c_text_s_height = self.c_text_s.get_size()
            #박스 크기
        self.c_box_width,self.c_box_height = 200,50
            #설정 텍스트(숫자키로 변경),크기
        T_change_button = [('number key','mouse rightclick'),('숫자키로 변경','마우스 우클릭으로 변경')]

        self.c_text_n = text_set(gamefont,15,False,False,T_change_button[lg][0],True,(255,255,255))
        self.c_text_n_width,self.c_text_n_height = self.c_text_n.get_size()
            #설정 텍스트(우클릭으로 변경),크기
        self.c_text_r = text_set(gamefont,15,False,False,T_change_button[lg][1],True,(255,255,255))
        self.c_text_r_width,self.c_text_r_height = self.c_text_r.get_size()
            #개체 사이의 거리
        self.c_space = 30
            #설정 설명 텍스트 좌표
        self.c_text_s_x = 400
        self.c_text_s_y = self.title_height+70
            #박스 y좌표
        self.c_box_nr_y = middle(self.c_text_s_y,self.c_text_s_height,self.c_box_height)
            #박스(숫자키로 변경) 좌표
        self.c_box_n_x = self.c_text_s_x+self.c_text_s_width+self.c_space    
            #박스(우클릭으로 변경) 좌표
        self.c_box_r_x = self.c_box_n_x+self.c_box_width+self.c_space
            #설정 텍스트 y좌표
        self.c_text_nr_y = middle(self.c_box_nr_y,self.c_box_height,self.c_text_n_height)
            #설정 텍스트(숫자키로 변경) 좌표
        self.c_text_n_x = middle(self.c_box_n_x,self.c_box_width,self.c_text_n_width)
            #설정 텍스트(우클릭으로 변경) 좌표
        self.c_text_r_x = middle(self.c_box_r_x,self.c_box_width,self.c_text_r_width)


        #그래픽 설정 버튼 (g:graphic), (s:subject), (l:low detail), (h:high detail)
            #설정 설명 텍스트,크기
        T_graphic = ['quality','그래픽 품질']

        self.g_text_s = text_set(gamefont,30,False,False,T_graphic[lg],True,gray)
        self.g_text_s_width,self.g_text_s_height = self.g_text_s.get_size()
            #박스 크기
        self.g_box_width,self.g_box_height = 170,50
            #설정 텍스트(저품질),크기
        T_graphic_button = [('low','high'),('저품질','고품질')]

        self.g_text_l = text_set(gamefont,20,False,False,T_graphic_button[lg][0],True,(255,255,255))
        self.g_text_l_width,self.g_text_l_height = self.g_text_l.get_size()
            #설정 텍스트(고품질),크기
        self.g_text_h = text_set(gamefont,20,False,False,T_graphic_button[lg][1],True,(255,255,255))
        self.g_text_h_width,self.g_text_h_height = self.g_text_h.get_size()
            #개체 사이의 거리
        self.g_space = 30
            #설정 설명 텍스트 좌표
        self.g_text_s_x = (screen_width-self.g_text_s_width-(self.g_space*2)-(self.g_box_width*2))/2
        self.g_text_s_y = self.title_height+200
            #박스 y좌표
        self.g_box_y = self.g_text_s_y+(self.g_text_s_height-self.g_box_height)/2
            #박스(저품질) 좌표
        self.g_box_l_x = self.g_text_s_x+self.g_text_s_width+self.g_space    
            #박스(고품질) 좌표
        self.g_box_h_x = self.g_box_l_x+self.g_box_width+self.g_space
            #설정 텍스트 y좌표
        self.g_text_y = self.g_box_y+(self.g_box_height-self.g_text_l_height)/2
            #설정 텍스트(저품질) 좌표
        self.g_text_l_x = self.g_box_l_x+(self.g_box_width-self.g_text_l_width)/2
            #설정 텍스트(고품질) 좌표
        self.g_text_h_x = self.g_box_h_x+(self.g_box_width-self.g_text_h_width)/2


        #시작 버튼  (s : start)
            #설명
        T_start = ['start!','시작!']

        self.s_text = text_set(gamefont,40,False,True,T_start[lg],True,(255,255,255))
        self.s_text_width,self.s_text_height = self.s_text.get_size()
            #설명 좌표
        self.s_text_x = (screen_width -self.s_text_width)/2
        self.s_text_y = self.title_height+400
            #텍스트와 차이나는 박스 길이
        self.s_box_distance_x = 200
        self.s_box_distance_y = 30
            #박스 좌표
        self.s_box_x = self.s_text_x - self.s_box_distance_x
        self.s_box_y = self.s_text_y - self.s_box_distance_y
            #박스 길이
        self.s_box_long_x = self.s_box_distance_x*2+self.s_text_width
        self.s_box_long_y = self.s_box_distance_y*2+self.s_text_height

        #아직 완성된 게임이 아닙니다.
        self.not_c_text = text_set(gamefont,20,False,False,'아직 100% 완성된 게임이 아닙니다.(게임 정보를 보려면 클릭)',True,(103, 153, 255))
        self.not_c_width,self.not_c_height = self.not_c_text.get_size()
        self.not_c_x = screen_width-self.not_c_width-10
        self.not_c_y = screen_height+UIbar_height-self.not_c_height-15

    def draw(self):
        global score_data

        #배경
        screen.fill((25,25,25))
        #pg.draw.rect(screen,set_color,(0,0,screen_width,screen_height+UIbar_height),5)

        #타이틀
        screen.blit(self.title_glow,((screen_width-self.title_width)/2,0))
        screen.blit(self.title_img,((screen_width-self.title_width)/2,0))

        #최고 점수
        screen.blit(self.hw_text,(self.hw_x,self.hw_y))
        screen.blit(self.hs_text,(self.hs_x,self.hs_y))

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
        
        #무기 변경 방식 설정
            #설정 설명 텍스트
        screen.blit(self.c_text_s,(self.c_text_s_x,self.c_text_s_y))
            #박스
        pg.draw.rect(screen,(51, 51, 51),(self.c_box_n_x,self.c_box_nr_y,self.c_box_width,self.c_box_height))
        pg.draw.rect(screen,(51, 51, 51),(self.c_box_r_x,self.c_box_nr_y,self.c_box_width,self.c_box_height))
            #설정 텍스트
        screen.blit(self.c_text_n,(self.c_text_n_x,self.c_text_nr_y))
        screen.blit(self.c_text_r,(self.c_text_r_x,self.c_text_nr_y))

        #그래픽 설정
            #설정 설명 텍스트
        screen.blit(self.g_text_s,(self.g_text_s_x,self.g_text_s_y))
            #박스
        pg.draw.rect(screen,(51, 51, 51),(self.g_box_l_x,self.g_box_y,self.g_box_width,self.g_box_height))
        pg.draw.rect(screen,(51, 51, 51),(self.g_box_h_x,self.g_box_y,self.g_box_width,self.g_box_height))
            #설정 텍스트
        screen.blit(self.g_text_l,(self.g_text_l_x,self.g_text_y))
        screen.blit(self.g_text_h,(self.g_text_h_x,self.g_text_y))

        #시작 버튼
            #밝아짐 효과
        if collide_with_point(mouse_x,mouse_y,self.s_box_x,self.s_box_y,self.s_box_long_x,self.s_box_long_y):
            screen.blit(rect_alpha(self.s_box_long_x,self.s_box_long_y,(255, 253, 106),60), (self.s_box_x,self.s_box_y))
            #설명
        screen.blit(self.s_text,(self.s_text_x,self.s_text_y))
            #박스
        pg.draw.rect(screen,(230, 233, 6),(self.s_box_x,self.s_box_y,self.s_box_long_x,self.s_box_long_y),3)    

        #아직 완성된 게임이 아닙니다.
        screen.blit(self.not_c_text,(self.not_c_x,self.not_c_y))

    def click(self):
        global volume,volume_max,change_weapon_type,Graphic,score_data
        mouse_x = pg.mouse.get_pos()[0]
        mouse_y = pg.mouse.get_pos()[1]

        #메인 메뉴
            #음량 설정
        if collide_with_point(mouse_x,mouse_y,self.v_img_x,self.v_img_up_y,self.modify_img_width,self.modify_img_height):
            if volume < volume_max:
                volume += 1
                Sound(assets,'volume_setting.wav',set_sound(0.7,volume,volume_max))

        elif collide_with_point(mouse_x,mouse_y,self.v_img_x,self.v_img_down_y,self.modify_img_width,self.modify_img_height):
            if volume > 0:
                volume -= 1
                Sound(assets,'volume_setting.wav',set_sound(0.7,volume,volume_max))

            #무기 변경 방식 설정
                #숫자키로 변경
        if collide_with_point(mouse_x,mouse_y,self.c_box_n_x,self.c_box_nr_y,self.c_box_width,self.c_box_height):
            change_weapon_type = 0
            Sound(assets,'click_button.wav',set_sound(0.7,volume,volume_max))
                #마우스 우클릭으로 변경
        elif collide_with_point(mouse_x,mouse_y,self.c_box_r_x,self.c_box_nr_y,self.c_box_width,self.c_box_height):
            change_weapon_type = 1
            Sound(assets,'click_button.wav',set_sound(0.7,volume,volume_max))

            #그래픽 설정
                #저품질
        if collide_with_point(mouse_x,mouse_y,self.g_box_l_x,self.g_box_y,self.g_box_width,self.g_box_height):
            Graphic = 0
            Sound(assets,'click_button.wav',set_sound(0.7,volume,volume_max))
                #고품질
        elif collide_with_point(mouse_x,mouse_y,self.g_box_h_x,self.g_box_y,self.g_box_width,self.g_box_height):
            Graphic = 1
            Sound(assets,'click_button.wav',set_sound(0.7,volume,volume_max))

            #시작 버튼
        if collide_with_point(mouse_x,mouse_y,self.s_box_x,self.s_box_y,self.s_box_long_x,self.s_box_long_y):
            Sound(assets,'game_start.wav',set_sound(0.5,volume,volume_max))
            self.bool = False

            #아직 완성된 게임이 아닙니다.
        if collide_with_point(mouse_x,mouse_y,self.not_c_x,self.not_c_y,self.not_c_width,self.not_c_height):
            webbrowser.open('https://www.instagram.com/jiyong._.06/')

    def work(self):
        global score_data

        self.draw()

        f_s = open("score data.txt",'rb')
        score_data = list(pickle.load(f_s))
        f_s.close()

        self.hw_text = text_set('hy목각파임b',20,False,True,f"최고 웨이브 >> {score_data[0]}",True,(75, 192, 89))
        self.hs_text = text_set('hy목각파임b',20,False,True,f"최고 점수 >> {score_data[1]}",True,(75, 192, 89))

        #음량 값
        self.v_text_num = text_set(gamefont,25,False,False,f"{volume}",True,(255,255,255))

        #무기 변경 방식에 따른 박스 테두리 유무
        '''if change_weapon_type == 0:
             pg.draw.rect(screen,(255,255,255),(self.c_box_n_x,self.c_box_nr_y,self.c_box_width,self.c_box_height),3)
        elif change_weapon_type == 1:
             pg.draw.rect(screen,(255,255,255),(self.c_box_r_x,self.c_box_nr_y,self.c_box_width,self.c_box_height),3)'''

        #품질에 따른 테두리 유무
        if Graphic == 0:
             pg.draw.rect(screen,(255,255,255),(self.g_box_l_x,self.g_box_y,self.g_box_width,self.g_box_height),3)
        elif Graphic == 1:
             pg.draw.rect(screen,(255,255,255),(self.g_box_h_x,self.g_box_y,self.g_box_width,self.g_box_height),3)

def ClassValueSetting() -> None: #차트 정리용
    """
    클래스 변수 선언하는 곳
                    V V V
    """

#클래스 설정   
player = Player()
atteck_dir = Atteck_dir()
target_mouse = Target_mouse()
bullet = Bullet()
knife = Knife()
zombie_melee = Zombie_melee()
zombie_shoot = Zombie_shoot()
bomb = Bomb()
upgrade = Upgrade()
main_menu = Main_Menu()
zombie_blood = ZombieBlood()
player_hurt = PlayerHurt()
particle = Particle()
blood_splash = BloodSplash()
bomb_splash = BombSplash()
lastzombie_effect = LastZombie_Effect()
cardselect_effect = CardSelect_Effect()
ph_ui = PlayerHealth_UI()
kc_ui = KnifeCooltime_UI()
ui = UI()
pause = Pause()
gameover = GameOver()
wave = Wave()

def MainLoopSetting() -> None: #차트 정리용
    """
    메인루프 설정 하는 곳
                    V V V
    """

if __name__ == '__main__':
    while not done:
        screen.fill(background_color)
        fps_proportion = 60/FPS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                #움직임
                if event.key == pg.K_a:
                    press_x_list.append(-player.speed)
                    press_left = True
                if event.key == pg.K_d:
                    press_x_list.append(player.speed)
                    press_right = True 
                if event.key == pg.K_w:
                    press_y_list.append(-player.speed)
                    press_up = True
                if event.key == pg.K_s:
                    press_y_list.append(player.speed)
                    press_down = True
                
                #숫자키로 무기변경
                if event.key == pg.K_1:  #총
                    weapon = 0
                    special_weapon = False  #칼
                if event.key == pg.K_2:
                    weapon = 1
                    special_weapon = False     
                if event.key == pg.K_g:
                    special_weapon = True

                if event.key == pg.K_ESCAPE:
                    if not main_menu.bool:
                        pause.bool = True if pause.bool==False else False
                
            if event.type == pg.KEYUP:
                #움직임
                if event.key == pg.K_a:
                    press_left = False
                    if press_right == True:
                        press_x_list.append(player.speed)
                if event.key == pg.K_d:
                    press_right = False
                    if press_left == True:
                        press_x_list.append(-player.speed)
                if event.key == pg.K_w:
                    press_up = False
                    if press_down == True:
                        press_y_list.append(player.speed)
                if event.key == pg.K_s:
                    press_down = False
                    if press_up == True:
                        press_y_list.append(-player.speed)
                        
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == pg.BUTTON_LEFT:
                    if main_menu.bool:
                        main_menu.click()
                    if pause.bool == True:
                        pause.click()
                    if Upgrading:
                        upgrade.select_process()
                    if gameover.bool == True:
                        gameover.click()

                #마우스 우클릭으로 무기변경
                if event.button == pg.BUTTON_RIGHT:
                    if not main_menu.bool and Upgrading == False:
                        if special_weapon == True:
                            special_weapon = False
                        else:
                            weapon = 0 if weapon == 1 else 1 #toggle            

        if pg.mouse.get_pressed()[0] == True:
            click_left = True
        if pg.mouse.get_pressed()[0] == False:
            click_left = False
            special_weapon_click = 1
        if pg.mouse.get_pressed()[2] == True:
            click_right = True
        if pg.mouse.get_pressed()[2] == False:
            click_right = False    

        mouse_x, mouse_y = pg.mouse.get_pos()

        if not main_menu.bool: 
            if not player.health <= 0:
                Game()
                Crash_Zombie(zombie_melee,zombie_shoot)
                gameover.bool = False
                gameover.gameover_sound_play = 0
            else:   
                gameover.bool = True
            if gameover.bool == True:     
                gameover.work()        
            if pause.bool == False:               
                pg.mixer.unpause()
                wave.work()   
                upgrade.work()
            else:
                pg.mixer.pause()
            
        else: #메인 메뉴
            main_menu.work()

        if ResetGame:
            #점수
            score = 0
            #무기
            weapon = 1
            special_weapon = False
            #총
            bullet.list.clear()
            #칼
            knife_atteck_term_startval = 120
            knife_atteck_term = knife_atteck_term_startval
            knife_atteck_timelong = 10
            knife_cooltime = 0
            knife_increase_size = 0
            knife.atteck = 0
            #좀비
            zombie_melee_spawntime = 90
            zombie_shoot_spawntime = 160
            zombie_melee.list.clear()
            zombie_shoot.list.clear()
            zombie_shoot.bullet.clear()
            #스폰 수
            wave.zm_spawn = 3
            wave.zs_spawn = 0
            wave.zm_spawn_startval = wave.zm_spawn
            wave.zs_spawn_startval = wave.zs_spawn
            wave.zm_spawncount = wave.zm_spawn
            wave.zs_spawncount = wave.zs_spawn
            #남은 좀비 수
            wave.Z_left = 0
            #웨이브
            wave_count = 0
            wave.time = 0
            wave.killzombie = 0
            wave.fontalpha = 255
            wave.WaitForCard = 60
            wave.fontdraw = False
            #수류탄
            special_weapon_click = 1
            special_weapon_availabletime = 0
            special_weapon_have = 3
            #최대체력
            player.max_health = 5
            #플레이어
            player.health = player.max_health
            player.speed = player.speed_init
            #플레이어 맞음 효과
            player.ph_e_transparent
            #피 효과
            blood_splash.object.clear()
            zombie_blood.list.clear()
            player_hurt.ph_e_transparent = 0
            #업그레이드 항목
            upgrade.firegun_level = 0
            upgrade.knife_size_level = 0
            upgrade.knife_cooltime_level = 0
            upgrade.health_level = 0
            upgrade.speed_level = 0
            upgrade.select_card = -1
            
            ResetGame = False
        
        pg.display.flip()
        clock.tick(60)
    pg.quit()
