import pygame
from pygame.locals import *
import math
import random

pygame.init()

def dist(p1, p2):
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

def tupleToVector2(p):
    return pygame.Vector2(p[0], p[1])

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, mass, radius):
        super(Ball, self).__init__()
        
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.offset = pygame.Vector2(radius, radius)

        self.radius = radius
        self.mass = mass

        self.image = pygame.Surface((radius * 2, radius * 2), flags=SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        pygame.draw.circle(self.image, (255, 0, 0), (radius, radius), radius)
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        
        self.clicked = False
    
    def update(self):
        self.pos += self.vel
        self.rect.update(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)
    
    def setPos(self, pos):
        self.pos = pos
        self.rect.update(pos.x - self.radius, pos.y - self.radius, self.radius * 2, self.radius * 2)
    
    def stop(self):
        self.vel = pygame.Vector2(0, 0)

width, height = 800, 800
window = pygame.display.set_mode((width, height))
balls = pygame.sprite.Group()

star = Ball(400, 400, 10000, 50)
planet1 = Ball(600, 400, 100, 10)
planet2 = Ball(200, 400, 1000, 25)
planet1.vel = (random.randint(-10, 10), random.randint(-10, 10))
planet2.vel = (random.randint(-10, 10), random.randint(-10, 10))
balls.add(star, planet1)

clock = pygame.time.Clock()
paused = False
past_pos = pygame.Vector2(0, 0)

gravity = 1

game_on = True
while game_on:
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            game_on = False
        elif event.type == MOUSEBUTTONDOWN:
            paused = True
            for ball in balls:
                if dist(ball.pos, tupleToVector2(event.pos)) < ball.radius:
                    ball.clicked = True
                    ball.pos = tupleToVector2(event.pos)
                    ball.stop()
        elif event.type == MOUSEBUTTONUP:
            paused = False
            for ball in balls:
                ball.clicked = False
        elif event.type == MOUSEMOTION:
            ball_clicked = False
            for ball in balls:
                if ball.clicked:
                    ball_clicked = True
                    ball.setPos(tupleToVector2(event.pos))
            if paused and not ball_clicked:
                for ball in balls:
                    ball.setPos(ball.pos + tupleToVector2(event.pos) - past_pos)
            past_pos = tupleToVector2(event.pos)
    
    if not paused:
        for center in balls:
            for satellite in balls:
                radius = dist(center.pos, satellite.pos)
                if abs(radius) < center.radius: continue
                mag = gravity * center.mass / radius ** 2
                dir = center.pos - satellite.pos
                dir.scale_to_length(mag)
                satellite.vel += dir
        balls.update()

    balls.draw(window)
    pygame.display.update()
    clock.tick(100)