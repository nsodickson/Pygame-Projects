import pygame
from pygame.locals import *
import random

pygame.init()


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super(Bird, self).__init__()

        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.w = w
        self.h = h

        self.image = pygame.image.load("Assets/flappy.png")
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = pygame.Rect(x, y, w, h)
    
    def update(self):
        self.pos += self.vel
        self.rect.update(self.pos.x, self.pos.y, self.w, self.h)
    
    def draw(self, window):
        window.blit(self.image, self.pos)


class TopPipe(pygame.sprite.Sprite):
    def __init__(self, x, y, h):
        super(TopPipe, self).__init__()

        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(-0.5, 0)
        self.h = h

        self.image = pygame.image.load("Assets/pipe-top.png")
        self.image = pygame.transform.scale(self.image, (80, h))
        self.rect = pygame.Rect(x, y, 80, h)
    
    def update(self):
        self.pos += self.vel
        self.rect.update(self.pos.x, self.pos.y, 80, self.h)


class BottomPipe(pygame.sprite.Sprite):
    def __init__(self, x, y, h):
        super(BottomPipe, self).__init__()

        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(-0.5, 0)
        self.h = h

        self.image = pygame.image.load("Assets/pipe-bottom.png")
        self.image = pygame.transform.scale(self.image, (80, h))
        self.rect = pygame.Rect(x, y, 80, h)
    
    def update(self):
        self.pos += self.vel
        self.rect.update(self.pos.x, self.pos.y, 80, self.h)

    
width, height = 1200, 800
window = pygame.display.set_mode((width, height))
bg_color = (173, 216, 230)
bird = Bird(200, 400, 50, 30)
pipes = pygame.sprite.Group()

clock = pygame.time.Clock()
pipe_delay = 2
ticks = 0
fps = 500

gravity = 0.01

game_on = True
while game_on:
    window.fill(bg_color)
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.vel.y = -1
    
    if ticks / fps % pipe_delay == 0:
        h = random.randint(200, 600)
        pipes.add(TopPipe(1200, 0, h), BottomPipe(1200, h + 150, height - h - 150))

    bird.vel.y += gravity
    bird.update()
    pipes.update()

    if bird.pos.y + bird.h > height:
        game_on = False
    elif bird.pos.y < 0:
        game_on = False 
    
    for pipe in pipes:
        if pygame.sprite.collide_rect(bird, pipe):
            game_on = False

    for pipe in pipes:
        if pipe.pos.x + 80 < 0:
            pipes.remove(pipe)

    bird.draw(window)
    pipes.draw(window)
    pygame.display.update()
    clock.tick(fps)
    ticks += 1

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
