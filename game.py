from turtle import up
import pygame as pg, os, time, random, math, sys

pg.init()

#기본 세팅
screen_width = 1200
screen_height = 700
UIbar_height = 150
screen = pg.display.set_mode([screen_width,screen_height+UIbar_height])
pg.display.set_caption("Hell Walker")

black = (0,0,0)

clock = pg.time.Clock()
done = False
a= 0
def file_path(relative_path):  #파일경로
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#전역 변수
    #파일
assets = file_path('jamsil_surviver/assets')
    #클릭
press_x_list = []
press_y_list = []
press_left,press_right,press_up,press_down = (False,False,False,False)
click_left, click_right = False,False
    #무기
weapon = 1
special_weapon = False
    #총
firegun_time = 60
    #칼
knife_atteck_term = 120
knife_atteck_timelong = 10
knife_cooltime = 0
knife_increase_size = 0
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
    #스폰 수
zm_spawn = 4
zs_spawn = 1
zm_spawn_startval = zm_spawn
zs_spawn_startval = zs_spawn
zm_spawncount = zm_spawn
zs_spawncount = zs_spawn
    #남은 좀비 수
Z_left = 0
    #웨이브
wave = 0
wave_time = 0
wave_killzombie = 0
wave_fontalpha = 200
between_wave = 60
wave_fontdraw = False
    #수류탄
special_weapon_click = 1
special_weapon_availabletime = 0
special_weapon_have = 3
    #최대체력
max_health = 5.0
    #업그레이드
DoingUpgrade = False
card_num = random.randint(2,3)

#플레이어
class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        global max_health
        self.img = pg.image.load(os.path.join(assets,'player.png'))
        self.rect = self.img.get_rect()
        self.width,self.height = self.img.get_size()
        self.x = screen_width/2-self.width/2
        self.y = screen_height/2-self.height/2+UIbar_height
        self.health = max_health
        self.speed = 2.7
        self.sprites = []
        #히트박스
        self.hitbox = pg.image.load(os.path.join(assets,'player_hitbox.png'))
        self.h_rect = self.hitbox.get_rect()
        self.h_width,self.h_height = self.hitbox.get_size()

    def move(self):
        if press_left == False and press_right == False:
            press_x_list.clear()
        if len(press_x_list) > 2:
            del press_x_list[0]
        try:
            self.x += press_x_list[len(press_x_list)-1]
        except Exception:
            pass
        if press_up == False and press_down == False:
            press_y_list.clear()
        if len(press_y_list) > 2:
            del press_y_list[0]
        try:
            self.y += press_y_list[len(press_y_list)-1]
        except Exception:
            pass
        #벽에 닿았을 때
        if self.x < 0:self.x += self.speed
        if self.x > screen_width-self.width:self.x -= self.speed
        if self.y < UIbar_height:self.y += self.speed
        if self.y > screen_height+UIbar_height-self.height:self.y -= self.speed  
    def draw(self):
        screen.blit(self.img,[self.x,self.y])

    def update(self):
        self.centerx = self.x + self.width/2
        self.centery = self.y + self.height/2
        self.rect.topleft = (self.x,self.y)
        #히트박스
        self.h_x = self.x + (self.width-self.h_width)/2
        self.h_y = self.y + (self.height-self.h_height)/2
        self.h_rect.topleft = (self.centerx,self.centery)
        #screen.blit(self.hitbox,[self.h_x,self.h_y])

        self.move()
       
#공격 방향 표시
class Atteck_dir():
    def __init__(self):
        self.img = []
        self.img.append([pg.image.load(os.path.join(assets,'atteck_dir_gun.png')),0,0,(34,177,76)])
        self.img.append([pg.image.load(os.path.join(assets,'atteck_dir_knife.png')),0,0,(70,235,125)])
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
class Target_mouse():
    def __init__(self):
        self.img = pg.image.load(os.path.join(assets,'target.png'))
        self.width, self.height = self.img.get_size()
        self.img.set_colorkey((0,0,0))
    def update(self):
        if special_weapon == True:
            pg.mouse.set_visible(False)
            screen.blit(self.img, [mouse_x-self.width/2,mouse_y-self.height/2])            
        else:
            pg.mouse.set_visible(True)
#총알
class Bullet():
    def __init__(self):
        self.img = pg.image.load(os.path.join(assets,'bullet.png'))
        self.width,self.height = self.img.get_size()
        self.rect = self.img.get_rect()
        self.speed = 10
        self.speed_increase = 0.13
        self.fire_term = firegun_time
        self.list = []
    def atteck(self): 
        global score
        for B in self.list:
            self.rect.topleft = (B[0],B[1])
            for Zm in zombie_melee.list:  #zombie_melee
                zombie_melee.rect.topleft = (Zm[0],Zm[1])
                if zombie_melee.rect.colliderect(self.rect):
                    Zm[5] -= 1
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

    def sound(self):
        if self.fire_term == 0 and weapon == 0 and special_weapon == False:
            gun_sound = pg.mixer.Sound(os.path.join(assets,'gun_sound.wav'))
            pg.mixer.Sound.set_volume(gun_sound, 0.1)
            gun_sound.play()

    def update(self):
        self.atteck()
        self.x = atteck_dir.x
        self.y = atteck_dir.y
        if self.fire_term == 0 and weapon == 0 and special_weapon == False:
            self.angle = math.atan2(mouse_y-player.centery, mouse_x-player.centerx)
            self.degree = math.degrees(self.angle)*-1
            self.dx = 0 #math.cos(self.angle)*self.speed
            self.dy = 0 #math.sin(self.angle)*self.speed
            self.list.append([self.x-self.width/2, self.y-self.height/2, self.dx, self.dy, 
                                    self.angle, self.speed])
            self.fire_term = firegun_time
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
            self.fire_term = firegun_time
    
#칼
class Knife():
    def __init__(self):
        global knife_atteck_term, knife_atteck_timelong
        self.img = pg.image.load(os.path.join(assets,'knife_hitbox.png'))
        self.width, self.height = self.img.get_size()
        self.atteck_term = 0
        self.cooltime = 0
        self.atteck_timelong = knife_atteck_timelong
        self.atteck = False

    def Atteck(self):
        global score,knife_increase_size
        self.img = pg.transform.scale(self.img,\
                (self.width+knife_increase_size,self.height+knife_increase_size))
        #공격, 히트박스 위치 설정
        global knife_atteck_term, knife_atteck_timelong
        if self.atteck_term > 0:
            self.atteck_term -= 1

        if click_left == True and self.atteck_term == 0 and weapon == 1 and special_weapon == False:
            self.atteck = True
            self.atteck_timelong = knife_atteck_timelong
            self.atteck_term = knife_atteck_term
            
        if self.atteck == True and self.atteck_timelong > 0:
            self.atteck_timelong -= 1
            self.angle = math.atan2(mouse_y-player.centery, mouse_x-player.centerx)
            self.x = (50+knife_increase_size)*math.cos(self.angle) \
                                                + player.centerx -(self.width+knife_increase_size)/2
            self.y = (50+knife_increase_size)*math.sin(self.angle) \
                                                + player.centery -(self.height+knife_increase_size)/2        
        #데미지 줌
            self.rect = self.img.get_rect()
            self.rect.topleft = (self.x,self.y)
            
            for Zmk in zombie_melee.list:  #zombie_melee
                Zmk_rect = zombie_melee.img.get_rect()
                Zmk_rect.topleft = (Zmk[0], Zmk[1])
                if self.rect.colliderect(Zmk_rect):
                    Zmk[5] -= 2
                    score += 100

            for Zs in zombie_shoot.list:   #zombie_shoot
                Zs_rect = zombie_shoot.img.get_rect()
                Zs_rect.topleft = (Zs[0], Zs[1])
                if self.rect.colliderect(Zs_rect):
                    Zs[5] -= 2
                    score += 100
        #히트박스 위치 초기화
        if self.atteck_timelong == 0:
            self.x, self.y = None, None

    def draw(self):
        if self.atteck == True and self.atteck_timelong > 0:
            screen.blit(self.img,(self.x, self.y))

    def update(self):
        self.Atteck()   

#특수무기(수류탄)-------------------------------------------------------------------------------------------------
class Bomb():
    def __init__(self):
        self.img = pg.image.load(os.path.join(assets,'bomb.png'))
        self.img.set_colorkey((255,255,255))     
        self.width, self.height = self.img.get_size()   
        self.f_img = pg.image.load(os.path.join(assets,'fallingpos.png'))  
        self.f_img.set_colorkey((0,0,0)) 
        self.fallingpos = []
        self.bomblist = []
        self.explode = []
        self.explode_draw = []
        #히트박스
        self.h_img = pg.image.load(os.path.join(assets,'explode_hitbox.png'))
        self.h_img.set_colorkey((255,255,255))
        self.h_width, self.h_height = self.h_img.get_size()   
        self.rect = self.h_img.get_rect()
        #폭발 모션
        self.e_img = []
        self.e_img.append(pg.image.load(os.path.join(assets,'explode_1.png')))
        self.e_img.append(pg.image.load(os.path.join(assets,'explode_2.png')))
        self.e_img.append(pg.image.load(os.path.join(assets,'explode_3.png')))
        self.e_img.append(pg.image.load(os.path.join(assets,'explode_4.png')))
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
                and special_weapon_have > 0:
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
                self.fallingpos.remove(f)  

                self.damage(zombie_melee,zombie_shoot)

                self.explode.clear()
        
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
            screen.blit(self.e_img[ed[5]],(ed[0],ed[1]))
            ed[2] -= 1
            ed[3] -= 1        
    
    def damage(self,zm,zs):
        global Z_left, score  
        for e in self.explode:
            self.rect.topleft = e[0],e[1]
            for i in range(0,4):
                for m in zm.list:
                    zm.rect.topleft = m[0],m[1]
                    if zm.rect.colliderect(self.rect):
                        zm.list.remove(m)
                        Z_left -= 1   
                        score += 100
            for i in range(0,4):
                for s in zs.list:
                    zs.rect.topleft = s[0],s[1]
                    if zs.rect.colliderect(self.rect):
                        zs.list.remove(s)
                        Z_left -= 1 
                        score += 100 
        
    def update(self):
        self.falling()

#좀비(근접)
class Zombie_melee():
    def __init__(self):
        self.img = pg.image.load(os.path.join(assets,'zombie_1.png'))
        self.img_Lflip = pg.transform.flip(self.img,True,False)
        self.width, self.height = self.img.get_size()
        self.rect = self.img.get_rect()
        self.speed = 2
        self.health = 2
        self.crash_player_time = 0
        self.list = []
        self.spawntime = zombie_melee_spawntime
        self.x , self.y = 0,0
        #크래시박스
        self.crashbox = pg.image.load(os.path.join(assets,'zombie_1_crashbox.png'))
        self.c_rect = self.crashbox.get_rect()
        self.c_width,self.h_height = self.crashbox.get_size()

    def spawn(self):
        global zm_spawncount,zm_spawn
        if zm_spawncount//1 > 0:
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
                                    self.crash_player_time,random.choice([True,False])])
                                # x:[0] y:[1] dx:[2] dy[3] angle[4] health[5] crash_player_time[6]
                                    #Lflip?[7]
                self.spawntime = 1000//zm_spawn
                zm_spawncount -= 1
                
                #만약 무한모드라면
                '''zm_count += 1'''
        self.spawntime -= 1

    def Atteck_Die(self):
        global score, wave_killzombie,Z_left
        #atteck
        for Zmp in self.list:
            Zmp_rect = self.img.get_rect()
            Zmp_rect.topleft = (Zmp[0],Zmp[1])
            if Zmp_rect.colliderect(player.h_rect):
                if Zmp[6] == 0:
                    player.health -= 1
                    Zmp[6] = zombie_melee_crash_player_time                
            if Zmp[6] != 0:
                Zmp[6] -= 1
            #die
            if Zmp[5] <= 0:
                self.list.remove(Zmp)
                score += 100
                wave_killzombie += 1
                Z_left -= 1
    def move(self):
        for Zm in self.list:
            #move
            Zm[0] += Zm[2] 
            Zm[1] += Zm[3]
            Zm[4] = math.atan2(player.y-Zm[1],player.x-Zm[0])
            Zm[2] = math.cos(Zm[4])*self.speed
            Zm[3] = math.sin(Zm[4])*self.speed           
    
    def draw(self):
        for Zm in self.list:
            if Zm[7] == True:
                screen.blit(self.img_Lflip,(Zm[0],Zm[1]))
            else:
                screen.blit(self.img,(Zm[0],Zm[1]))

    def update(self):
        self.spawn()
        self.Atteck_Die() 
        self.move() 

        self.c_x = self.x + (self.width-self.c_width)/2
        self.c_y = self.y + (self.height-self.h_height)/2
        self.c_rect.topleft = (self.c_x,self.c_y)
        #screen.blit(self.hitbox,[self.h_x,self.h_y])
        
#좀비(원거리)
class Zombie_shoot():
    def __init__(self):
        #zombie
        self.img = pg.image.load(os.path.join(assets,'zombie_2.png'))
        self.width, self.height = self.img.get_size()
        self.rect = self.img.get_rect()
        self.speed = 2
        self.health = 1
        self.list = []
        self.bullet = []
        self.crash = False
        self.spawntime = zombie_shoot_spawntime
        self.x, self.y = 0,0
        #bullet
        self.b_img = pg.image.load(os.path.join(assets,'zombie_bullet.png'))
        self.b_rect = self.b_img.get_rect()
        self.b_width, self.b_height = self.b_img.get_size()
        self.b_speed = 7
        self.shooting_time = zombie_shoot_shooting_time

    def spawn(self):
        global zs_spawncount,zs_spawn
        if zs_spawncount//1 >0:
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
                self.spawntime = 1000//zs_spawn
                zs_spawncount -= 1                
                #만약 무한모드라면
                '''zs_count += 1'''
        self.spawntime -= 1

    def Basic(self):
        global score, wave_killzombie,Z_left
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
                self.list.remove(Zs)
                score += 100
                wave_killzombie += 1
                Z_left -= 1
    
    def Bullet(self):
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
                player.health -= 1
                self.bullet.remove(Zb)
        
    def draw(self):
        for Zs in self.list:
            screen.blit(self.img,(Zs[0],Zs[1]))

        for Zb in self.bullet:
            screen.blit(self.b_img,(Zb[0],Zb[1]))
            
    def update(self):
        self.spawn()
        self.Basic()
        self.Bullet()

def Crash_Zombie(zm,zs):
        a_index, b_index = 0,0
        for Zm1 in zm.list:
            for Zm2 in zm.list:
                if a_index < b_index:
                    Zm1_rect,Zm2_rect = zm.crashbox.get_rect(), zm.crashbox.get_rect()
                    Zm1_rect.topleft,Zm2_rect.topleft = (Zm1[0],Zm1[1]), (Zm2[0],Zm2[1])
                    if Zm1_rect.colliderect(Zm2_rect):
                        Zm1_angle = math.atan2(Zm1[1]-Zm2[1],Zm1[0]-Zm1[0]) #math.cos또는sin(Zm1_angle)*zm.speed
                        if math.dist((Zm1[0],Zm1[1]),(player.x , player.y)) \
                            < math.dist((Zm2[0],Zm2[1]),(player.x , player.y)):
                            Zm2[2] = -math.cos(Zm1_angle)*zm.speed
                            Zm2[3] = -math.sin(Zm1_angle)*zm.speed                  
                        else: 
                            Zm1[2]= math.cos(Zm1_angle)*zm.speed
                            Zm1[3]= math.cos(Zm1_angle)*zm.speed
                b_index += 1
            b_index = 0
            a_index += 1 
        a_index, b_index = 0,0  
        for Zs1 in zs.list:
            for Zs2 in zs.list:
                if a_index < b_index:
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
def Timegoing():
    global Time,score
    if Time <= 0:
            score += 10
            Time = 60
    Time -= 1

def Click(u):
    if click_left:
        u.pressing_mouse = u.pressing_mouse_initialval
    else:
        if u.pressing_mouse > 0:
            u.pressing_mouse -= 1

    #게임
def Game():
    global wave_time,DoingUpgrade
    if DoingUpgrade == False:
        #시간
        Timegoing()
        #업데이트
        player.update()
        atteck_dir.update()
        target_mouse.update()
        bullet.update() 
        knife.update()
        zombie_melee.update()
        zombie_shoot.update()
        bomb.update()
        
    #그리기
    bullet.draw()
    atteck_dir.draw()
    zombie_shoot.draw()
    player.draw()
    zombie_melee.draw()
    knife.draw()
    bomb.draw()
    
    #사운드
    bullet.sound()
    #클릭
    Click(upgrade)

    #UI바
    pg.draw.rect(screen,(0,0,0),[0,0,screen_width,UIbar_height],0)
    pg.draw.rect(screen,(255,80,199),[0,0,screen_width,UIbar_height],3)
    #체력
    font_health = pg.font.SysFont('한컴산뜻돋움', 50, False, False)
    text_health = font_health.render(f"체력 : {player.health}/{max_health}", True, (255,72,199))
    screen.blit(text_health, (screen_width/2-(text_health.get_rect())[2]/2,50))
    #칼 쿨타임
    font_k_cooltime = pg.font.SysFont('한컴산뜻돋움', 30, False, True)
    text_k_cooltime = font_k_cooltime.render(f"칼 쿨타임 : {knife.atteck_term/60:0.2f}", True, (243,97,220))
    screen.blit(text_k_cooltime, (800,30))
    #수류탄 개수
    font_bomb = pg.font.SysFont('한컴산뜻돋움', 30, False, True)
    text_bomb = font_bomb.render(f"수류탄 개수 : {special_weapon_have}", True, (255,97,166))
    screen.blit(text_bomb, (800,75))
    #웨이브
    font_score = pg.font.SysFont('한컴산뜻돋움', 30, False, True)
    text_score = font_score.render(f"wave : {wave}", True, (255,36,163))
    screen.blit(text_score, (220,30))
    #점수
    font_score = pg.font.SysFont('한컴산뜻돋움', 30, False, True)
    text_score = font_score.render(f"점수 : {score}", True, (110,227,247))
    screen.blit(text_score, (220,80))
    #웨이브 시간
    font_wavetime = pg.font.SysFont('한컴산뜻돋움', 20, False, False)
    text_wavetime = font_wavetime.render(f"웨이브 시간 {wave_time//60}", True, (255,255,255))
    screen.blit(text_wavetime, (screen_width/2-(text_wavetime.get_rect())[2]/2,20))

def Wave():
    global wave, wave_time, wave_killzombie, wave_fontalpha, zm_spawn, zs_spawn, zm_spawncount, zs_spawncount\
        ,zombie_melee_spawntime, zombie_shoot_spawntime, Z_left,zombie_melee_spawntime,zombie_shoot_spawntime\
        , zm_spawn_startval, zs_spawn_startval, between_wave, wave_fontdraw, card_num

    if wave_time == 0 or Z_left == 0:
        if between_wave > 0:
            between_wave -= 1
        else:
            if DoingUpgrade == False:
                wave += 1
                between_wave = 60
                wave_fontdraw = True
                wave_time = 3600
                wave_fontalpha = 230
                wave_killzombie = 0

                zm_spawn = zm_spawn_startval + 1.3*wave
                zs_spawn = zs_spawn_startval + 0.55*wave
                zm_spawncount = zm_spawn
                zs_spawncount = zs_spawn

                Z_left += zm_spawn//1 + zs_spawn//1

                zombie_melee.spawntime = 1000//zm_spawn
                zombie_shoot.spawntime = 1000//zs_spawn

                card_num = random.randint(2,3)
                upgrade.select()

                #사운드
                wave_change_sound = pg.mixer.Sound(os.path.join(assets,'wave change.wav'))
                pg.mixer.Sound.set_volume(wave_change_sound, 0.5)
                wave_change_sound.play()
    if wave_fontalpha > 0 and wave_fontdraw:
        wave_fontalpha -= 2.3

        #웨이브 알림
        font_wave = pg.font.SysFont('Times new Roman',150, True, False)
        textsurface = font_wave.render(f"WAVE {wave}", True, (255,80,199))
        surface = pg.Surface((textsurface.get_rect()[2], textsurface.get_rect()[3]))
        surface.fill(black)
        surface.blit(textsurface, pg.Rect(0, 0, 10, 10))
        surface.set_alpha(wave_fontalpha)
        screen.blit(surface,(screen_width/2-(surface.get_rect())[2]/2,screen_height/2-(surface.get_rect())[1]/2))
    else:
        wave_fontdraw = False

    if between_wave > 0 and wave_time > 0:
        wave_time -= 1

class Upgrade():
    def __init__(self):
        self.width,self.height = 150,300
        self.middlecard_x = screen_width/2-self.width/2
        self.y = (UIbar_height+screen_height-self.height)/2
        self.space = 70
        self.pos = []
        self.card = []
        self.select_card = 0
        self.pressing_mouse_initialval = 2
        self.pressing_mouse = 0 #눌렀을 때 초기값 됨, 뗐을 때 0까지 1틱당 1씩 줄어듬
        self.add_card = False
        #업그레이드 리스트
        self.upgrade_list = []
        self.upgrade_list.append("공격 속도 증가") #0
        self.upgrade_list.append("칼 크기 증가") #1
        self.upgrade_list.append("칼 쿨타임 감소") #2
        self.upgrade_list.append("수류탄 2+") #3
        self.upgrade_list.append("힐(최대체력의 50%)") #4
        self.upgrade_list.append("힐(100%)") #5
        self.upgrade_list.append("최대 체력 증가") #6
        self.upgrade_list.append("이동속도 증가") #7

    def random(self,card_num):
        while not len(self.card) == card_num:
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

    def select_process(self,card_num):
        global between_wave,DoingUpgrade,special_weapon
       
        if between_wave <= 0:
            DoingUpgrade = True

        if DoingUpgrade == True:
            pg.mouse.set_visible(True)          

            if card_num == 2:
                self.pos.append([screen_width/2-self.width-self.space/2,self.y])
                self.pos.append([screen_width/2+self.space/2,self.y])

                if not click_left:
                    if self.pressing_mouse:  #Game -> Click
                        for c in self.pos:        
                            if c[0] <= mouse_x <= c[0]+self.width and c[1] <= mouse_y <= c[1]+self.height:
                                DoingUpgrade = False
                                self.select_card = self.card[self.pos.index(c)]
                                knife.cooltime = 0
                                self.pos.clear()    
                                self.card.clear()   

            if card_num == 3:        
                self.pos.append([self.middlecard_x-self.width-self.space,self.y])
                self.pos.append([self.middlecard_x,self.y])
                self.pos.append([self.middlecard_x+self.width+self.space,self.y])
                
                if not click_left:
                    if self.pressing_mouse:  #Game -> Click
                        for c in self.pos:        
                            if c[0] <= mouse_x <= c[0]+self.width and c[1] <= mouse_y <= c[1]+self.height:
                                DoingUpgrade = False
                                self.select_card = self.card[self.pos.index(c)]
                                knife.cooltime = 0
                                self.pos.clear()    
                                self.card.clear()

    def select(self):
        global firegun_time,knife_atteck_term,special_weapon_have,max_health,knife_increase_size
        sc = self.select_card
        if sc == 0:
            firegun_time -= 2
        elif sc == 1:
            knife_increase_size += 5
        elif sc == 2:
            knife_atteck_term -= 3
        elif sc == 3:
            special_weapon_have += 2
        elif sc == 4:
            player.health += max_health//2
            if player.health > max_health:
                player.health = max_health
        elif sc == 5:
            player.health = max_health
        elif sc == 6:
            max_health += 0.5
        elif sc == 7:
            player.speed += 0.3

    def draw(self):
        for c in self.pos: 
            pg.draw.rect(screen,(0,0,0),[c[0],c[1],self.width,self.height],0)   
            pg.draw.rect(screen,(255,80,199),[c[0],c[1],self.width,self.height],3)
           
        for cd in self.card:
            cd_index = self.card.index(cd)
            font_ug_des = pg.font.SysFont('한컴산뜻돋움', 15, False, False)
            text_ug_des = font_ug_des.render(f"{self.upgrade_list[self.card[cd_index]]}", True, (255,255,255))
            try:
                screen.blit(text_ug_des, (self.pos[cd_index][0]+(self.width-text_ug_des.get_size()[0])/2\
                                            ,self.pos[cd_index][1]+(self.height-text_ug_des.get_size()[1])/2)) 
            except:pass
    def update(self,card_num):
        self.random(card_num)
        self.select_process(card_num)
        #self.select()
        self.draw()

def GameOver():
    global special_weapon
    if player.health <= 0:
        screen.fill(black)

        font_totalwave = pg.font.SysFont('휴먼매직체', 70, False, False)
        text_totalwave = font_totalwave.render(f"wave : {wave}", True, (255,72,199))
        screen.blit(text_totalwave, (screen_width/2-(text_totalwave.get_rect())[2]/2,\
            screen_height/2-(text_totalwave.get_rect())[3]/2+UIbar_height/2-70))

        font_score = pg.font.SysFont('휴먼매직체', 50, False, True)
        text_score = font_score.render(f"점수 : {score}", True, (255,255,255))
        screen.blit(text_score, (screen_width/2-(text_score.get_rect())[2]/2,\
            screen_height/2-(text_score.get_rect())[3]/2+UIbar_height/2+30))

        pg.mouse.set_visible(True)

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

while not done:
    screen.fill(black)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
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
            
            if event.key == pg.K_1:  #총
                weapon = 0
                special_weapon = False  #칼
            if event.key == pg.K_2:
                weapon = 1
                special_weapon = False     
            if event.key == pg.K_g:
                special_weapon = True
            
        if event.type == pg.KEYUP:
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

    Wave()
    if not player.health <= 0:
        Game() 
    upgrade.update(card_num)
    GameOver()
    Crash_Zombie(zombie_melee,zombie_shoot)
    
    pg.display.flip()
    clock.tick(60)
pg.quit()
