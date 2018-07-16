# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 13:45:08 2017

@author: Admin
"""

import pygame
import random
import math
import os

WIDTH=660
HEIGHT=680
FPS=60

#define colors
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

#set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

font_name = pygame.font.match_font('arial')
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_lives(surface, x, y):
    img_rect = live_img.get_rect()
    live_img.set_colorkey(WHITE)
    img_rect.center = (x,y)
    surface.blit(live_img, img_rect)  
 
#classes  
    
#player    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT-60)
        self.speedx = 0
        self.lives = 3
        
    def update(self,dt):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -400
        if keystate[pygame.K_RIGHT]:
            self.speedx = 400
        self.rect.x += self.speedx * dt
        if self.rect.right >= WIDTH-20:
            self.rect.right = WIDTH-20
        if self.rect.left <= 29:
            self.rect.left = 29
#brick        
class Brick(pygame.sprite.Sprite):
    def __init__(self,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = brick_images[color]
        self.rect = self.image.get_rect()
        self.rect.center = (50,50)
        
class Pow(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pow_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = center
        self.speedy = 5
    def update(self,dt):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
        
        
#ball        
class Ball(pygame.sprite.Sprite):
    def __init__(self,player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = ball_img
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        #pygame.draw.circle(self.image, BLACK, self.rect.center, self.radius)
        self.rect.center = (WIDTH/2,HEIGHT-(HEIGHT-player.rect.top)-(self.rect.height/2 + 3))
        self.speedx = 0
        self.speedy = 0
        self.speed = 300
        self.times = 0 #ile odbic z bonusem
    
    def vector(self,angle_degree):
        angle = math.radians(angle_degree)
        if angle_degree > 90:
            self.speedx = -math.ceil(  self.speed / (math.sqrt(math.tan(angle)**2 + 1))   )
            self.speedy = math.ceil(  self.speed*math.tan(angle) / (math.sqrt(math.tan(angle)**2 + 1))  )
        else:
            self.speedx = math.ceil(  self.speed / (math.sqrt(math.tan(angle)**2 + 1))   )
            self.speedy = -math.ceil(  self.speed*math.tan(angle) / (math.sqrt(math.tan(angle)**2 + 1))  )
        
    def bounce(self):
        #walls bounce
        if self.rect.left < 29:
            self.speedx = abs(self.speedx)
        if self.rect.right > WIDTH-24:
            self.speedx = -abs(self.speedx)
        
        #ceiling bounce
        if self.rect.top < 61:
            self.speedy = abs(self.speedy)
            
        #pad bounce
        if self.rect.bottom >= HEIGHT-(HEIGHT-player.rect.top) and self.rect.bottom <= HEIGHT-(HEIGHT-player.rect.bottom):
            if self.rect.center[0] <= player.rect.right+3 and self.rect.center[0] >= player.rect.left-6:
                if self.rect.center[0] <= player.rect.left+8:
                    self.vector(155)
                elif self.rect.center[0] <= player.rect.left+18:
                    self.vector(138)
                elif self.rect.center[0] <= player.rect.left+34:
                    self.vector(117)
                elif self.rect.center[0] <= player.rect.left+51:
                    self.vector(112)
            #right half
                elif self.rect.center[0] < player.rect.left+68:
                    self.vector(78)
                elif self.rect.center[0] < player.rect.left+81:
                    self.vector(57)
                elif self.rect.center[0] < player.rect.left+97:
                    self.vector(42)
                else:
                    self.vector(25)
                if self.speed < 600:
                    self.speed += 10
                if self.times > 0:
                    self.times -=1
    
        
    def reset(self):
        self.rect.center = (WIDTH/2,HEIGHT-88)
        self.speed = 300
        self.speedx = 0
        self.speedy = 0
            
    def death(self):
        if self.rect.bottom >= HEIGHT:
            player.lives -= 1
            position = player.rect.center
            player.image = player_img
            player.image.set_colorkey(WHITE)
            player.rect = player.image.get_rect()
            player.rect.center = position
            self.reset()            
           
            
    def  update(self,dt):
        #start ball movement
        keystate = pygame.key.get_pressed()
        if self.speedx==0 and self.speedy==0:
            ball.rect.x = player.rect.center[0] - ball.rect.width/2
            if keystate[pygame.K_SPACE]:
                self.vector(66)
        
        #ball bounce
        self.bounce()
        
        self.rect.centerx += self.speedx * dt
        self.rect.centery += self.speedy * dt
        
        #reset
        self.death()
                

                  
#initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Arkanoid")
clock = pygame.time.Clock()

def game_start_screen():
    screen.fill(BLACK)
    draw_text(screen,"Arkanoid",40,WIDTH/2,HEIGHT/2-50)
    draw_text(screen,"poruszaj się strzałkami, spacja - start piłki", 22, WIDTH/2,  HEIGHT/2)
    draw_text(screen,"naciśnij dowolny klawisz aby zacząć", 16, WIDTH/2,  HEIGHT/2+40)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def game_over_screen(score):
    screen.fill(BLACK)
    draw_text(screen,"KONIEC GRY", 50, WIDTH/2,  HEIGHT/2-20)
    draw_text(screen,"twój wynik to "+str(score), 26, WIDTH/2,  HEIGHT/2+40)
    draw_text(screen,"naciśnij spację aby zagrać jeszcze raz", 12, WIDTH/2,  HEIGHT/2+80)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    waiting = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

def next_level_screen():
    screen.fill(BLACK)
    draw_text(screen,"KOLEJNY POZIOM", 30, WIDTH/2,  HEIGHT/2)
    draw_text(screen,"naciśnij spację aby kontynuować", 16, WIDTH/2,  HEIGHT/2+40)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    waiting = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

                
#load game graphics
background = pygame.image.load(os.path.join(img_folder, "background.png")).convert() 
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, "pad.png")).convert()
player2_img = pygame.image.load(os.path.join(img_folder, "pad2.png")).convert()
ball_img = pygame.image.load(os.path.join(img_folder, "ball.png")).convert()
live_img = pygame.image.load(os.path.join(img_folder, "live.png")).convert()
pow_img = pygame.image.load(os.path.join(img_folder, "powerup.png")).convert()
brick_images = []
brick_list = ["brick_red.png","brick_yellow.png","brick_blue.png","brick_brown.png",
              "brick_dgreen.png","brick_green.png","brick_orange.png","brick_gray.png",
              "brick_ice.png","brick_lgreen.png","brick_pink.png","brick_steel.png",
              "brick_violet.png"]
for img in brick_list:
    brick_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

def add_brick(color,x,y):
    br = Brick(color)
    br.rect.center = (x,y)
    all_sprites.add(br)
    bricks.add(br)

    
def first_level():
    #bricks
    for a in range(0,7):
        for i in range(a,13-a):
            if i==a or i==12-a:
                for j in range(a,13-a):
                    add_brick(a,94+40*j,100+20*i)
            else:
                for k in range(a,13-a,12-2*a):
                    add_brick(a,94+40*k,100+20*i)

def second_level():
    #bricks
    for a in range(0,7):
        for i in range(a,13-a):
            if i==a or i==12-a:
                for j in range(a,13-a):
                    add_brick(a,94+40*j,100+20*i)
              
    
#game loop
game_start = True
game_over = False
next_level = False
running = True
while running:
    if game_over:
        game_over_screen(score)
        game_over = False
    if game_start:
        game_start_screen()
        game_start = False
        #creating sprites
        all_sprites = pygame.sprite.Group()
        player = Player()
        ball = Ball(player)
        bricks = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        all_sprites.add(player)
        all_sprites.add(ball)
        level = 1
        #score
        score = 0
        first_level()
        
    if len(bricks) == 0:
        next_level = True
    
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_q] and keystate[pygame.K_r]:
        all_sprites.remove(bricks)
        pygame.sprite.Group.empty(bricks)    
        
        
    if next_level:
        next_level = False
        next_level_screen()
        ball.reset()
        second_level()
    #keep loop running at the right speed
    dt = clock.tick(FPS) / 1000 #time to draw one frame (in seconds)
    
    #events
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
    if player.lives < 0:
        game_over = True
        game_start = True
    
    if ball.times==0:
        position = player.rect.center
        player.image = player_img
        player.image.set_colorkey(WHITE)
        player.rect = player.image.get_rect()
        player.rect.center = position
        
    #update
    all_sprites.update(dt)
            
    #check if ball hit a brick
    hits = pygame.sprite.spritecollide(ball,bricks,True,pygame.sprite.collide_circle)
    if hits:
        score += 50            
        if (ball.rect.center[1] <= hits[0].rect.bottom and ball.rect.center[1] >= hits[0].rect.top):
            ball.speedx = -ball.speedx
        else:
            ball.speedy = -ball.speedy
        if random.random() > 0.9:
            pow = Pow(hits[0].rect.center)
            powerups.add(pow)
            all_sprites.add(pow)
            
    #check if player catches powerup
    catch = pygame.sprite.spritecollide(player,powerups,True)
    if catch:
        ball.times = 5 #ile razy mozna odbic z bonusem
        score += 100
        position = player.rect.center
        player.image = player2_img
        player.image.set_colorkey(WHITE)
        player.rect = player.image.get_rect()
        player.rect.center = position
    
    #render/draw
    screen.fill(BLUE)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "wynik: "+str(score), 18, 50, 10)
    for l in range(0,player.lives):
        draw_lives(screen, 50+30*l,HEIGHT-20)
    
    #after drawing everything flip the display
    pygame.display.flip()
    
pygame.quit()
print(len(bricks))