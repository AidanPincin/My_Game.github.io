try:
    import pygame
except:
    print("pygame isn't installed")
    print("installing pygame...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame
import math
import random
pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, 32)
w, h = screen.get_size()
if w/1.7777-50<=h<=w/1.7777+50:
    pass
else:
    screen = pygame.display.set_mode((w,w/1.7777))
    w, h = screen.get_size()
clock = pygame.time.Clock()

big_font = pygame.font.SysFont("Arial", round(w/54))
load_text = big_font.render("Loading...", True, (255,255,255))
load_width = load_text.get_width()

##game_speed = 1

def load():
    Button.counter += 1
    screen.fill((0,0,0))
    screen.blit(load_text, (w/2-load_width/2,h/2-h/10.8))
    pygame.draw.rect(screen, (255,255,255), (w/2-w/7.68, h/2-h/28.8, w/3.84, h/14.4), 1)
    pygame.draw.rect(screen, (0,255,0), (w/2-w/7.68+1, h/2-h/28.8+1, (Button.counter/141)*w/3.84-2, h/14.4-2))
    pygame.display.update()

class Button():
    counter = 0
    def __init__(self,x,y,width,height,text,font_size,command,second_command,loading=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = pygame.font.SysFont("Arial", round(font_size)).render(text, True, (200,200,200))
        self.text_width, self.text_height = self.text.get_size()
        self.command = command
        self.second_command = second_command
        if loading:
            load()

    def blit(self):
        pygame.draw.rect(screen, (50,50,50), (self.x,self.y,self.width,self.height))
        screen.blit(self.text, (self.x+self.width/2-self.text_width/2,self.y+self.height/2-self.text_height/2))

    def if_click(self):
        pos = pygame.mouse.get_pos()
        if self.x <= pos[0] <= self.x+self.width:
            if self.y <= pos[1] <= self.y+self.height:
                return self.command
        return self.second_command

yes_button = Button(w/2-w/7.68,h/2,w/19.2,h/27,"yes", w/80, True, False)
no_button = Button(w/2+w/12.8,h/2,w/19.2,h/27,"no",w/80,True,False)

text = big_font.render("Would you like a tutorial on how to play?", True, (0,0,0))
text_width = text.get_width()

clicked_yes = False
clicked_no = False

gold = 100
c=0
d=0
xp = 0
armor_dmg = 0
critx2 = 0
critx3 = 0

def draw_path():
    pygame.draw.rect(screen, (75,75,75), (w-w/9.6,h-h/5.4,w/38.4,h/5.4))
    pygame.draw.rect(screen, (75,75,75), (w/12.8,h-h/5.4,w-w/5.486,h/21.6))
    pygame.draw.rect(screen, (75,75,75), (w/12.8,h-h/2.7,w/38.4,h/5.4))
    pygame.draw.rect(screen, (75,75,75), (w/12.8,h-h/2.7,w-w/5.486,h/21.6))
    pygame.draw.rect(screen, (75,75,75), (w-w/9.6,h-h/1.8,w/38.4,h/4.32))
    pygame.draw.rect(screen, (75,75,75), (w/12.8,h-h/1.8,w-w/5.486,h/21.6))
    pygame.draw.rect(screen, (75,75,75), (w/12.8,h-h/1.35,w/38.4,h/4.32))
    pygame.draw.rect(screen, (75,75,75), (w/12.8,h-h/1.35,w-w/5.486,h/21.6))
    pygame.draw.rect(screen, (75,75,75), (w-w/9.6,h-h/1.08,w/38.4,h/4.32))
    pygame.draw.rect(screen, (75,75,75), (w/38.4,h-h/1.08,w-w/7.68,h/21.6))
    pygame.draw.rect(screen, (0,255,0), (0,h/21.6,w/19.2,h/13.5))

class Bullet():
    def __init__(self, x, y, width, height, damage, bullet_speed, range, l, progress):
        self.x = x+w/384
        self.y = y+h/216
        self.width = width
        self.height = height
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.range = range
        self.l = l
        self.progress = progress

    def Shoot(self):
        if self.progress:
            thing = 0
            while thing == 0:
                try:
                    thing = monsters[self.l]
                except IndexError:
                    self.l -= 1
        else:
            self.l = get_closest_monster(self.x,self.y)
        if monsters != []:
            self.dist_x = (monsters[self.l].x+monsters[self.l].width/2) - (self.x+self.width/2)
            self.dist_y = (monsters[self.l].y+monsters[self.l].height/2) - (self.y+self.height/2)
            pygame.draw.rect(screen, (0,0,0), (self.x+self.width/2, self.y+self.height/2-5, w/192, h/108))
            sum = self.dist_x**2 + self.dist_y**2
            sum1 = math.sqrt(sum)
            self.x += (self.dist_x/sum1)*self.bullet_speed
            self.y += (self.dist_y/sum1)*self.bullet_speed
            if monsters[self.l].x-self.bullet_speed < self.x+self.width/2+self.width/1.5 < monsters[self.l].x+monsters[self.l].width+self.bullet_speed:
                if monsters[self.l].y-self.bullet_speed < self.y+self.height/2-5 < monsters[self.l].y+monsters[self.l].height+self.bullet_speed:
                    armor = monsters[self.l].armor - armor_dmg
                    dm = self.damage
                    if critx2 != 0:
                        roll = random.randint(1,100)
                        if roll <= critx2:
                            dm *= 2

                    if critx3 != 0:
                        roll = random.randint(1,100)
                        if roll <= critx3:
                            dm *= 3

                    dmg = dm - armor
                    if dmg < 0:
                        dmg = 0
                    monsters[self.l].hp -= dmg
                    return True
            return False

class Tower():
    def __init__(self, x, y, dmg, attack_speed, range):
        self.bullets = []
        self.x = x
        self.y = y
        self.time = 60
        self.sum = 0
        self.dmg = dmg
        self.attack_speed = attack_speed
        self.range = range

    def blit(self):
        if monsters != [] and defend == True:
            if self.progress:
                self.l = 0
                index_lst1 = []
                index_lst2 = []
                index_lst3 = []
                index_lst4 = []
                index_lst5 = []
                for ind,monster in enumerate(monsters):
                    x_dist = monster.x - self.x
                    y_dist = monster.y - self.y
                    sum = x_dist**2 + y_dist**2
                    total = math.sqrt(round(sum))
                    if total <= self.range:
                        index_lst1.append(monster.y)
                        index_lst2.append(monster.x)
                        index_lst4.append(ind)
                    
                if index_lst1 != []:
                    closest_y = min(index_lst1)
                    for i,num in enumerate(index_lst1):
                        if num == closest_y:
                            index_lst3.append(index_lst2[i])
                            index_lst5.append(index_lst4[i])

                    if closest_y == h/1.22:
                        closest_x = min(index_lst3)
                        indx = index_lst3.index(closest_x)
                        index = index_lst5[indx]
                    elif closest_y == h/1.577:
                        closest_x = max(index_lst3)
                        indx = index_lst3.index(closest_x)
                        index = index_lst5[indx]
                    elif closest_y == h/2.227:
                        closest_x = min(index_lst3)
                        indx = index_lst3.index(closest_x)
                        index = index_lst5[indx]
                    elif closest_y == h/3.789:
                        closest_x = max(index_lst3)
                        indx = index_lst3.index(closest_x)
                        index = index_lst5[indx]
                    elif closest_y == h/12.706:
                        closest_x = min(index_lst3)
                        indx = index_lst3.index(closest_x)
                        index = index_lst5[indx]
                    try:
                        self.l = index
                    except:
                        pass

            else:
                self.l = get_closest_monster(self.x,self.y)
            self.dist_x = monsters[self.l].x - self.x + w/96
            self.dist_y = monsters[self.l].y - self.y + h/54
            sum = self.dist_x**2 + self.dist_y**2
            sum1 = math.sqrt(sum)
            self.sum = sum1
            x = (self.dist_x/sum1)*w/76.8
            y = (self.dist_y/sum1)*w/76.8
            if sum1 <= self.range:
                pygame.draw.rect(screen, self.color, (self.x+w/384, self.y+h/216, self.width, self.height))
                pygame.draw.line(screen, (0,0,0), (self.x+self.width/2+w/384,self.y+self.height/2+h/216),(self.x+self.width/2+x+w/384,self.y+self.height/2+y+h/216),int(self.width/7.5))
            else:
                pygame.draw.rect(screen, self.color, (self.x+w/384, self.y+h/216, self.width, self.height))
                pygame.draw.line(screen, (0,0,0), (self.x+self.width/2+w/384,self.y+self.height/2+h/216),(self.x+self.width/2+w/64,self.y+self.height/2+h/216),int(self.width/7.5))
        else:
            pygame.draw.rect(screen, self.color, (self.x+w/384, self.y+h/216, self.width, self.height))
            pygame.draw.line(screen, (0,0,0), (self.x+self.width/2+w/384,self.y+self.height/2+h/216),(self.x+self.width/2+w/64,self.y+self.height/2+h/216),int(self.width/7.5))

    def shoot(self):
        if self.sum <= self.range:
            if self.time < 60/self.attack_speed:
                self.time += 1
            else:
                self.bullets.append(Bullet(self.x,self.y,self.width,self.height, self.dmg, self.bullet_speed, self.range, self.l, self.progress))
                self.time = 0
                if sound:
                    self.sound.play(0,750)

        for i in self.bullets:
            hit = i.Shoot()
            if hit:
                self.bullets.remove(i)
                hit = False

class basic_tower(Tower):
    color = (255,0,0)
    width = w/48
    height = h/27
    bullet_speed = w/96
    tower_type = 'basic tower'
    up_cost1 = 10
    range2 = 250
    mult1 = 0
    up_cost2 = 10
    mult2 = 0
    up_cost3 = 10
    mult3 = 0
    progress = False
    sell_value = math.ceil(0.75*25)
    sound = pygame.mixer.Sound('basic.mp3')

class fast_tower(Tower):
    color = (255,255,0)
    width = w/48
    range2 = 300
    height = h/27
    bullet_speed = w/96
    tower_type = 'fast tower'
    up_cost1 = 20
    mult1 = 0
    up_cost2 = 20
    mult2 = 0
    up_cost3 = 20
    mult3 = 0
    progress = False
    sell_value = math.ceil(0.75*50)
    sound = pygame.mixer.Sound('fast.mp3')

class sniper_tower(Tower):
    color = (0,0,255)
    width = w/48
    height = h/27
    range2 = 2200
    bullet_speed = w/48
    tower_type = 'sniper tower'
    up_cost1 = 40
    mult1 = 0
    up_cost2 = 40
    mult2 = 0
    up_cost3 = None
    progress = False
    sell_value = 75
    sound = pygame.mixer.Sound('sniper.mp3')

class Base():
    def __init__(self):
        self.hp = 100

    def hp_bar(self):
        pygame.draw.rect(screen, (255,255,255), (w-w/8.533, h/86.4, w/9.6, h/43.2))
        pygame.draw.rect(screen, (255,0,0), (w-w/8.533, h/86.4, self.hp*((w/9.6)/100), h/43.2))
        screen.blit(hp_txt, (w-w/6.4, h/86.4))

base = Base()
font = pygame.font.SysFont("Arial", round(w/120))
hp_txt = font.render(str(base.hp) + "/100", True, (0,0,0))


class Monster():
    def __init__(self,delay):
        self.x = w-w/9.846
        self.y = h-h/24+delay
        self.step1 = False
        self.step2 = False
        self.step3 = False
        self.step4 = False
        self.step5 = False
        self.step6 = False
        self.step7 = False
        self.step8 = False
        self.step9 = False
        self.step10 = False
    def blit(self):
        if self.step1 == False:
            self.y -= self.speed
            if self.y < h-h/5.538:
                self.y = h-h/5.538
                self.step1 = True
        elif self.step2 == False:
            self.x -= self.speed
            if self.x < w/12.387:
                self.x = w/12.387
                self.step2 = True
        elif self.step3 == False:
            self.y -= self.speed
            if self.y <= h-h/2.734:
                self.y = h-h/2.734
                self.step3 = True
        elif self.step4 == False:
            self.x += self.speed
            if self.x >= w-w/9.846:
                self.x = w-w/9.846
                self.step4 = True
        elif self.step5 == False:
            self.y -= self.speed
            if self.y <= h-h/1.815:
                self.y = h-h/1.815
                self.step5 = True
        elif self.step6 == False:
            self.x -= self.speed
            if self.x < w/12.387:
                self.x = w/12.387
                self.step6 = True
        elif self.step7 == False:
            self.y -= self.speed
            if self.y <= h-h/1.358:
                self.y = h-h/1.358
                self.step7 = True
        elif self.step8 == False:
            self.x += self.speed
            if self.x >= w-w/9.846:
                self.x = w-w/9.846
                self.step8 = True
        elif self.step9 == False:
            self.y -= self.speed
            if self.y <= h-h/1.085:
                self.y = h-h/1.085
                self.step9 = True
        elif self.step10 == False:
            self.x -= self.speed
            if self.x < w/25.6:
                base.hp -= self.damage
                hp_txt = font.render(str(base.hp) + "/100", True, (0,0,0))
                return True, hp_txt
        hp_txt = font.render(str(base.hp) + "/100", True, (0,0,0))
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height))
        pygame.draw.rect(screen, (255,255,255), (self.x,self.y-h/54,w/48,h/108))
        pygame.draw.rect(screen, (255,0,0), (self.x,self.y-h/54,(self.hp/self.max_hp)*w/48,h/108))
        return False, hp_txt

class basic_monster(Monster):
    color = (0,0,0)
    width = w/48
    height = h/27
    hp = 5
    max_hp = 5
    speed = w/640
    damage = 1
    gold_drop = 1
    armor = 0
    kill_score = 1
    xp_drop = 0.1

class tough_monster(Monster):
    color = (33,122,64)
    width = w/48
    height = h/27
    hp = 20
    armor = 1
    gold_drop = 2
    max_hp = 20
    speed = w/960
    damage = 2
    kill_score = 2
    xp_drop = 0.2

class boss1(Monster):
    color = (255,0,0)
    width = w/48
    height = h/27
    hp = 500
    max_hp = 500
    armor = 3
    gold_drop = 20
    speed = w/1920
    damage = 20
    kill_score = 20
    xp_drop = 2

class boss2(Monster):
    color = (84, 94, 14)
    width = w/48
    height = h/27
    hp = 500
    max_hp = 500
    armor = 30
    gold_drop = 30
    speed = w/960
    damage = 30
    kill_score = 30
    xp_drop = 3

class fast_monster(Monster):
    color = (255,255,0)
    width = w/48
    height = h/27
    hp = 40
    max_hp = 40
    armor = 0
    gold_drop = 3
    speed = w/384
    damage = 3
    kill_score = 3
    xp_drop = 0.3

monsters = []
gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
font2 = pygame.font.SysFont("Arial", round(w/96))

research = False
 
wave_button = Button(w/76.8,h/216,w/19.2,h/27,"Next wave",w/120,True,False)
shop_button = Button(w/12.8,h/216,w/19.2,h/27,"Shop", w/120, True, False)
monster_button = Button(w/6.981,h/216,w/19.2,h/27,"Monster info", w/120, True, False)
research_button = Button(w/4.8, h/216, w/19.2, h/27, "Research", w/120, True, False)
settings_button = Button(w/3.657,h/216, w/19.2, h/27, "Settings", w/120, True, False)
back_button = Button(w/2-w/38.4,h-h/5.4,w/19.2,h/21.6,"Back",w/80,False,True)
##speed_button = Button(w/2,h/216,100,30,"speed",24,True,False)
buy1 = Button(w/19.2,h/3.6,w/19.2,h/27,"Buy",w/80,True,False)
buy2 = Button(w/4.8,h/3.6,w/19.2,h/27,"Buy",w/80,True,False)
buy3 = Button(w/2.743,h/3.6,w/19.2,h/27,"Buy",w/80,True,False)

class display_shop_item():
    def __init__(self, x, y, width, height, dmg, attack_speed, color, range, tower_name, cost):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.txt1 = font2.render("Damage -- " + str(dmg), True, (0,0,0))
        self.txt2 = font2.render("Attack speed -- " + str(attack_speed), True, (0,0,0))
        self.txt3 = font2.render("Range -- " + str(range), True, (0,0,0))
        self.txt4 = font2.render(tower_name + ":", True, (0,0,0))
        self.txt5 = font2.render("Cost -- " + str(cost), True, (0,0,0))
        self.txt1_width = self.txt1.get_width()
        self.txt2_width = self.txt2.get_width()
        self.txt3_width = self.txt3.get_width()
        self.txt4_width = self.txt4.get_width()
        self.txt5_width = self.txt5.get_width()
        load()

    def blit(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0,0,0), (self.x+self.width/2,self.y+self.height/2-self.height/15,self.width/2+self.width/5,self.height/7.5))
        screen.blit(self.txt4, (self.x+self.width/2-self.txt4_width/2, self.y+self.height+h/72))
        screen.blit(self.txt1, (self.x+self.width/2-self.txt1_width/2, self.y+self.height+h/27))
        screen.blit(self.txt2, (self.x+self.width/2-self.txt2_width/2, self.y+self.height+h/16.615))
        screen.blit(self.txt3, (self.x+self.width/2-self.txt3_width/2, self.y+self.height+h/12))
        screen.blit(self.txt5, (self.x+self.width/2-self.txt5_width/2, self.y+self.height+h/9.391))


def get_closest_monster(x,y):
    distances =[]
    for k in monsters:
        dist_x = k.x - x
        dist_y = k.y - y
        sum = dist_x**2 + dist_y**2
        distance = round(math.sqrt(sum))
        distances.append(distance)
    
    lowest = min(distances)
    for j,_ in enumerate(distances):
        if lowest == distances[j]:
            closest_monster = j

    return closest_monster

towers = []
wave_click = False
defend = False
wave = 0
shop = False
place_tower = False
no_gold_txt = big_font.render("Not enough gold!",True,(255,0,0))
no_gold_width = no_gold_txt.get_width()
no_gold = False
b=0
buy_fast = False
buy_sniper = False

wave_txt = font.render("Wave -- " + str(wave), True, (0,0,0))
basic = display_shop_item(w/19.2,h/21.6,w/19.2, h/10.8, 3, 1, (255,0,0),250, "Basic Tower", 25)
fast = display_shop_item(w/4.8,h/21.6,w/19.2,h/10.8,1.5,5,(255,255,0),300,"Fast Tower", 50)
sniper = display_shop_item(w/2.743,h/21.6,w/19.2,h/10.8,15,0.5,(0,0,255),"Infinite","Sniper Tower",100)
game_over_txt = big_font.render("GAME OVER", True, (255,0,0))
game_over_width = game_over_txt.get_width()
restart_txt = font.render("press r to restart", True, (255,0,0))
restart_width = restart_txt.get_width()

ROWS = 4
COLS = 31

cant_place_txt = big_font.render("Can't place that here!", True, (255,0,0))
cp_width = cant_place_txt.get_width()

tower_cordinates = []
cant_place = False

class tt():
    def __init__(self,x,y,text,color, font_size):
        self.text = pygame.font.SysFont("Arial", round(w/(1920/font_size))).render(text, True, color)
        self.text_width, self.text_height = self.text.get_size()
        self.x = w/(1920/x)
        self.y = h/(1080/y)
        load()

    def blit(self):
        screen.blit(self.text, (self.x-self.text_width/2,self.y-self.text_height/2))

class tps():
    clicked = False
    cords = (0,0)
    def __init__(self, rows, cols, x, y):
        self.rows = rows
        self.cols = cols
        self.x = x
        self.y = y
        load()

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.x+col*(w/(1920/50.6)) <= pos[0] <= self.x+col*(w/(1920/50.6))+w/(1920/50):
                    if self.y-row*(h/(1080/50))-(h/(1080/50)) <= pos[1] <= self.y-row*(h/(1080/50)):
                        if (self.x+col*(w/(1920/50.6)), self.y-row*(h/(1080/50))-h/(1080/50)) in tower_cordinates:
                            pass
                        else:
                            pygame.draw.rect(screen, (0,255,0), (self.x+col*(w/(1920/50.6)),self.y-row*(h/(1080/50))-h/(1080/50),w/(1920/50.6),h/(1080/50)))

    def if_click(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.x+col*w/(1920/50.6) <= pos[0] <= self.x+col*w/(1920/50.6)+w/(1920/50):
                    if self.y-row*h/(1080/50)-h/(1080/50) <= pos[1] <= self.y-row*h/(1080/50):
                        tps.clicked = True
                        tps.cords = (self.x+col*w/(1920/50.6), self.y-row*h/(1080/50)-h/(1080/50))
t1 = tps(3, 34, 0, h)
t2 = tps(3, 3, w-w/12.8, h)
t3 = tps(3, 34, w/9.6, h-h/5.4)
t4 = tps(3, 3, 0, h-h/5.4)
t5 = tps(1, 3, 0, h-h/7.2)
t6 = tps(1, 3, w-w/12.8, h-h/7.2)
t7 = tps(1, 3, 0, h-h/3.086)
t8 = tps(1, 3, w-w/12.8, h-h/3.086)
t9 = tps(3, 34, 0, h-h/2.7)
t10 = tps(3, 3, w-w/12.8, h-h/2.7)
t11 = tps(1,3,0,h-h/1.964)
t12 = tps(1,3,w-w/12.8,h-h/1.964)
t13 = tps(3, 34, w/9.6, h-h/1.8)
t14 = tps(3, 3, 0, h-h/1.8)
t15 = tps(1,3,0,h-h/1.44)
t16 = tps(1,3,w-w/12.8,h-h/1.44)
t17 = tps(3, 34, 0, h-h/1.35)
t18 = tps(3, 3, w-w/12.8, h-h/1.35)
t19 = tps(1,3,w-w/12.8,h-h/1.137)
demo_complete = False
demo_txt = big_font.render("Congratulations you have beaten the demo!", True, (0,255,0))
demo_width = demo_txt.get_width()
txt = font2.render("press r to restart if you would like to try and get a better score!", True, (0,255,0))
txt_width = txt.get_width()
step = 1
tt1 = tt(w-325,112.5,"This is your base's hp(current/max)",(0,0,0),12)
tt2 = tt(w-100,112.5,"This is your base hp bar", (0,0,0), 12)
continue_txt = tt(w-200,175,"click anywhere to continue", (0,0,0), 16)
tt3 = tt(100, 160, "This is your base", (0,0,0), 12)
tt4 = tt(100, 175, "Don't let monsters reach it!", (0,0,0), 12)
tt5 = tt(1046.25, 62.5, "This is how much gold you have", (0,0,0), 12)
tt6 = tt(1246.25, 62.5, "This is the wave your on", (0,0,0), 12)
tt7 = tt(200, 95, "This is the shop button", (0,0,0), 12)
tt8 = tt(200, 110, "This is where you will buy all", (0,0,0), 12)
tt9 = tt(200, 125, "your towers to defend your base", (0,0,0), 12)
tt10 = tt(200, 140, "click on it", (0,0,0), 12)
tt11 = tt(450, 412.5, "These are what the different towers look like", (0,0,0), 12)
tt12 = tt(450, 412.5, "These are the different names of the towers", (0,0,0), 12)
tt13 = tt(450, 412.5, "These are the towers stats", (0,0,0), 12)
tt14 = tt(1000,200,"How much damage it does to monsters", (0,0,0), 12)
tt15 = tt(987.5,225,"How many bullets it fires per second", (0,0,0), 12)
tt16 = tt(1056.25,250,"How far away it can shoot monsters(higher numbers better)", (0,0,0), 12)
tt17 = tt(1000,275,"How much gold it costs to buy the tower", (0,0,0), 12)
tt18 = tt(150,412.5,"click the buy button", (0,0,0), 12)
tt19 = tt(w/2, 20, "Place the tower down wherever you want", (0,0,0), 12)
tt20 = tt(200,97.5,"click shop", (0,0,0), 12)
tt21 = tt(w/2,h/2-200,"Congratulations! You have completed the tutorial!", (0,0,0), 36)
tt22 = tt(w/2, h/2, "click anywhere to continue playing", (0,0,0), 18)
tt23 = tt(150, 110, "This is the next wave button", (0,0,0), 12)
tt24 = tt(150, 130, "When you it is clicked it will start the next wave", (0,0,0), 12)
tt25 = tt(150, 150, "You cannot start the next wave or open the shop", (0,0,0), 12)
tt26 = tt(150,170,"until you finish the wave that you have started", (0,0,0),12)
tt27 = tt(150,190,"click next wave to continue", (0,0,0), 12)
tt28 = tt(w/2, 20, "You have not discovered any monsters yet!", (255,0,0), 48)
tt29 = tt(200, 100, "Penatrating Bullets", (0,0,0), 32)
tt30 = tt(200, 135, "All towers do +5 damage", (0,0,0), 16)
tt31 = tt(200, 300, "Critical Chance l", (0,0,0), 32)
tt32 = tt(200, 500, "Critical Chance ll", (0,0,0), 32)
tt33 = tt(200, 335, "+5% chance to hit for x2 damage", (0,0,0), 16)
tt34 = tt(200, 535, "+3% chance to hit for x3 damage", (0,0,0), 16)
tt35 = tt(200, 355, "Damage stacks with critical chance ll", (0,0,0), 16)
tt36 = tt(200, 555, "Damage stacks with critical chance l", (0,0,0), 16)
tt37 = tt(200, 100, "Sound:", (0,0,0), 36)
font3 = pygame.font.SysFont("Arial", round(w/96))
no_gold1 = False
tt38 = font3.render("Current crit -- %"+str(critx2), True, (0,0,0))
tt39 = font3.render("Current crit -- %"+str(critx3), True, (0,0,0))
tt40 = font3.render("Current damage -- "+str(armor_dmg), True, (0,0,0))

R_Button1 = Button(w/3.85, h/12, w/9.6, h/21.6, "Research for 100xp", w/96, False, True)
B_Button1 = Button(w/3.85, h/12, w/9.6, h/21.6, "Bought", w/96, False, True)
R_Button2 = Button(w/3.85, h/3.724, w/9.6, h/21.6, "Research for 150xp", w/96, False, True)
B_Button2 = Button(w/3.85, h/3.724, w/9.6, h/21.6, "Bought", 20, False, True)
R_Button3 = Button(w/3.85, h/2.204, w/9.6, h/21.6, "Research for 200xp", w/96, False, True)
B_Button3 = Button(w/3.85, h/2.204, w/9.6, h/21.6, "Bought", w/96, False, True)
S_Button1 = Button(w/5.486, h/12-h/108, w/25.6, h/21.6, "On", w/96, True, False)

class Monster_Info():
    def __init__(self, x, y, name, hp, speed, armor, dmg, color):
        self.x = x
        self.y = y
        self.color = color
        self.txt1 = tt(x+w/38.4, y+h/9.391, name+":", (0,0,0), w/96)
        self.txt2 = tt(x+w/38.4, y+h/7.714, "HP -- " + str(hp), (0,0,0), w/96)
        self.txt3 = tt(x+w/38.4, y+h/6.545, "Armor -- " + str(armor), (0,0,0), w/96)
        self.txt4 = tt(x+w/38.4, y+h/5.684, "Speed -- " + str(speed), (0,0,0), w/96)
        self.txt5 = tt(x+w/38.4, y+h/5.023, "Damage -- " + str(dmg), (0,0,0), w/96)
        load()

    def blit(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, w/19.2, h/10.8))
        self.txt1.blit()
        self.txt2.blit()
        self.txt3.blit()
        self.txt4.blit()
        self.txt5.blit()

basic_info = Monster_Info(w/19.2,h/21.6,"Weak Boi",5,3,0,1,(0,0,0))
tough_info = Monster_Info(w/4.8,h/21.6,"Tough Boi",20,2,1,2,(33,122,64))
boss1_info = Monster_Info(w/2.743,h/21.6,"Chunky Boi",500,1,3,20,(255,0,0))
fast_info = Monster_Info(w/1.92, h/21.6, "Speedy Boi",40,5,0,3,(255,255,0))
boss2_info = Monster_Info(w/1.477, h/21.6, "Chonky Boi",500,2,30,30,(84, 94, 14))

encounter = False
encounter1 = False
encounter2 = False
encounter3 = False
encounter4 = False
encounter5 = False

class upgrades():
    def __init__(self, x, y, dmg, attack_speed, range, cost1, cost2, cost3, progress, sell_value):
        self.x = x
        self.y = y
        self.dmg = dmg
        self.attack_speed = attack_speed
        self.range = range
        self.b4 = Button(x+w/17.455, y+h/108, w/96, h/48, "<", w/80, True, False, False)
        self.b5 = Button(x+w/7.245, y+h/108, w/96, h/48, ">", w/80, True, False, False)
        self.b6 = Button(x+w/20.211, y-h/27, w/17.455, h/36, "sell for " + str(sell_value) + " gold", w/160, True, False, False)
        self.b3 = Button(x+w/10.378, y+h/7.2, w/21.333, h/36, "can't upgrade", w/160, True, False, False)
        if cost3 != None:
            self.b3 = Button(x+w/10.378, y+h/7.2, w/14.222, h/36, "upgrade for " + str(cost3) + " gold", w/160, True, False, False)
        self.b1 = Button(x+w/10.378, y+h/21.6, w/14.222, h/36, "upgrade for " + str(cost1) + " gold", w/160, True, False, False)
        self.b2 = Button(x+w/10.378, y+h/10.8, w/14.222, h/36, "upgrade for " + str(cost2) + " gold", w/160, True, False, False)
        self.txt1 = font3.render("Damage -- " + str(dmg), True, (0,0,0))
        self.txt2 = font3.render("Attack speed -- " + str(attack_speed), True, (0,0,0))
        self.txt3 = font3.render("Range -- " + str(range), True, (0,0,0))
        self.txt4 = font3.render("Target -- ", True, (0,0,0))
        if progress:
            self.txt5 = font.render("closest to base", True, (0,0,0))
        else:
            self.txt5 = font.render("closest to tower", True, (0,0,0))

    def blit(self):
        pygame.draw.rect(screen, (125,125,125), (self.x-w/76.8,self.y-h/21.6,w/5.486,h/4.32))
        self.b1.blit()
        self.b2.blit()
        self.b3.blit()
        self.b4.blit()
        self.b5.blit()
        self.b6.blit()
        screen.blit(self.txt1, (self.x-w/76.8,self.y+h/21.6))
        screen.blit(self.txt2, (self.x-w/76.8,self.y+h/10.8))
        screen.blit(self.txt3, (self.x-w/76.8,self.y+h/7.2))
        screen.blit(self.txt4, (self.x+w/192,self.y+h/108))
        screen.blit(self.txt5, (self.x+w/14.491,self.y+h/86.4))

game_over = False
upgrade = None
click1 = False
click2 = False
click3 = False
click4 = False
click5 = False
click6 = False
monster_page = False
score = 0

encounter_txt1 = tt(960, 540-315, "You see a new type of monster in the distance!", (255,0,0), 36)
encounter_txt2 = tt(960, 540-270, "You can now look at this monster in the Monster info tab", (0,0,0), 20)
continue_text = tt(960, 540+200, "Click anywhere to continue", (0,0,0), 20)

class Encounter():
    def __init__(self, monster, color, hp, armor, speed, dmg):
        self.color = color
        self.txt1 = tt(960, 540+15, monster + ":", (0,0,0), 24)
        self.txt2 = tt(960, 540+45, "HP -- " + str(hp), (0,0,0), 24)
        self.txt3 = tt(960, 540+75, "Armor -- " + str(armor), (0,0,0), 24)
        self.txt4 = tt(960, 540+105, "Speed -- " + str(speed), (0,0,0), 24)
        self.txt5 = tt(960, 540+135, "Damage -- " + str(dmg), (0,0,0), 24)
        load()

    def blit(self):
        pygame.draw.rect(screen, (175,175,175), (w/2-w/3.84,h/2-h/3.224,w/1.92,h/1.8))
        pygame.draw.rect(screen, self.color, (w/2-w/19.2, h/2-h/5.4, w/9.6, h/5.4))
        encounter_txt1.blit()
        encounter_txt2.blit()
        self.txt1.blit()
        self.txt2.blit()
        self.txt3.blit()
        self.txt4.blit()
        self.txt5.blit()
        continue_text.blit()

Encounter1 = Encounter("Weak Boi", (0,0,0), 5, 0, 3, 1)
Encounter2 = Encounter("Tough Boi", (33,122,64), 20, 1, 2, 2)
Encounter3 = Encounter("Chunky Boi", (255,0,0), 500, 3, 1, 20)
Encounter4 = Encounter("Speedy Boi", (255,255,0), 20, 0, 5, 3)
Encounter5 = Encounter("Chonky Boi", (84, 94, 14), 500, 30, 2, 30)
xp_txt = font.render("XP -- " + str(xp), True, (0,0,0))
show_R1 = True
show_R2 = True
show_R3 = True
run = False
settings = False
tutorial = False
change_sound = False
sound = True
while run:
    screen.fill((0,125,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_yes = yes_button.if_click()
            clicked_no = no_button.if_click()
            if clicked_no:
                tutorial = False
                run = False
            if clicked_yes:
                tutorial = True
                run = False

    screen.blit(text, (w/2-text_width/2,h/2-h/7.2))
    yes_button.blit()
    no_button.blit()

    pygame.display.update()

run = True
while run:
    screen.fill((0,125,0))
    if demo_complete:
        screen.fill((0,0,125))
    if tutorial:
        screen.fill((0,25,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif demo_complete:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    towers = []
                    tower_cordinates = []
                    monsters = []
                    wave = 0
                    gold = 100
                    xp = 0
                    score = 0
                    demo_complete = False
                    base = Base()
                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                    wave_txt = font.render("Wave -- " + str(wave), True, (0,0,0))
                    hp_txt = font.render(str(base.hp) + "/100", True, (0,0,0))
                    wave_button = Button(25,5,100,40,"Next wave",16,True,False)
                    shop_button = Button(150,5,100,40,"Shop", 16, True, False)
                    back_button = Button(w/2-50,h-200,100,50,"Back",24,False,True)
                    xp_txt = font.render("XP -- " + str(xp), True, (0,0,0))

        elif game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    towers = []
                    tower_cordinates = []
                    monsters = []
                    wave = 0
                    gold = 75
                    game_over = False
                    base = Base()
                    xp = 0
                    score = 0
                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                    wave_txt = font.render("Wave -- " + str(wave), True, (0,0,0))
                    hp_txt = font.render(str(base.hp) + "/100", True, (0,0,0))
                    wave_button = Button(25,5,100,40,"Next wave",16,True,False)
                    shop_button = Button(150,5,100,40,"Shop", 16, True, False)
                    back_button = Button(w/2-50,h-200,100,50,"Back",24,False,True)
                    xp_txt = font.render("XP -- " + str(xp), True, (0,0,0))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if place_tower:
                pos = pygame.mouse.get_pos()
                t1.if_click()
                t2.if_click()
                t3.if_click()
                t4.if_click()
                t5.if_click()
                t6.if_click()
                t7.if_click()
                t8.if_click()
                t9.if_click()
                t10.if_click()
                t11.if_click()
                t12.if_click()
                t13.if_click()
                t14.if_click()
                t15.if_click()
                t16.if_click()
                t17.if_click()
                t18.if_click()
                t19.if_click()
                if tps.clicked:
                    if tps.cords in tower_cordinates:
                        cant_place = True
                    else:
                        if buy_basic:
                            gold -= 25
                            towers.append(basic_tower(tps.cords[0],tps.cords[1], 3, 1, w/7.68))
                        if buy_fast:
                            gold -= 50
                            towers.append(fast_tower(tps.cords[0],tps.cords[1], 1.5, 5, w/6.4))
                        if buy_sniper:
                            gold -= 100
                            towers.append(sniper_tower(tps.cords[0],tps.cords[1], 15, 0.5, w/0.864))
                        tower_cordinates.append(tps.cords)
                        gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                        place_tower = False
                        shop = False
                    tps.clicked = False

                else:
                    cant_place = True

            elif shop:
                if tutorial:
                    if step == 11:
                        buy_fast = buy2.if_click()
                        if buy_fast:
                            buy_basic = False
                            place_tower = True
                            step += 1
                            tt18.x = 150
                    elif step == 9:
                        buy_basic = buy1.if_click()
                        if buy_basic:
                            place_tower = True
                            step += 1
                            tt18.x = 450
                    elif step == 8:
                        step += 1
                    elif step == 7:
                        step += 1
                    elif step == 6:
                        step += 1
                else:
                    shop = back_button.if_click()
                    buy_basic = buy1.if_click()
                    buy_fast = buy2.if_click()
                    buy_sniper = buy3.if_click()
                    if buy_basic:
                        if gold < 25:
                            buy_basic = False
                            no_gold = True
                        else:
                            place_tower = True
                    if buy_fast:
                        if gold < 50:
                            buy_fast = False
                            no_gold = True
                        else:
                            place_tower = True
                    if buy_sniper:
                        if gold < 100:
                            buy_sniper = False
                            no_gold = True
                        else:
                            place_tower = True

            elif monster_page:
                monster_page = back_button.if_click()

            elif encounter:
                if wave == 1:
                    encounter1 = True
                if wave == 4:
                    encounter2 = True
                if wave == 5:
                    encounter3 = True
                if wave == 7:
                    encounter4 = True
                if wave == 10:
                    encounter5 = True
                encounter = False

            elif research:
                research = back_button.if_click()
                if show_R1:
                    show_R1 = R_Button1.if_click()
                    if show_R1 == False:
                        if xp >= 100:
                            armor_dmg += 5
                            xp -= 100
                            tt40 = font3.render("Current damage -- "+str(armor_dmg), True, (0,0,0))
                            if armor_dmg<100:
                                show_R1 = True
                        else:
                            show_R1 = True
                if show_R2:
                    show_R2 = R_Button2.if_click()
                    if show_R2 == False:
                        if xp >= 150:
                            critx2 += 5
                            xp -= 150
                            if critx2 < 100:
                                show_R2 = True
                            tt38 = font3.render("Current crit -- %"+str(critx2), True, (0,0,0))
                        else:
                            show_R2 = True
                if show_R3:
                    show_R3 = R_Button3.if_click()
                    if show_R3 == False:
                        if xp >= 200:
                            critx3 += 3
                            xp -= 200
                            if critx3 < 100:
                                show_R3 = True
                            tt39 = font3.render("Current crit -- %"+str(critx3), True, (0,0,0))
                        else:
                            show_R3 = True

            elif settings:
                change_sound = S_Button1.if_click()
                settings = back_button.if_click()
                if change_sound:
                    if sound:
                        sound = False
                        S_Button1.text = pygame.font.SysFont("Arial", round(w/96)).render("Off", True, (200,200,200))
                    else:
                        sound = True
                        S_Button1.text = pygame.font.SysFont("Arial", round(w/96)).render("On", True, (200,200,200))

            else:
                if tutorial:
                    if step == 16:
                        tutorial = False
                    elif step == 14:
                        defend = wave_button.if_click()
                        if defend:
                            wave_click = True
                    elif step == 10:
                        shop = shop_button.if_click()
                        if shop:
                            step += 1
                    elif step == 5:
                        shop = shop_button.if_click()
                        if shop:
                            step += 1
                            continue_txt.x = 450
                            continue_txt.y = 462.5
                    elif step == 4:
                        step += 1
                    elif step == 3:
                        step += 1
                        continue_txt.x = 1246.25
                    elif step == 2:
                        step += 1
                        continue_txt.x = 1046.25
                        continue_txt.y = 97.5
                    elif step == 1:
                        step += 1
                        continue_txt.x = 112.5
                        continue_txt.y = 212.5

                else:
                    if defend == False:
                        defend = wave_button.if_click()
                    shop = shop_button.if_click()
                    monster_page = monster_button.if_click()
                    research = research_button.if_click()
                    settings = settings_button.if_click()
                    pos = pygame.mouse.get_pos()
                    if upgrade != None:
                        click1 = upgrade.b1.if_click()
                        click2 = upgrade.b2.if_click()
                        click3 = upgrade.b3.if_click()
                        click4 = upgrade.b4.if_click()
                        click5 = upgrade.b5.if_click()
                        click6 = upgrade.b6.if_click()
                        if click1:
                            if towers[index].tower_type == 'basic tower':
                                if gold < towers[index].up_cost1:
                                    no_gold1 = True
                                else:
                                    gold -= towers[index].up_cost1
                                    towers[index].sell_value += math.ceil(towers[index].up_cost1*0.75)
                                    towers[index].dmg += 1.5
                                    towers[index].mult1 += 1
                                    towers[index].mult1 = round(towers[index].mult1*1.5)
                                    towers[index].up_cost1 += towers[index].mult1
                                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                            if towers[index].tower_type == 'fast tower':
                                if gold < towers[index].up_cost1:
                                    no_gold1 = True
                                else:
                                    gold -= towers[index].up_cost1
                                    towers[index].sell_value += math.ceil(towers[index].up_cost1*0.75)
                                    towers[index].dmg += 0.75
                                    towers[index].mult1 += 1
                                    towers[index].mult1 = round(towers[index].mult1*1.5)
                                    towers[index].up_cost1 += towers[index].mult1
                                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                            if towers[index].tower_type == 'sniper tower':
                                if gold < towers[index].up_cost1:
                                    no_gold1 = True
                                else:
                                    gold -= towers[index].up_cost1
                                    towers[index].sell_value += math.ceil(towers[index].up_cost1*0.75)
                                    towers[index].dmg += 7.5
                                    towers[index].mult1 += 1
                                    towers[index].mult1 = round(towers[index].mult1*1.5)
                                    towers[index].up_cost1 += towers[index].mult1
                                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                        if click2:
                            if towers[index].tower_type == 'basic tower':
                                if gold < towers[index].up_cost2:
                                    no_gold1 = True
                                else:
                                    gold -= towers[index].up_cost2
                                    towers[index].sell_value += math.ceil(towers[index].up_cost2*0.75)
                                    towers[index].attack_speed += 0.5
                                    towers[index].mult2 += 1
                                    towers[index].mult2 = round(towers[index].mult2*1.5)
                                    towers[index].up_cost2 += towers[index].mult2
                                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                            if towers[index].tower_type == 'fast tower':
                                if gold < towers[index].up_cost2:
                                    no_gold1 = True
                                else:
                                    gold -= towers[index].up_cost2
                                    towers[index].sell_value += math.ceil(towers[index].up_cost2*0.75)
                                    towers[index].attack_speed += 2.5
                                    towers[index].mult2 += 1
                                    towers[index].mult2 = round(towers[index].mult2*1.5)
                                    towers[index].up_cost2 += towers[index].mult2
                                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                            if towers[index].tower_type == 'sniper tower':
                                if gold < towers[index].up_cost2:
                                    no_gold1 = True
                                else:
                                    gold -= towers[index].up_cost2
                                    towers[index].sell_value += math.ceil(towers[index].up_cost2*0.75)
                                    towers[index].attack_speed += 0.25
                                    towers[index].mult2 += 1
                                    towers[index].mult2 = round(towers[index].mult2*1.5)
                                    towers[index].up_cost2 += towers[index].mult2
                                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                        if click3:
                            if towers[index].tower_type == 'basic tower':
                                if gold < towers[index].up_cost3:
                                    no_gold1 = True
                                else:
                                    gold -= towers[index].up_cost3
                                    towers[index].sell_value += math.ceil(towers[index].up_cost3*0.75)
                                    towers[index].range2 += 125
                                    towers[index].range += w/15.36
                                    towers[index].mult3 += 1
                                    towers[index].mult3 = round(towers[index].mult3*1.5)
                                    towers[index].up_cost3 += towers[index].mult3
                                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                            if towers[index].tower_type == 'fast tower':
                                if gold < towers[index].up_cost3:
                                    no_gold1 = True
                                else:
                                    gold -= towers[index].up_cost3
                                    towers[index].sell_value += math.ceil(towers[index].up_cost3*0.75)
                                    towers[index].range2 += 150
                                    towers[index].range += w/12.8
                                    towers[index].mult3 += 1
                                    towers[index].mult3 = round(towers[index].mult3*1.5)
                                    towers[index].up_cost3 += towers[index].mult3
                                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))

                        if click4:
                            if towers[index].progress:
                                towers[index].progress = False
                            else:
                                towers[index].progress = True
                        if click5:
                            if towers[index].progress:
                                towers[index].progress = False
                            else:
                                towers[index].progress = True
                        if click6:
                            gold += towers[index].sell_value
                            gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                            towers.remove(towers[index])
                            tower_cordinates.remove(tower_cordinates[index])
                    if click1 == False and click2 == False and click3 == False and click4 == False and click5 == False:
                        t1.if_click()
                        t2.if_click()
                        t3.if_click()
                        t4.if_click()
                        t5.if_click()
                        t6.if_click()
                        t7.if_click()
                        t8.if_click()
                        t9.if_click()
                        t10.if_click()
                        t11.if_click()
                        t12.if_click()
                        t13.if_click()
                        t14.if_click()
                        t15.if_click()
                        t16.if_click()
                        t17.if_click()
                        t18.if_click()
                        t19.if_click()
                    if tps.clicked:
                        if tps.cords in tower_cordinates:
                            index = tower_cordinates.index((tps.cords[0],tps.cords[1]))
                            upgrade = upgrades(towers[index].x-w/12.8,towers[index].y-h/5.4,towers[index].dmg,towers[index].attack_speed,towers[index].range2,towers[index].up_cost1,towers[index].up_cost2,towers[index].up_cost3,towers[index].progress,towers[index].sell_value)
                        else:
                            upgrade = None
                    else:
                        upgrade = None

                    if click1:
                        upgrade = upgrades(towers[index].x-w/12.8,towers[index].y-h/5.4,towers[index].dmg,towers[index].attack_speed,towers[index].range2,towers[index].up_cost1,towers[index].up_cost2,towers[index].up_cost3,towers[index].progress,towers[index].sell_value)
                    if click2:
                        upgrade = upgrades(towers[index].x-w/12.8,towers[index].y-h/5.4,towers[index].dmg,towers[index].attack_speed,towers[index].range2,towers[index].up_cost1,towers[index].up_cost2,towers[index].up_cost3,towers[index].progress,towers[index].sell_value)
                    if click3:
                        upgrade = upgrades(towers[index].x-w/12.8,towers[index].y-h/5.4,towers[index].dmg,towers[index].attack_speed,towers[index].range2,towers[index].up_cost1,towers[index].up_cost2,towers[index].up_cost3,towers[index].progress,towers[index].sell_value)
                    if click4:
                        upgrade = upgrades(towers[index].x-w/12.8,towers[index].y-h/5.4,towers[index].dmg,towers[index].attack_speed,towers[index].range2,towers[index].up_cost1,towers[index].up_cost2,towers[index].up_cost3,towers[index].progress,towers[index].sell_value)
                    if click5:
                        upgrade = upgrades(towers[index].x-w/12.8,towers[index].y-h/5.4,towers[index].dmg,towers[index].attack_speed,towers[index].range2,towers[index].up_cost1,towers[index].up_cost2,towers[index].up_cost3,towers[index].progress,towers[index].sell_value)
                    

                if defend == True and monsters == [] and wave != 12:
                    wave += 1
                    wave_txt = font.render("Wave -- " + str(wave), True, (0,0,0))
                    if wave == 1:
                        a = 1
                        while a<=25:
                            monsters.append(basic_monster(a*w/16))
                            a+=1
                    if wave == 2:
                        a = 1
                        while a<=50:
                            monsters.append(basic_monster(a*w/21.333))
                            a+=1
                    if wave == 3:
                        a = 1
                        while a<=75:
                            monsters.append(basic_monster(a*w/32))
                            a+=1
                    if wave == 4:
                        a = 1
                        while a<=25:
                            monsters.append(tough_monster(a*w/16))
                            a+=1
                        a = 1
                        while a<=50:
                            monsters.append(basic_monster(a*w/32))
                            a+=1
                    if wave == 5:
                        monsters.append(boss1(w/32))
                    if wave == 6:
                        a=1
                        while a <= 100:
                            monsters.append(tough_monster(a*w/32))
                            a+=1
                        a=1
                        while a <= 3:
                            monsters.append(boss1(a*w/16))
                            a+=1
                    if wave == 7:
                        a = 1
                        while a <= 25:
                            monsters.append(fast_monster(a*w/16))
                            a+=1
                    if wave == 8:
                        a=1 
                        while a <= 25:
                            monsters.append(fast_monster(a*w/8))
                            monsters.append(tough_monster(a*w/32))
                            a+=1
                        a=1
                        while a <= 10:
                            monsters.append(boss1(a*w/8))
                            a+=1
                    if wave == 9:
                        a = 1
                        while a <= 100:
                            monsters.append(fast_monster(a*w/32))
                            a+=1
                    if wave == 10:
                        a=1
                        while a <= 200:
                            monsters.append(tough_monster(a*w/32))
                            a+=1
                        a=1
                        while a <= 20:
                            monsters.append(boss1(a*w/32))
                            a+=1
                        monsters.append(boss2(w/0.32))
                    if wave == 11:
                        a=1
                        while a<=5:
                            monsters.append(boss2(a*w/16))
                            a+=1
                    if wave == 12:
                        a=1
                        while a<=50:
                            monsters.append(fast_monster(a*w/32))
                            a+=1
                        a=1
                        while a<= 10:
                            monsters.append(boss2(a*w/32))
                            a+=1

                if encounter1 == False:
                    if wave == 1:
                        encounter = True

                if encounter2 == False:
                    if wave == 4:
                        encounter = True
                
                if encounter3 == False:
                    if wave == 5:
                        encounter = True

                if encounter4 == False:
                    if wave == 7:
                        encounter = True

                if encounter5 == False:
                    if wave == 10:
                        encounter = True

    if demo_complete:
        screen.blit(score_txt, (w/2-score_width/2,h/2))
        screen.blit(demo_txt, (w/2-demo_width/2,h/2-h/10.8))
        screen.blit(txt, (w/2-txt_width/2,h/2+h/21.6))

    elif game_over:
        screen.blit(game_over_txt, (w/2-game_over_width/2,h/2))
        screen.blit(restart_txt, (w/2-restart_width/2,h/2+h/10.8))

    elif place_tower:
        if tutorial:
            screen.fill((0,125,0))
        draw_path()
        pygame.draw.line(screen, (0,0,0), (w-w/12.8,h/13.5), (w,h/13.5))
        pygame.draw.rect(screen, (150,150,150), (0,0,w,h/21.6))
        for i in towers:
            i.blit()
        for row in range(ROWS):
            pygame.draw.line(screen, (0,0,0), (0,h-row*(h/21.6)),(w-w/9.6,h-row*(h/21.6)))
            pygame.draw.line(screen, (0,0,0), (w-w/12.8,h-row*(h/21.6)),(w,h-row*(h/21.6)))
            pygame.draw.line(screen, (0,0,0), (w/9.6,h-row*(h/21.6)-h/5.4),(w,h-row*(h/21.6)-h/5.4))
            pygame.draw.line(screen, (0,0,0), (0,h-row*(h/21.6)-h/5.4),(w/12.8,h-row*(h/21.6)-h/5.4))
            pygame.draw.line(screen, (0,0,0), (0,h-row*(h/21.6)-h/2.7),(w-w/9.6,h-row*(h/21.6)-h/2.7))
            pygame.draw.line(screen, (0,0,0), (w-w/12.8,h-row*(h/21.6)-h/2.7),(w,h-row*(h/21.6)-h/2.7))
            pygame.draw.line(screen, (0,0,0), (w/9.6,h-row*(h/21.6)-h/1.8),(w,h-row*(h/21.6)-h/1.8))
            pygame.draw.line(screen, (0,0,0), (0,h-row*(h/21.6)-h/1.8),(w/12.8,h-row*(h/21.6)-h/1.8))
            pygame.draw.line(screen, (0,0,0), (0,h-row*(h/21.6)-h/1.35),(w-w/9.6,h-row*(h/21.6)-h/1.35))
            pygame.draw.line(screen, (0,0,0), (w-w/12.8,h-row*(h/21.6)-h/1.35),(w,h-row*(h/21.6)-h/1.35))
        for col in range(COLS):
            pygame.draw.line(screen, (0,0,0), (w/9.6+col*(w/37.9),h-w/12.8),(w/9.6+col*(w/37.9),h))
            pygame.draw.line(screen, (0,0,0), (w/9.6+col*(w/37.945),h-h/3.086),(w/9.6+col*(w/37.945),h-h/5.4))
            pygame.draw.line(screen, (0,0,0), (w/9.6+col*(w/37.9),h-h/1.964),(w/9.6+col*(w/37.9),h-h/2.7))
            pygame.draw.line(screen, (0,0,0), (w/9.6+col*(w/37.945),h-h/1.44),(w/9.6+col*(w/37.945),h-h/1.8))
            pygame.draw.line(screen, (0,0,0), (w/9.6+col*(w/37.9),h-h/1.137),(w/9.6+col*(w/37.9),h-h/1.35))
        for col in range(COLS-27):
            pygame.draw.line(screen, (0,0,0), (w-w/12.8+col*(w/37.945),h/13.5),(w-w/12.8+col*(w/37.945),h))
            pygame.draw.line(screen, (0,0,0), (col*(w/38.2),h/8.308),(col*(w/38.2),h))
        pos = pygame.mouse.get_pos()
        t1.draw()
        t2.draw()
        t3.draw()
        t4.draw()
        t5.draw()
        t6.draw()
        t7.draw()
        t8.draw()
        t9.draw()
        t10.draw()
        t11.draw()
        t12.draw()
        t13.draw()
        t14.draw()
        t15.draw()
        t16.draw()
        t17.draw()
        t18.draw()
        t19.draw()
        if tutorial:
            pygame.draw.rect(screen, (255,255,255), (w/2-125,7.5,250,25))
            tt19.blit()
        if cant_place:
            screen.blit(cant_place_txt, (w/2-cp_width/2,10))
            c+=1
            if c==120:
                cant_place = False
                c=0

    elif shop:
        buy1.blit()
        buy2.blit()
        buy3.blit()
        if tutorial:
            if step == 6:
                pygame.draw.rect(screen, (255,255,255), (97,47,106,106), 3)
                pygame.draw.rect(screen, (255,255,255), (200,91,23,17), 2)
                pygame.draw.rect(screen, (255,255,255), (397,47,106,106), 3)
                pygame.draw.rect(screen, (255,255,255), (500,91,23,17), 2)
                pygame.draw.rect(screen, (255,255,255), (697,47,106,106), 3)
                pygame.draw.rect(screen, (255,255,255), (800,91,23,17), 2)
                pygame.draw.rect(screen, (255,255,255), (312.5, 400, 275, 25))
                pygame.draw.line(screen, (255,255,255), (450, 400), (150,150), 3)
                pygame.draw.line(screen, (255,255,255), (450, 400), (450,150), 3)
                pygame.draw.line(screen, (255,255,255), (450, 400), (750,150), 3)
                pygame.draw.rect(screen, (255,255,255), (337.5, 450, 225, 25))
                tt11.blit()
                continue_txt.blit()
            if step == 7:
                pygame.draw.rect(screen, (0,125,0), (80,163.33,140,30))
                pygame.draw.rect(screen, (255,255,255), (80,163.33,140,30), 3)
                pygame.draw.rect(screen, (0,125,0), (380,163.33,140,30))
                pygame.draw.rect(screen, (255,255,255), (380,163.33,140,30), 3)
                pygame.draw.rect(screen, (0,125,0), (677,163.33,146,30))
                pygame.draw.rect(screen, (255,255,255), (677,163.33,146,30), 3)
                pygame.draw.rect(screen, (255,255,255), (337.5, 450, 225, 25))
                pygame.draw.rect(screen, (255,255,255), (312.5, 400, 275, 25))
                pygame.draw.line(screen, (255,255,255), (450, 400), (150,193.33), 3)
                pygame.draw.line(screen, (255,255,255), (450, 400), (450,193.33), 3)
                pygame.draw.line(screen, (255,255,255), (450, 400), (750,193.33), 3)
                continue_txt.blit()
                tt12.blit()
            if step == 8:
                pygame.draw.rect(screen, (0,125,0), (55,190,187.5,105))
                pygame.draw.rect(screen, (255,255,255), (55,190,187.5,105),3)
                pygame.draw.rect(screen, (0,125,0), (355,190,187.5,105))
                pygame.draw.rect(screen, (255,255,255), (355,190,187.5,105),3)
                pygame.draw.rect(screen, (0,125,0), (647,190,205,105))
                pygame.draw.rect(screen, (255,255,255), (647,190,205,105),3)
                pygame.draw.rect(screen, (255,255,255), (337.5, 450, 225, 25))
                pygame.draw.rect(screen, (255,255,255), (362.5, 400, 175, 25))
                pygame.draw.line(screen, (255,255,255), (450, 400), (151.75,295), 3)
                pygame.draw.line(screen, (255,255,255), (450, 400), (451.75,295), 3)
                pygame.draw.line(screen, (255,255,255), (450, 400), (749.5,295), 3)
                pygame.draw.rect(screen, (255,255,255), (875,190,250,20))
                pygame.draw.rect(screen, (255,255,255), (875,215,225,20))
                pygame.draw.rect(screen, (255,255,255), (875,240,362.5,20))
                pygame.draw.rect(screen, (255,255,255), (875,265,250,20))
                pygame.draw.rect(screen, (255,255,255), (670,190,160,27),2)
                pygame.draw.rect(screen, (255,255,255), (650,218,199,24),2)
                pygame.draw.rect(screen, (255,255,255), (662.5,243,174,24),2)
                pygame.draw.rect(screen, (255,255,255), (685,268,130,23),2)
                pygame.draw.line(screen, (255,255,255), (875, 200), (830,203.5), 2)
                pygame.draw.line(screen, (255,255,255), (875, 225), (849,230), 2)
                pygame.draw.line(screen, (255,255,255), (875, 250), (836.5,255), 2)
                pygame.draw.line(screen, (255,255,255), (875, 275), (815,279.5), 2)
                continue_txt.blit()
                tt13.blit()
                tt14.blit()
                tt15.blit()
                tt16.blit()
                tt17.blit()
            if step == 9:
                pygame.draw.rect(screen, (255,255,255), (97,297,106,46), 3)
                pygame.draw.rect(screen, (255,255,255), (75,400,150,25))
                pygame.draw.line(screen, (255,255,255), (150,400), (150, 343), 3)
                tt18.blit()
            if step == 11:
                pygame.draw.rect(screen, (255,255,255), (397,297,106,46), 3)
                pygame.draw.rect(screen, (255,255,255), (375,400,150,25))
                pygame.draw.line(screen, (255,255,255), (450,400), (450, 343), 3)
                tt18.blit()
        back_button.blit()
        basic.blit()
        fast.blit()
        sniper.blit()
        if no_gold == True:
            screen.blit(no_gold_txt, (w/2-no_gold_width/2,10))
            b+=1
            if b==120:
                b=0
                no_gold = False

    elif monster_page:
        back_button.blit()
        if wave == 0:
            tt28.blit()
        if wave >= 1:
            basic_info.blit()
        if wave >= 4:
            tough_info.blit()
        if wave >= 5:
            boss1_info.blit()
        if wave >= 7:
            fast_info.blit()
        if wave >= 10:
            boss2_info.blit()

    elif encounter:
        if wave == 1:
            Encounter1.blit()
        if wave == 4:
            Encounter2.blit()
        if wave == 5:
            Encounter3.blit()
        if wave == 7:
            Encounter4.blit()
        if wave == 10:
            Encounter5.blit()

    elif research:
        back_button.blit()
        tt29.blit()
        tt30.blit()
        tt31.blit()
        tt32.blit()
        tt33.blit()
        tt34.blit()
        tt35.blit()
        tt36.blit()
        screen.blit(tt38, (500,355))
        screen.blit(tt39, (500,555))
        screen.blit(tt40, (500,155))
        B_Button1.blit()
        B_Button2.blit()
        B_Button3.blit()
        if show_R1:
            R_Button1.blit()
        if show_R2:
            R_Button2.blit()
        if show_R3:
            R_Button3.blit()

    elif settings:
        tt37.blit()
        S_Button1.blit()
        back_button.blit()

    else:
        if tutorial:
            if step == 14:
                if defend:
                    step += 1

            elif step == 15:
                screen.fill((0,125,0))
                if wave_click == True and monsters == []:
                    step += 1
                
        draw_path()
        pygame.draw.rect(screen, (150,150,150), (0,0,w,h/21.6))
        base.hp_bar()
        wave_button.blit()
        shop_button.blit()
        monster_button.blit()
        research_button.blit()
        settings_button.blit()
        screen.blit(gold_txt, (w/1.92,h/108))
        screen.blit(xp_txt, (w/1.6,h/108))
        screen.blit(wave_txt, (w/1.371,h/108))
        for i in towers:
            i.blit()
            if defend:
                if monsters == []:
                    defend = False
                else:
                    i.shoot()

        if defend:
            for monster in monsters:
                hit, hp_txt = monster.blit()
                if hit:
                    monsters.remove(monster)
                    hit = False
                elif monster.hp <= 0:
                    gold += monster.gold_drop
                    xp += monster.xp_drop
                    score += monster.kill_score
                    gold_txt = font.render("Gold -- " + str(gold), True, (0,0,0))
                    xp_txt = font.render("XP -- " + str(math.floor(xp)), True, (0,0,0))
                    monsters.remove(monster)

        if base.hp <= 0:
            game_over = True

        if wave == 12 and monsters == [] and game_over == False:
            d += 1
            if d == 120:
                score += base.hp*10
                score += gold*2
                score += xp*20
                demo_complete = True
                score_txt = font2.render("Your score -- " + str(round(score)), True, (0,255,0))
                score_width = score_txt.get_width()
                d=0

        if upgrade != None:
            upgrade.blit()

        if tutorial:
            if step == 1:
                pygame.draw.rect(screen, (255,255,255), (w-225, 12.5, 200, 25), 3)
                pygame.draw.rect(screen, (255,255,255), (w-304, 12.5, 75, 25), 3)
                pygame.draw.rect(screen, (255,255,255), (w-450, 100, 250, 25))
                pygame.draw.rect(screen, (255,255,255), (w-175, 100, 150, 25))
                pygame.draw.rect(screen, (255,255,255), (w-312.5, 165, 225, 25))
                pygame.draw.line(screen, (255,255,255), (w-325,100), (w-275,37.5),3)
                pygame.draw.line(screen, (255,255,255), (w-100,100), (w-125,37.5),3)
                tt1.blit()
                tt2.blit()
                continue_txt.blit()
            if step == 2:
                pygame.draw.rect(screen, (255,255,255), (0,50,100,80), 3)
                pygame.draw.rect(screen, (255,255,255), (0,150,200,35))
                pygame.draw.line(screen, (255,255,255), (100, 150), (50, 130), 3)
                pygame.draw.rect(screen, (255,255,255), (0,200,225,25))
                tt3.blit()
                tt4.blit()
                continue_txt.blit()
            if step == 3:
                pygame.draw.rect(screen, (255,255,255), (990,7.5,112.5,25), 3)
                pygame.draw.rect(screen, (255,255,255), (950,50,192.5,25))
                pygame.draw.rect(screen, (255,255,255), (933.75,85,225,25))
                tt5.blit()
                pygame.draw.line(screen, (255,255,255), (1046.25, 50), (1046.25, 32.5), 3)
                continue_txt.blit()
            if step == 4:
                pygame.draw.rect(screen, (255,255,255), (1190,7.5,112.5,25), 3)
                pygame.draw.rect(screen, (255,255,255), (1150,50,192.5,25))
                pygame.draw.rect(screen, (255,255,255), (1133.75,85,225,25))
                pygame.draw.line(screen, (255,255,255), (1246.25, 50), (1246.25, 32.5), 3)
                tt6.blit()
                continue_txt.blit()
            if step == 5:
                pygame.draw.rect(screen, (255,255,255), (150,5,100,40), 3)
                pygame.draw.rect(screen, (255,255,255), (100,85,200,65))
                pygame.draw.line(screen, (255,255,255), (200, 85), (200, 45), 3)
                tt7.blit()
                tt8.blit()
                tt9.blit()
                tt10.blit()
            if step == 10:
                pygame.draw.rect(screen, (255,255,255), (150,5,100,40), 3)
                pygame.draw.rect(screen, (255,255,255), (162.5,85,75,25))
                pygame.draw.line(screen, (255,255,255), (200,85), (200,45), 3)
                tt20.blit()
            if step == 12:
                step = 14
            if step == 14:
                pygame.draw.rect(screen, (255,255,255), (22,2,106,46), 3)
                pygame.draw.rect(screen, (255,255,255), (0,100,300,100))
                pygame.draw.line(screen, (255,255,255), (150, 100), (75, 48), 3)
                tt23.blit()
                tt24.blit()
                tt25.blit()
                tt26.blit()
                tt27.blit()
            elif step == 16:
                pygame.draw.rect(screen, (255,255,255), (w/2-500, h/2-235, 1000, 70))
                pygame.draw.rect(screen, (255,255,255), (w/2-200, h/2-15, 400, 30))
                tt21.blit()
                tt22.blit()

        if no_gold1 == True:
            screen.blit(no_gold_txt, (w/2-no_gold_width/2,10))
            b+=1
            if b==120:
                b=0
                no_gold1 = False

    if wave == 12 and monsters == [] and game_over == False:
        shop = False
        wave = 12

    clock.tick(60)
    pygame.display.update()
# end
