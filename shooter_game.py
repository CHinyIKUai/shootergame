#Create your own shooter
from random import randint
from pygame import *

width = 700
height = 500
window = display.set_mode((width,height))
display.set_caption("Shooter Game!")

background = transform.scale(image.load("galaxy.jpg"),(width,height))

mixer.init()
mixer.music.load("Overtaken-One-Piece1.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx, self.rect.top,30,35,10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(80, width - 80)
            missed += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

game = True
finish = False
clock = time.Clock()
FPS = 60

score = 0
missed = 0
goal = 90
max_missed = 5 

YELLOW = (255, 226, 94)
RED = (255, 94, 94)
BLUE = (94, 124, 255)

font.init()
font_counter = font.Font("Raleway-Italic-VariableFont_wght.ttf",36)

font_win = font.Font("Raleway-VariableFont_wght.ttf",80)
win_text = font_win.render("YOU WIN!",True, YELLOW)
font_lose = font.Font("Raleway-Italic-VariableFont_wght.ttf",80)
lose_text = font_lose.render("YOU LOSE!",True, RED)
rocket = Player("cabbage.png", 5 , height - 100, 100, 100, 10)

ufos = sprite.Group()
for i in range(1,6):
    ufo = Enemy("AMONGUS.png", randint(80, width - 80), -40, 80, 80, randint(1,5))
    ufos.add(ufo)
while game:
    for e in event.get():
        if e.type == QUIT: 
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()

    if not finish:
        window.blit(background,(0,0))
        rocket.reset()
        rocket.update()
        ufos.draw(window)
        ufos.update()
        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(ufos, bullets, True , True)
        for c in collides:
            score += 1
            ufo = Enemy("AMONGUS.png", randint(80, width - 80), -40, 80, 80, randint(1,5))
            ufos.add(ufo)

        if sprite.spritecollide(rocket, ufos, False):
            finish = True
            window.blit(lose_text, (width//2 - lose_text.get_width() // 2, height // 2 - lose_text.get_height() // 2))
        
        if missed >= max_missed:
            finish = True
            window.blit(lose_text, (width//2 - lose_text.get_width() // 2, height // 2 - lose_text.get_height() // 2))

        if score >= goal:
            finish = True
            window.blit(win_text, (width//2 - win_text.get_width() // 2, height // 2 - win_text.get_height() // 2))

        text_counter = font_counter.render("Score:"+str(score),True,RED)
        window.blit(text_counter, (10,5))
        text_missed = font_counter.render("Missed:"+ str(missed),True,BLUE)
        window.blit(text_missed, (10,40))
    
    else:
        time.delay(3000)

        finish = False
        score = 0
        missed = 0

        for ufo in ufos:
            ufo.kill()
        for bullet in bullets:
            bullet.kill()

        for ufo in range(1, 6):
            ufo = Enemy("AMONGUS.png", randint(80, width - 80), -40, 80, 80, randint(1,5))
            ufos.add(ufo)

        rocket.rect.x = window.get_width() // 2 - rocket.rect.width // 2
        rocket.rect.y = height - 100

    display.update()
    clock.tick(FPS)

quit()