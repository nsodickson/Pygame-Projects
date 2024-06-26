import pygame
from pygame.locals import *
import random

pygame.init()


def map_range(in_min, in_max, out_min, out_max, val):
    in_range = in_max - in_min
    out_range = out_max - out_min
    return (val - in_min) * out_range / in_range + out_min


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super(Bird, self).__init__()

        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.w = w
        self.h = h

        self.base_image = pygame.image.load("Assets/flappy.png")
        self.base_image = pygame.transform.scale(self.base_image, (w, h))
        self.image = self.base_image.copy()
        self.rect = pygame.Rect(x, y, w, h)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.pos += self.vel
        self.rect.update(self.pos.x, self.pos.y, self.w, self.h)
        clamped_vel = pygame.math.clamp(self.vel.y, 0, 2)
        self.image = pygame.transform.rotate(self.base_image, map_range(0, 2, 20, -45, clamped_vel))
        self.mask = pygame.mask.from_surface(self.image)
    
    def draw(self, window):
        window.blit(self.image, self.pos)


class TopPipe(pygame.sprite.Sprite):
    def __init__(self, x, y, h):
        super(TopPipe, self).__init__()

        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(-speed, 0)
        self.h = h

        pipe_base = pygame.image.load("Assets/pipe-base-top.png")
        pipe_top = pygame.image.load("Assets/pipe-top.png")
        scale = 80 / pipe_top.get_width()
        pipe_top = pygame.transform.scale_by(pipe_top, scale)
        pipe_base = pygame.transform.scale(pipe_base, (80, h - pipe_top.get_height()))
        self.image = pygame.Surface((80, h), flags=SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        self.image.blit(pipe_base, (0, 0))
        self.image.blit(pipe_top, (0, pipe_base.get_height()))
        self.rect = pygame.Rect(x, y, 80, h)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.pos += self.vel
        self.rect.update(self.pos.x, self.pos.y, 80, self.h)


class BottomPipe(pygame.sprite.Sprite):
    def __init__(self, x, y, h):
        super(BottomPipe, self).__init__()

        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(-speed, 0)
        self.h = h

        pipe_base = pygame.image.load("Assets/pipe-base-bottom.png")
        pipe_bottom = pygame.image.load("Assets/pipe-bottom.png")
        scale = 80 / pipe_bottom.get_width()
        pipe_bottom = pygame.transform.scale_by(pipe_bottom, scale)
        pipe_base = pygame.transform.scale(pipe_base, (80, h - pipe_bottom.get_height()))
        self.image = pygame.Surface((80, h), flags=SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        self.image.blit(pipe_bottom, (0, 0))
        self.image.blit(pipe_base, (0, pipe_bottom.get_height()))
        self.rect = pygame.Rect(x, y, 80, h)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.pos += self.vel
        self.rect.update(self.pos.x, self.pos.y, 80, self.h)

width, height = 1200, 800
window = pygame.display.set_mode((width, height))
bg_img = pygame.image.load("Assets/flappy-bg.jpeg")
bg_img = pygame.transform.scale(bg_img, (width, height))
bg_x = 0

font_big = pygame.font.Font(None, 80)
font_med = pygame.font.Font(None, 60)
clock = pygame.time.Clock()
pipe_delay = 2
fps = 500
speed = 0.5
gravity = 0.01
max_score = 0

def run():
    global max_score
    global bg_x

    score = 0
    ticks = 0
    bird = Bird(200, 400, 50, 30)
    pipes = pygame.sprite.Group()

    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird.vel.y = -1
        
        if ticks / fps % pipe_delay == 0:
            h = random.randint(200, 600)
            pipes.add(TopPipe(1200, 0, h), BottomPipe(1200, h + 100, height - h - 100))

        bird.vel.y += gravity
        bird.update()
        pipes.update()

        if bird.pos.y + bird.h > height:
            game_on = False
        elif bird.pos.y + bird.h / 2 < 0:
            game_on = False
        
        for pipe in pipes:
            if pygame.sprite.collide_mask(bird, pipe) is not None:
                game_on = False
            elif isinstance(pipe, BottomPipe) and pipe.pos.x + 40 == bird.pos.x:
                score += 1
                if score > max_score:
                    max_score = score

        for pipe in pipes:
            if pipe.pos.x + 80 < 0:
                pipes.remove(pipe)

        bg_x = (bg_x - speed * 1.1) % width
        window.blit(bg_img, (bg_x, 0))
        window.blit(bg_img, (bg_x - width, 0))
        bird.draw(window)
        pipes.draw(window)
        font_surf = font_big.render(str(score), True, (255, 0, 0))
        window.blit(font_surf, (25, 25))
        pygame.display.update()
        clock.tick(fps)
        ticks += 1

run()

restart = font_big.render("Click to Restart", True, (255, 0, 0))
restart_size = font_big.size("Click to Restart")
restart_pos = (width / 2 - restart_size[0] / 2, height / 2 - restart_size[1] / 2)
restart_rect = pygame.Rect(restart_pos[0], restart_pos[1], restart_size[0], restart_size[1])
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            if restart_rect.collidepoint(event.pos):
                run()
    
    highscore = font_med.render("Highest: {}".format(max_score), True, (255, 0, 0))
    highscore_size = font_med.size("Highest: {}".format(max_score))
    highscore_pos = (width / 2 - highscore_size[0] / 2, restart_pos[1] + restart_size[1] + 5)
    window.blit(highscore, highscore_pos)
    window.blit(restart, restart_pos)
    pygame.display.update()
    
