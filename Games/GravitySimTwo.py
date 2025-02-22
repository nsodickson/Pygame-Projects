import pygame
from pygame.locals import *
import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np

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
                center.vel = (center.mass * center.vel + satellite.mass * satellite.vel) / (center.mass + satellite.mass)
                center.setMass(center.mass + satellite.mass)
                center.setRadius(math.sqrt(center.radius ** 2 + satellite.radius ** 2))
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
            if radius > center.radius:
                mag = G * center.mass * satellite.mass / radius ** 2

                dir1 = center.pos - satellite.pos
                dir1.scale_to_length(mag / satellite.mass)
                satellite.vel += dir1
                if satellite.vel.magnitude() > C:
                    satellite.vel.scale_to_length(C)

                dir2 = satellite.pos - center.pos
                dir2.scale_to_length(mag / center.mass)
                center.vel += dir2
                if center.vel.magnitude() > C:
                    center.vel.scale_to_length(C)

# Window and Clock Setup
width, height = 800, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Simulation 2")
clock = pygame.time.Clock()
fps = 100
past_pos = pygame.Vector2(0, 0)

# Flags
paused = False
clicked = False
click_frame = False
gravity_on = True
merge_on = True
trails = False
plot_diagnostics = False

# Constants
G = 1
C = 1e20

balls = pygame.sprite.Group()

star = Ball(400, 400, 10000, 50)
planets = []
for i in range(999):
    r = math.sqrt(random.random()) * (width / 2 - star.radius) + star.radius
    theta = random.random() * 2 * math.pi
    planet = Ball(r * math.cos(theta) + width / 2, r * math.sin(theta) + height / 2, 1, 1)
    vel = (planet.pos - star.pos).rotate(90)
    vel.scale_to_length(math.sqrt(G * star.mass / dist(planet.pos, star.pos)) + random.randint(-2, 2))
    # vel.scale_to_length(random.random() * math.sqrt(G * star.mass / dist(planet.pos, star.pos)))
    # vel.scale_to_length(random.random() * 5)
    if vel.magnitude() > C:
        vel.scale_to_length(C)
    planet.vel = vel
    planets.append(planet)

balls.add(star, *planets)

ticks = 0
particle_nums = []
merge_times = []
gravity_times = []

pygame.display.set_caption("N-Body Simulation (Diagnostics {})".format("On" if plot_diagnostics else "Off"))
game_on = True
while game_on:
    if not trails:
        window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            game_on = False
        elif event.type == MOUSEBUTTONDOWN:
            clicked = True
            for ball in balls:
                if dist(ball.pos, tupleToVector2(event.pos)) < ball.radius:
                    ball.clicked = True
        elif event.type == MOUSEBUTTONUP:
            clicked = False
            for ball in balls:
                ball.clicked = False
        elif event.type == MOUSEMOTION:
            ball_clicked = False
            for ball in balls:
                if ball.clicked:
                    ball_clicked = True
                    ball.setPos(tupleToVector2(event.pos))
            if clicked and not ball_clicked:
                for ball in balls:
                    ball.setPos(ball.pos + tupleToVector2(event.pos) - past_pos)
            past_pos = tupleToVector2(event.pos)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                fps = 25
            elif event.key == K_RIGHT:
                fps = 500
            elif event.key == K_g:
                gravity_on = not gravity_on
            elif event.key == K_t:
                trails = not trails
            elif event.key == K_d:
                plot_diagnostics = not plot_diagnostics
                pygame.display.set_caption("N-Body Simulation (Diagnostics {})".format("On" if plot_diagnostics else "Off"))
            elif event.key == K_m:
                merge_on = not merge_on
            elif event.key == K_RETURN:
                if paused:
                    click_frame = True
            elif event.key == K_SPACE:
                paused = not paused
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                fps = 100
    
    if not paused or click_frame:
        start = time.perf_counter()
        if merge_on:
            handleMerges()
        merge_times.append(time.perf_counter() - start)
        particle_nums.append(len(balls))

        start = time.perf_counter()
        if gravity_on:
            handleGravity()
        gravity_times.append(time.perf_counter() - start)
            
        for ball in balls:
            if ball.clicked:
                ball.stop()
            else:
                ball.update()
        click_frame = False
        ticks += 1

    # Drawing the Schwarzschild Radius of the star
    # pygame.draw.circle(window, (50, 50, 50, 0.5), star.pos, 2 * G * star.mass / C ** 2, width=5)

    balls.draw(window)
    pygame.display.update()
    clock.tick(fps)

    # For comparison to barnes-hut algorithm
    """
    if ticks > 100:
        game_on = False
    """

pygame.quit()

print("Average Merge Time: {}".format(sum(merge_times) / len(merge_times)))
print("Average Gravity Time: {}".format(sum(gravity_times) / len(gravity_times)))
if plot_diagnostics:
    particle_nums = np.array(particle_nums)
    merge_times = np.array(merge_times)
    gravity_times = np.array(gravity_times)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.set(figwidth=10, figheight=6)
    x = np.arange(0, ticks, 1)
    ax1.plot(x, merge_times * 1000, color="red", label="Merge Time")
    ax1.plot(x, gravity_times * 1000, color="blue", label="Gravity Time")
    ax1.set_yscale("log")
    ax1.set_xlabel("Ticks")
    ax1.set_ylabel("Time (MS)")
    ax1.legend()

    ax2.plot(particle_nums, merge_times * 1000, color="red", label="Merge Time")
    ax2.plot(particle_nums, gravity_times * 1000, color="blue", label="Gravity Time")
    ax2.set_xlabel("Number of Bodies")
    ax2.set_ylabel("Time (MS)")
    ax2.legend()

    fig.suptitle("Simulation Diagnostics ({} Bodies)".format(len(planets) + 1))
    fig.tight_layout()
    plt.show()