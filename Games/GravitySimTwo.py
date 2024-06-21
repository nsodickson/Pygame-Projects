import pygame
from pygame.locals import *
import math
import random
import time

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
    
    def setPos(self, pos):
        self.pos = pos
        self.rect.update(pos.x - self.radius, pos.y - self.radius, self.radius * 2, self.radius * 2)
    
    def setRadius(self, radius):
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), flags=SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        pygame.draw.circle(self.image, (255, 0, 0), (radius, radius), radius)
        self.rect = pygame.Rect(self.pos.x - radius, self.pos.y - radius, radius * 2, radius * 2)
    
    def setMass(self, mass):
        self.mass = mass
    
    def update(self):
        self.pos += self.vel
        self.rect.update(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)
    
    def stop(self):
        self.vel = pygame.Vector2(0, 0)


def handleMerges():
    global balls
    centers = sorted(balls.sprites(), key=lambda x: -x.mass)
    satellites = sorted(balls.sprites(), key=lambda x: -x.mass)
    i = 0
    while i < len(centers):
        n = i + 1
        while n < len(satellites):
            center = centers[i]
            satellite = satellites[n]
            radius = dist(center.pos, satellite.pos)
            if radius < center.radius + satellite.radius:
                center.setMass(center.mass + satellite.mass)
                center.setRadius(math.sqrt(center.radius ** 2 + satellite.radius ** 2))
                center.vel = (center.mass * center.vel + satellite.mass * satellite.vel) / (center.mass + satellite.mass)
                balls.remove(satellite)
                satellites.remove(satellite)
                centers.remove(satellite)
            n += 1
        i += 1

def handleGravity():
    centers = balls.sprites()
    satellites = balls.sprites()
    for i in range(len(centers)):
        for n in range(i + 1, len(satellites)):
            center = centers[i]
            satellite = satellites[n]
            radius = dist(center.pos, satellite.pos)
            
            mag1 = G * center.mass / radius ** 2
            dir1 = center.pos - satellite.pos
            dir1.scale_to_length(mag1)
            satellite.vel += dir1
            satellite.vel.scale_to_length(min(C, satellite.vel.magnitude()))

            mag2 = G * satellite.mass / radius ** 2
            dir2 = satellite.pos - center.pos
            dir2.scale_to_length(mag2)
            center.vel += dir2
            center.vel.scale_to_length(min(C, center.vel.magnitude()))

width, height = 800, 800
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 100
paused = False
click_frame = False
gravity_on = True
past_pos = pygame.Vector2(0, 0)

G = 1
C = 100000000

balls = pygame.sprite.Group()

star = Ball(400, 400, 10000, 50)
randomness = 0
planets = []
for i in range(250):
    r = random.random() * (width / 2 - star.radius) + star.radius
    theta = random.random() * 2 * math.pi
    planet = Ball(r * math.cos(theta) + width / 2, r * math.sin(theta) + height / 2, 1, 1)
    vel = (planet.pos - star.pos).rotate(90)
    vel.scale_to_length(min(C, math.sqrt(G * star.mass / dist(planet.pos, star.pos)) + random.randint(-randomness, randomness)))
    planet.vel = vel
    planets.append(planet)

balls.add(star, *planets)

merge_times = []
gravity_times = []

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
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                fps = 25
            elif event.key == K_RIGHT:
                fps = 500
            elif event.key == K_SPACE:
                gravity_on = not gravity_on
            elif event.key == K_RETURN:
                if paused:
                    click_frame = True
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                fps = 100
    
    if not paused or click_frame:
        start = time.perf_counter()
        handleMerges()
        merge_times.append(time.perf_counter() - start)

        if gravity_on:
            start = time.perf_counter()
            handleGravity()
            gravity_times.append(time.perf_counter() - start)
            
        balls.update()
        click_frame = False

    # Drawing the Schwarzschild Radius of the star
    # pygame.draw.circle(window, (50, 50, 50, 0.5), star.pos, 2 * G * star.mass / C ** 2, width=5)

    balls.draw(window)
    pygame.display.update()
    clock.tick(fps)

print("Average Merge Time: {}".format(sum(merge_times) / len(merge_times)))
print("Average Gravity Time: {}".format(sum(gravity_times) / len(gravity_times)))