import pygame as pg, os, time, random, math, sys

pg.init()

#기본 세팅
screen_width = 1200
screen_height = 700
screen = pg.display.set_mode([screen_width,screen_height])
pg.display.set_caption("Hell Walker")

black = (0,0,0)

clock = pg.time.Clock()
done = False

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
    #마우스 좌표
mouse_x, mouse_y = pg.mouse.get_pos()
    #무기
weapon = 1
special_weapon = False
    #총
firegun_time = 10
    #칼
knife_atteck_term = 120
knife_atteck_timelong = 10
    #좀비(근접)
zombie_melee_spawntime = 20
zombie_melee_crash_player_time = 60
crash_Zm_time = 20 # while문에서 실행

#플레이어
class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.img = pg.image.load(os.path.join(assets,'player.png'))
        self.rect = self.img.get_rect()
        self.width,self.height = self.img.get_size()
        self.x = screen_width/2-self.width/2
        self.y = screen_height/2-self.height/2 
        self.health = 10
        self.speed = 3
        self.sprites = []

    def update(self):
        self.centerx = self.x + self.width/2
        self.centery = self.y + self.height/2
        self.rect.topleft = (self.centerx,self.centery)
        screen.blit(self.img,[self.x,self.y])
        if self.health <= 0: #사망
            print("die")

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
        if self.y < 0:self.y += self.speed
        if self.y > screen_height-self.height:self.y -= self.speed
#공격 방향 표시
class Atteck_dir():
    def __init__(self):
        self.img = []
        self.img.append(pg.image.load(os.path.join(assets,'atteck_dir_gun.png')))
        self.img.append(pg.image.load(os.path.join(assets,'atteck_dir_knife.png')))
        self.width, self.height = 30,30
    def update(self):
        self.img[weapon].set_colorkey((0,0,0))
        self.angle = math.atan2(mouse_y-player.centery, mouse_x-player.centerx)
        self.degree = math.degrees(self.angle)*-1
        self.x = 50*math.cos(self.angle) + player.centerx
        self.y = 50*math.sin(self.angle) + player.centery
        self.result = pg.transform.rotate(self.img[weapon],self.degree)
        if special_weapon == False:
            screen.blit(self.result,(self.x-self.width/2,self.y-self.height/2))
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
        for Zm in zombie_melee.list:  #zombie_melee
            zombie_melee.rect.topleft = (Zm[0],Zm[1])
            for B in self.list:
                self.rect.topleft = (B[0],B[1])
                if zombie_melee.rect.colliderect(self.rect):
                    Zm[5] -= 1
                    self.list.remove(B)
            
    def update(self):
        self.atteck()
        self.x = atteck_dir.x
        self.y = atteck_dir.y
        if self.fire_term == 0 and weapon == 0:
            self.angle = math.atan2(mouse_y-player.centery, mouse_x-player.centerx)
            self.degree = math.degrees(self.angle)*-1
            self.dx = 0 #math.cos(self.angle)*self.speed
            self.dy = 0 #math.sin(self.angle)*self.speed
            self.list.append([self.x-self.width/2, self.y-self.height/2, self.dx, self.dy, 
                                    self.angle, self.speed])
            self.fire_term = firegun_time
        for B in self.list:
            if B[0] >= screen_width:
                self.list.remove(B)
            elif B[1] >= screen_height:
                self.list.remove(B)         
        for B in self.list:
            B[5] += self.speed_increase
            B[2] = math.cos(B[4])*B[5]
            B[3] = math.sin(B[4])*B[5]
            B[0] += B[2]
            B[1] += B[3]
            screen.blit(self.img,(B[0],B[1]))
        if weapon == 0:
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
        self.atteck_timelong = knife_atteck_timelong
        self.atteck = False

    def Atteck(self):
        #공격, 히트박스 위치 설정
        global knife_atteck_term, knife_atteck_timelong
        if self.atteck_term > 0:
            self.atteck_term -= 1

        if click_left == True and self.atteck_term == 0 and weapon == 1:
            self.atteck = True
            self.atteck_timelong = knife_atteck_timelong
            self.atteck_term = knife_atteck_term
            
        if self.atteck == True and self.atteck_timelong > 0:
            self.atteck_timelong -= 1
            self.angle = math.atan2(mouse_y-player.centery, mouse_x-player.centerx)
            self.x = 50*math.cos(self.angle) + player.centerx - self.width/2
            self.y = 50*math.sin(self.angle) + player.centery - self.height/2
            screen.blit(self.img,(self.x, self.y))
        #데미지 줌
            self.rect = self.img.get_rect()
            self.rect.topleft = (self.x,self.y)
            
            for Zmk in zombie_melee.list:
                Zmk_rect = zombie_melee.img.get_rect()
                Zmk_rect.topleft = (Zmk[0], Zmk[1])
                if self.rect.colliderect(Zmk_rect):
                    Zmk[5] -= 2
        #히트박스 위치 초기화
        if self.atteck_timelong == 0:
            self.x, self.y = None, None
        
    def update(self):
        self.Atteck()       
        
#좀비(근접)
class Zombie_melee():
    def __init__(self):
        self.img = pg.image.load(os.path.join(assets,'zombie_1.png'))
        self.width, self.height = self.img.get_size()
        self.rect = self.img.get_rect()
        self.speed = 2
        self.health = 2
        self.crash_player_time = 0
        self.list = []
        self.spawntime = zombie_melee_spawntime
    def spawn(self):
        if self.spawntime == 0:
            first_random = random.randint(1,4)
            if first_random == 1:
                x_pos = random.randint(0,screen_width-self.width)
                y_pos = -self.height       
            elif first_random == 2:
                x_pos = random.randint(0,screen_width-self.width)
                y_pos = screen_height       
            elif first_random == 3:
                x_pos = -self.width
                y_pos = random.randint(0,screen_height-self.height)
            elif first_random == 4:
                x_pos = screen_width
                y_pos = random.randint(0,screen_height-self.height)
            self.x = x_pos
            self.y = y_pos
            self.angle = 0
            self.dx = 0
            self.dy = 0
            self.list.append([self.x,self.y,self.dx,self.dy,self.angle,self.health,
                                self.crash_player_time])
                            # x:[0] y:[1] dx:[2] dy[3] angle[4] health[5] crash_player_time[6]
            self.spawntime = zombie_melee_spawntime
        self.spawntime -= 1
    def crash_Zm(self):
        a_index, b_index = 0,0
        for Zm1 in self.list:
            for Zm2 in self.list:
                if a_index < b_index:
                    Zm1_rect,Zm2_rect = self.img.get_rect(), self.img.get_rect()
                    Zm1_rect.topleft,Zm2_rect.topleft = (Zm1[0],Zm1[1]), (Zm2[0],Zm2[1])
                    if Zm1_rect.colliderect(Zm2_rect):
                        Zm1_angle = math.atan2(Zm1[1]-Zm2[1],Zm1[0]-Zm1[0])
                        Zm1[2] = math.cos(Zm1_angle)*self.speed
                        Zm1[3] = math.sin(Zm1_angle)*self.speed
                        Zm2[2] = -Zm1[2]
                        Zm2[3] = -Zm1[3]                   
                b_index += 1
            b_index = 0
            a_index += 1
    def atteck(self):
        for Zmp in self.list:
            Zmp_rect = self.img.get_rect()
            Zmp_rect.topleft = (Zmp[0],Zmp[1])
            if Zmp_rect.colliderect(player.rect):
                if Zmp[6] == 0:
                    player.health -= 1
                    Zmp[6] = zombie_melee_crash_player_time
                    print("damaged")
                Zmp[6] -= 1
    
    def die(self):
        for Zm in self.list:
            if Zm[5] <= 0:
                self.list.remove(Zm)
    def update(self):
        zombie_melee.spawn()
        zombie_melee.atteck()  
        self.die()
        
        global crash_Zm_time     
        if crash_Zm_time == 0: #충돌 방지 유효 시간 조정
            self.crash_Zm()
            crash_Zm_time = 3
        crash_Zm_time -= 1  

        for Zm in self.list:
            Zm[0] += Zm[2] 
            Zm[1] += Zm[3]
            Zm[4] = math.atan2(player.y-Zm[1],player.x-Zm[0])
            Zm[2] = math.cos(Zm[4])*self.speed
            Zm[3] = math.sin(Zm[4])*self.speed
            screen.blit(self.img,(Zm[0],Zm[1]))
            
    #게임
def Game():
    player.move()
    player.update()
    atteck_dir.update()
    target_mouse.update()
    bullet.update()
    
    knife.update()

    zombie_melee.update()

#클래스 설정   
player = Player()
atteck_dir = Atteck_dir()
target_mouse = Target_mouse()
bullet = Bullet()
knife = Knife()
zombie_melee = Zombie_melee()

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
            
            if event.key == pg.K_1:
                weapon = 0
                special_weapon = False
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
    if pg.mouse.get_pressed()[1] == True:
        click_right = True
    if pg.mouse.get_pressed()[1] == False:
        click_right = False    

    mouse_x, mouse_y = pg.mouse.get_pos()
    
    print(knife.atteck_term)
    Game() 

    pg.display.flip()
    clock.tick(60)
pg.quit()