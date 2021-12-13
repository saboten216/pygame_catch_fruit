import pygame
import sys
import os
import random

FPS = 60
WIDTH = 650
HEIGHT = 750
BLACK = (0,0,0)
RED = (204,109,96)

'''
初始化
'''
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #畫面長寬
clock = pygame.time.Clock()
pygame.display.set_caption("仙仙接水果")#標題

'''
img
'''
background_img = pygame.image.load(os.path.join("img","background.jpg")).convert()
background_init_img = pygame.image.load(os.path.join("img","background_init.jpg")).convert()
cactus_img = pygame.image.load(os.path.join("img","1.png")).convert()
cactus_mini_img = pygame.image.load(os.path.join("img","1.png")).convert()
cactus_mini_img = pygame.transform.scale(cactus_img,(40,60))
cactus_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(cactus_mini_img)
boom_img = pygame.image.load(os.path.join("img","boom.png")).convert()
fruit_imgs = [] #載入多種水果
for i in range (1,5,1):
    fruit_imgs.append(pygame.image.load(os.path.join("img",f"fruit{i}.png")).convert())

'''
music
'''
fruit_sound = pygame.mixer.Sound(os.path.join("sound","fruit.mp3"))
boom_sound = pygame.mixer.Sound(os.path.join("sound","boom.mp3"))
pygame.mixer.music.load(os.path.join("sound","bgm.mp3"))
pygame.mixer.music.set_volume(0.2) #音量

'''
字體
'''
font_name = os.path.join("font.ttf")
def draw_text(surf ,text, size , x , y):
    font = pygame.font.Font(font_name , size) #文字物件
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y 
    surf.blit(text_surface , text_rect)
'''
生命
'''
def draw_lives(surf , lives , img , x , y ):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 45 * i #間格畫出
        img_rect.y = y 
        surf.blit(img,img_rect)
'''
初始畫面
''' 
def draw_init():
    screen.blit(background_init_img , (0,0))
    draw_text(screen , '仙仙接水果', 70 , WIDTH/2,HEIGHT/4)
    draw_text(screen , '方向鍵移動', 40 , WIDTH/2,355)
    draw_text(screen , '生命歸零 遊戲結束', 40 , WIDTH/2,HEIGHT/2+23)
    draw_text(screen , '按下任意鍵開始遊戲', 40 , WIDTH/2,HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get(): # 按叉叉關掉
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                waiting = False
'''
end 畫面
'''
def draw_end():
    screen.blit(background_img , (0,0))
    draw_text(screen , "score : " + str(score) , 70 , WIDTH/2,HEIGHT/4)
    draw_text(screen , '點擊螢幕回到初始畫面', 50 , WIDTH/2,HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get(): # 按叉叉關掉
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                draw_init()
                waiting = False

'''
物件
'''        
class Player(pygame.sprite.Sprite): #仙人掌player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image =  pygame.transform.scale(cactus_img,(70,100)) #設置圖片大小
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #image距形大小
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = WIDTH/2-35 #定位
        self.rect.y = HEIGHT/2+250
        self.speedx = 8
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
    def update(self):
        key_pressed = pygame.key.get_pressed() # return布林
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]: 
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2 
            self.rect.bottom = HEIGHT - 10
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2 , HEIGHT +500)

class Fruit(pygame.sprite.Sprite): #水果
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(fruit_imgs) #原本的圖片(未失真)
        self.image_ori =  pygame.transform.scale(self.image_ori,(40,40))#set size 40*40
        self.image_ori.set_colorkey(BLACK) #去黑色背 (png)
        self.image = self.image_ori.copy() #存轉動過後的圖片         
        self.rect = self.image.get_rect() #image 距形大小
        self.mask = pygame.mask.from_surface(self.image) #適用在去背圖片
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(3,8)
        self.speedx = random.randrange(-1,1)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)
        
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360 #轉超過一圈沒有意義
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree) #單純使用此函示會失真 所以需要用原本的圖片進行轉動
        center = self.rect.center
        self.rect = self.image.get_rect() #對轉動過後的圖片 重新定位
        self.rect.center = center
        
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0: #超出外框就重新
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-1,1)   

class Boom(pygame.sprite.Sprite): #貓咪炸彈
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = boom_img #原本的圖片(未失真)
        self.image_ori =  pygame.transform.scale(boom_img,(40,40))#set size 40*40
        self.image_ori.set_colorkey((0,0,0)) #去黑色背 (png)
        self.image = self.image_ori.copy() #存轉動過後的圖片         
        self.rect = self.image.get_rect() #image 距形大小
        self.mask = pygame.mask.from_surface(self.image) #適用在去背圖片
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-45)
        self.speedy = random.randrange(3,8)
        self.speedx = random.randrange(-1,1)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)
        
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360 #轉超過一圈沒有意義
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree) #單純使用此函示會失真 所以需要用原本的圖片進行轉動
        center = self.rect.center
        self.rect = self.image.get_rect() #對轉動過後的圖片 重新定位
        self.rect.center = center
        
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0: #超出外框就重新
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(5,10)
            self.speedx = random.randrange(-1,1)
              
all_sprites = pygame.sprite.Group()
fruits = pygame.sprite.Group() #水果群組 
player_hit = pygame.sprite.Group() #player_hit群組
booms = pygame.sprite.Group()
player = Player() #生成玩家
all_sprites.add(player) #在all_sprites群組新增player
player_hit.add(player) #在player_hit群組新增 player
for i in range  (10): #生成水果
    f = Fruit()
    all_sprites.add(f)
    fruits.add(f)
for i in range  (4): #生成炸彈
    b = Boom()
    all_sprites.add(b)
    booms.add(b)
    
score = 0

pygame.mixer.music.play(-1) #無限重複撥放

'''
loop
'''
show_init = True
show_end = False
while True :
    if show_end:
        draw_end()
        show_end = False
        show_init = True
    if show_init:
        draw_init()
        show_init = False
        all_sprites = pygame.sprite.Group()
        fruits = pygame.sprite.Group() #水果群組 
        player_hit = pygame.sprite.Group() #player_hit群組
        booms = pygame.sprite.Group()
        player = Player() #生成玩家
        all_sprites.add(player) #在all_sprites群組新增player
        player_hit.add(player) #在player_hit群組新增 player
        for i in range  (10): #生成水果
            f = Fruit()
            all_sprites.add(f)
            fruits.add(f)
        for i in range  (4): #生成炸彈
            b = Boom()
            all_sprites.add(b)
            booms.add(b)
        score = 0

    clock.tick(FPS)
    '''
    get input 
    '''
    for event in pygame.event.get(): # 按叉叉關掉
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
  
    '''
    update
    '''
    
    all_sprites.update() #更新all_sprites
    
    hits = pygame.sprite.groupcollide(player_hit, fruits ,False , True , pygame.sprite.collide_mask) #傳群組進去 回傳碰撞的字典 #mask>>真實碰撞
    for hit in hits:#碰到水果 就消失 並重生水果
        score += 7
        f = Fruit()
        all_sprites.add(f)
        fruits.add(f)
        fruit_sound.play()
    
    b_hits = pygame.sprite.groupcollide(player_hit, booms ,False , True , pygame.sprite.collide_mask) #傳群組進去 回傳碰撞的字典 #mask>>真實碰撞
    for hit in b_hits: #碰到炸彈 就消失 並重生炸彈
        score -= 5
        player.lives -= 1
        b = Boom()
        all_sprites.add(b)
        booms.add(b)
        player.hide()
        boom_sound.play()
    
    if player.lives == 0 :
        show_end = True
        
    '''
    畫面顯示
    '''
    # screen.fill((183, 183, 220))
    screen.blit(background_img , (0,0))
    all_sprites.draw(screen)
    draw_text(screen , "score : " + str(score) , 50 , WIDTH/2 , 10)
    draw_lives(screen , player.lives , cactus_mini_img , WIDTH-150 , 15 )
    pygame.display.update() #更新畫面
    
    
