import pygame
import random
import os
Height = 600
Width = 500
FPS = 60
# 初始化＆建立視窗&音效
pygame.init()
pygame.mixer.init()                                 # 音效初始化
screen = pygame.display.set_mode((Width, Height))  # input 長寬畫面長寬(tuple)
pygame.display.set_caption('pygame practice~~~')
# 載入圖片
background_img = pygame.image.load(os.path.join("img", "background.jpg")).convert()      # 轉換成py可讀取的格式
player_img = pygame.transform.scale(pygame.image.load(os.path.join("img", "player.png")).convert(), (95, 75))
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
# bullet = pygame.image.load(os.path.join("img", "bullet_dog.jpeg")).convert()
# bullet_img = pygame.transform.scale(bullet, (70, 70))
# bullet_img.set_colorkey('white')
player_mini_img = pygame.transform.scale(player_img, (25, 19))
pygame.display.set_icon(player_mini_img)
player_mini_img.set_colorkey('black')
rocks_img = []
for i in range(7):
    rocks_img.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())

# 載入爆炸特效(store by dic)&死亡音效
explode = {'big': [], 'small': [], 'player': []}
for i in range(9):
    explode_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    player_explode_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    explode_img.set_colorkey('black')
    player_explode_img.set_colorkey('black')
    explode['big'].append(pygame.transform.scale(explode_img, (75, 75)))
    explode['small'].append(pygame.transform.scale(explode_img, (30, 30)))
    explode['player'].append(player_explode_img)

# 載入寶物圖片&音效
power_gun = pygame.image.load(os.path.join("img", 'power_gun.png')).convert()
power_gun_min = pygame.transform.scale(power_gun, (19, 30))
# power_gun_min.set_colorkey('black')
power_img = {'shield': pygame.image.load(os.path.join("img", 'shield.png')).convert(),
             'gun': pygame.image.load(os.path.join("img", 'gun.png')).convert(),
             'power_gun': power_gun_min
             }
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
power_gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
# 載入音效
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
explode_sound = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))  # 設定背景音樂
pygame.mixer.music.set_volume(0.4)                                # 設定背景音量
# 分數字體
# font_name = pygame.font.match_font('Al Nile', True)                     # 找字體花太久時間
font_name = os.path.join("font.ttf")       # 找字體花太久時間


def draw_life(sur, hp, x, y):
    if hp < 0:
        hp = 0
    bar_length = 100
    bar_height = 10
    fill = (hp/100) * bar_length
    out_line_rect = pygame.Rect(x, y, bar_length, bar_height)    # 畫外框
    fill_rect = pygame.Rect(x, y, fill, bar_height)              # 畫血條
    if hp >= 50:
        pygame.draw.rect(sur, 'green', fill_rect)
    elif 10 <= hp < 50:
        pygame.draw.rect(sur, 'orange', fill_rect)
    else:
        pygame.draw.rect(sur, 'red', fill_rect)
    pygame.draw.rect(sur, 'white', out_line_rect, 2)             # 第四個參數為指定像素


def new_rock():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))                # true-反鋸齒
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def draw_live_remaining(sur, life_remaining, img, x, y):
    for num in range(life_remaining):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * num
        img_rect.y = y
        sur.blit(img, img_rect)


def draw_init():
    screen.blit(background_img, (0, 0))  # 要放上的圖,(x,y)
    draw_text(screen, '隕石遊戲', 64, Width / 2, Height / 4)
    draw_text(screen, 'WASD上下左右移動飛船 空白鍵發射子彈~', 22, Width / 2, Height / 2)
    draw_text(screen, '按任意鍵開始遊戲!', 18, Width / 2, Height * 3 / 4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event_ in pygame.event.get():  # 取得所有事件
            if event_.type == pygame.QUIT:
                pygame.quit()
                return True
            # 當按下空白鍵，發射子彈
            elif event_.type == pygame.KEYUP:
                waiting = False
                return False


class Player(pygame.sprite.Sprite):                             # 繼承Sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey('black')                        # 把指定顏色變成透明
        self.rect = self.image.get_rect()                       # 產生圖片的定位框
        self.radius = 20                                       # 產生碰撞判斷的圓
        # pygame.draw.circle(self.image, 'red', self.rect.center, self.radius)
        self.rect.centerx = Width/2
        self.rect.bottom = Height - 10
        self.health = 100
        self.life = 3
        self.hidden = False
        self.hide_time = 0
        self.gun_level = 1
        self.gun_time = 0
        self.move_speed = 5

    def update(self):
        key_pressed = pygame.key.get_pressed()      # 回傳boolean
        now = pygame.time.get_ticks()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.move_speed
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.move_speed
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.move_speed
        if key_pressed[pygame.K_s]:
            self.rect.y += self.move_speed
        if self.rect.right > Width:
            self.rect.right = Width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > Height:
            self.rect.bottom = Height
        # 延緩死亡後出現的時間
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = Width / 2
            self.rect.bottom = Height - 10
        if self.gun_level > 1 and now - self.gun_time > 5000:
            self.gun_level -= 1
            self.gun_time = now

    def shoot(self):
        if not self.hidden:
            if self.gun_level == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                bullets.add(bullet)
                all_sprites.add(bullet)
                shoot_sound.play()
            elif self.gun_level >= 2:
                bullet_1 = Bullet(self.rect.left, self.rect.centery)
                bullet_2 = Bullet(self.rect.right, self.rect.centery)
                bullets.add(bullet_1)
                all_sprites.add(bullet_1)
                bullets.add(bullet_2)
                all_sprites.add(bullet_2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (Width/2, Height + 500)

    def gun_up(self):
        self.gun_level += 1
        self.gun_time = pygame.time.get_ticks()


class Rock(pygame.sprite.Sprite):                 # 繼承Sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rocks_img)
        self.image_ori.set_colorkey('black')
        self.image = self.image_ori.copy()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()           # 產生圖片的定位框
        self.radius = int(self.rect.width * 0.85 / 2)  # 產生碰撞判斷的圓
        # pygame.draw.circle(self.image, 'red', self.rect.center, self.radius)
        self.rect.x = random.randrange(0, Width - self.rect.width)
        self.rect.bottom = random.randrange(-180, -100)
        self.speed_x = random.randrange(-3, 3)
        self.speed_y = random.randrange(2, 10)
        self.total_rot_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > Height or self.rect.left > Width or self.rect.right < 0:
            self.rect.x = random.randrange(0, Width - self.rect.width)
            self.rect.bottom = random.randrange(-100, -40)
            self.speed_x = random.randrange(-3, 3)
            self.speed_y = random.randrange(2, 10)

    def rotate(self):
        # 每次對原本的rock轉動
        self.total_rot_degree += self.rot_degree
        self.total_rot_degree = self.total_rot_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_rot_degree)
        center = self.rect.center                   # 把原本的center記下來
        self.rect = self.image.get_rect()           # 得到轉動後的img的rect
        self.rect.center = center


class Bullet(pygame.sprite.Sprite):                 # 繼承Sprite
    def __init__(self, x, y):                           # 傳入位置
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()           # 產生圖片的定位框
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top < 0:
            self.kill()                            # sprite內建，檢查所有sprite群組是否有該物件並刪除


class Explosion(pygame.sprite.Sprite):                 # 繼承Sprite
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explode[self.size][0]
        self.rect = self.image.get_rect()               # 得到外框資訊
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()      # 從初始化到現在所經過的時間
        self.frame_rate = 50                            # 經過時間ms

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explode[self.size]):
                self.kill()
            else:
                self.image = explode[self.size][self.frame]
                center = self.rect.center
                # self.rect = self.image.get_rect()
                self.rect.center = center


class Power(pygame.sprite.Sprite):                 # 繼承Sprite
    """
    center: 傳入生成掉落物的位置
    """
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        # 定義掉落物種類
        self.type = random.choice(['shield', 'gun', 'power_gun'])
        self.image = power_img[self.type]
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()               # 得到外框資訊
        self.rect.center = center
        self.speed_y = 3

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > Height:
            self.kill()


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
# 石頭sprite group
rocks = pygame.sprite.Group()
# 子彈sprite group
bullets = pygame.sprite.Group()
# 掉落物sprite group
powers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
game_score = 0
# 產生Rock
for i in range(15):
    new_rock()
pygame.mixer.music.play(-1)                 # -1代表重複播放背景音樂
# 遊戲迴圈
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        game_score = 0
        for i in range(15):
            new_rock()
    clock.tick(FPS)                                         # 設定每秒更新畫畫面
    # 取得輸入
    for event in pygame.event.get():                         # 取得所有事件
        if event.type == pygame.QUIT:
            running = False
        # 當按下空白鍵，發射子彈
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # 更新畫面
    all_sprites.update()                                            # 把群組的東西全部畫到xxx上並使用update()更新
    # 當石頭和子彈碰撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)   # 後兩個參數為是否刪除該物件，並回傳該兩碰撞物件 by dict
    for hit in hits:                                                # 當群組裡有物件碰撞時，進行刪除，並加入新的rock
        random.choice(explode_sound).play()
        expl = Explosion(hit.rect.center, 'big')
        all_sprites.add(expl)
        game_score += hit.radius
        # 設定碰撞後掉落物
        if random.random() > 0.5:
            power = Power(hit.rect.center)
            all_sprites.add(power)
            powers.add(power)
        new_rock()
    # 當飛船和石頭碰
    touches = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)    # 改成以圓形判斷碰撞
    for touch in touches:
        player.health -= touch.radius
        exp1_small = Explosion(touch.rect.center, 'small')
        all_sprites.add(exp1_small)
        new_rock()
        if player.health <= 0:
            die = Explosion(player.rect.center, 'player')
            all_sprites.add(die)
            die_sound.play()
            player.life -= 1
            player.health = 100
            player.hide()
    # 當寶物和飛船碰撞
    power_player = pygame.sprite.spritecollide(player, powers, True)    # 回傳player和power by list
    for power in power_player:
        if power.type == 'shield':
            shield_sound.play()
            player.health += 20
            if player.health >= 100:
                player.health = 100
        elif power.type == 'gun':
            gun_sound.play()
            player.gun_up()
        elif power.type == 'power_gun':
            # player.power_gun()
            if player.life < 3:
                player.life += 1

    if player.life == 0 and not die.alive():        # 動畫完全結束才終止遊戲
        show_init = True
    # 畫面顯示
    screen.fill('black')
    screen.blit(background_img, (0, 0))                      # 要放上的圖,(x,y)
    all_sprites.draw(screen)
    draw_life(screen, player.health, 5, 15)                 # 設定生命值條
    draw_text(screen, str(game_score), 18, Width/2, 10)     # 設定分數
    draw_live_remaining(screen, player.life, player_mini_img, Width-100, 15)        # 設定剩餘命數
    pygame.display.update()                                 # 透過class的update()更新畫面
pygame.quit()

