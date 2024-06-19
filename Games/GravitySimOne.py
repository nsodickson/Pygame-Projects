import pygame
from pygame.locals import *
import math

pygame.init()

def dist(p1, p2):
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

def tupleToVector2(p):
    return pygame.Vector2(p[0], p[1])

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super(Ball, self).__init__()
        
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.offset = pygame.Vector2(radius, radius)
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(self.image, (255, 0, 0), (radius, radius), radius)
        self.rect = pygame.Rect(x + radius, y + radius, radius * 2, radius * 2)
    
    def draw(self, window):
        window.blit(self.image, self.pos - self.offset)
    
    def update(self):
        self.pos += self.vel
        self.rect.update(self.pos.x, self.pos.y, self.radius * 2, self.radius * 2)
    
    def stop(self):
        self.vel = pygame.Vector2(0, 0)

width, height = 800, 800
window = pygame.display.set_mode((width, height))
ball = Ball(400, 400, 50)

clock = pygame.time.Clock()
ticks = 0
mouse_down = False
pos_history = []
tick_history = []
cutoff = 8

gravity = 0.025
friction = 0.01
x_damping = 0.8
y_damping = 0.8

game_on = True
while game_on:
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            game_on = False
        elif event.type == MOUSEBUTTONDOWN:
            if dist(ball.pos, tupleToVector2(event.pos)) < ball.radius:
                mouse_down = True
                ball.pos = tupleToVector2(event.pos)
                ball.stop()
        elif event.type == MOUSEBUTTONUP:
            if mouse_down:
                x_vel = (pos_history[-1].x - pos_history[-cutoff].x) / cutoff
                y_vel = (pos_history[-1].y - pos_history[-cutoff].y) / cutoff
                ball.vel = pygame.Vector2(x_vel, y_vel)
            mouse_down = False
        elif event.type == MOUSEMOTION:
            if mouse_down:
                ball.pos = tupleToVector2(event.pos)
    
    pos_history.append(tupleToVector2(pygame.mouse.get_pos()))
    if len(pos_history) > cutoff:
        pos_history.pop(0)

    if not mouse_down:
        ball.vel.y += gravity
        if abs(ball.vel.x) > 0 and ball.pos.y + ball.radius == height:
            ball.vel.x = ball.vel.x / abs(ball.vel.x) * max(0, abs(ball.vel.x) - friction)
        ball.update()
        
        if ball.pos.y + ball.radius >= height:
            ball.vel.y *= -1 * y_damping
            ball.pos.y = height - ball.radius
        if ball.pos.y - ball.radius <= 0:
            ball.vel.y *= -1 * y_damping
            ball.pos.y = ball.radius
        if ball.pos.x + ball.radius >= width:
            ball.vel.x *= -1 * x_damping
            ball.pos.x = width - ball.radius
        if ball.pos.x - ball.radius <= 0:
            ball.vel.x *= -1 * x_damping
            ball.pos.x = ball.radius

    ball.draw(window)
    pygame.display.update()
    clock.tick(500)
    ticks += 1