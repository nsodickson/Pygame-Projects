import pygame
from pygame.locals import *
import random
import math

def sign(x):
    return x / abs(x)

def tupleToVector2(p):
    return pygame.Vector2(p[0], p[1])

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pygame.init()

# Simulation parameters
g = pygame.Vector2(0, 0.01)
dt = 1
fps = 300
clock = pygame.time.Clock()
font = pygame.font.Font(size=25)
width = 800
height = 800
window = pygame.display.set_mode((width, 
                                  height))

# Initializing circlular border
border_radius = width / 2 - 50
border_center = pygame.Vector2(width / 2, height / 2)
border_click_radius = 5

num_balls = 25
colors = [RED for i in range(num_balls)]
radii = [2 for i in range(num_balls)]
positions = []
velocities = []

# Square
"""
assert math.isqrt(num_balls) ** 2 == num_balls  # Assert there is a square number of balls
for i in range(num_balls):
    grid_length = math.isqrt(num_balls)
    length = 4 * radii[0] * grid_length
    row = i // grid_length 
    col = i % grid_length
    positions.append(pygame.Vector2(border_center.x - length // 2 + length * row / grid_length + 1e-10,
                                    border_center.y - length // 2 + length * col / grid_length + 1e-10))
    velocities.append(pygame.Vector2(0, 0))
"""

# Small deviations
# """
r = math.sqrt(random.random()) * border_radius - 2
theta = random.random() * 2 * math.pi
random_pos = pygame.Vector2(r * math.cos(theta) + border_center.x,
                            r * math.sin(theta) + border_center.y)
for i in range(num_balls):
    positions.append(random_pos + pygame.Vector2(random.random() * 0.1,
                                                 random.random() * 0.1))
    velocities.append(pygame.Vector2(0, 0))
# """

# Random positions
"""
for i in range(num_balls):
    r = math.sqrt(random.random()) * border_radius - radii[i]
    theta = random.random() * 2 * math.pi
    positions.append(pygame.Vector2(r * math.cos(theta) + border_center.x,
                                    r * math.sin(theta) + border_center.y))
    velocities.append(pygame.Vector2(0, 0))
"""

paused = False
click_frames = 0
base_fps = fps
fast_fps = 1000
slow_fps = 100
past_pos = tupleToVector2(pygame.mouse.get_pos())
clicked_idx = None
border_clicked = False
damping = 1.0
radius_damping = 1.0

game_on = True
while game_on:
    window.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            game_on = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                paused = not paused
            elif event.key == K_RETURN and paused:
                click_frames = 10
            elif event.key == K_RIGHT:
                fps = fast_fps
            elif event.key == K_LEFT:
                fps = slow_fps
            elif event.key == K_DOWN:
                border_radius = max(10, border_radius - 10)
            elif event.key == K_UP:
                border_radius += 10
        elif event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_LEFT:
                fps = base_fps
        elif event.type == MOUSEBUTTONDOWN:
            event_pos = tupleToVector2(event.pos)
            if (event_pos - border_center).magnitude() < border_click_radius:
                border_clicked = True
            if not border_clicked:
                for i in range(num_balls):
                    if (event_pos - positions[i]).magnitude() < radii[i]:
                        clicked_idx = i
                        velocities[i] = pygame.Vector2(0, 0)
                        break
        elif event.type == MOUSEMOTION:
            event_pos = tupleToVector2(event.pos)
            if border_clicked:
                border_center += event_pos - past_pos
            elif clicked_idx is not None:
                positions[clicked_idx] += event_pos - past_pos
            past_pos = event_pos
        elif event.type == MOUSEBUTTONUP:
            border_clicked = False
            clicked_idx = None
    
    if not paused or click_frames > 0:
        for i in range(num_balls):
            if i != clicked_idx:
                velocities[i] += g * dt / 2
                positions[i] += velocities[i] * dt + 0.5 * g * dt ** 2
                velocities[i] += g * dt / 2

        for i in range(num_balls):
            if (positions[i] - border_center).magnitude() + radii[i] >= border_radius:
                # Update velocity
                border_pos = positions[i] - border_center  # Position relative to the border center
                border_x = border_pos.x * border_radius / border_pos.magnitude()  # x pos of collision relative to the border center
                border_y = sign(border_pos.y) * math.sqrt(border_radius ** 2 - border_x ** 2) # y pos of collision relative to the border center
                norm_x = -1 * sign(border_pos.x) * math.sqrt(1 / (1 + border_y ** 2 / border_x ** 2))
                norm_y = border_y / border_x * norm_x
                norm = pygame.Vector2(norm_x, norm_y)
                velocities[i] = velocities[i] - 2 * (velocities[i] * norm) * norm * damping

                # Update radius
                radii[i] *= radius_damping

                # Update position
                angle = math.atan(-1 * border_pos.y / border_pos.x)  # Angle relative to border center
                positions[i] = pygame.Vector2(border_x + border_center.x - sign(border_pos.x) * radii[i] * abs(math.cos(angle)),
                                              border_y + border_center.y - sign(border_pos.y) * radii[i] * abs(math.sin(angle)))

        click_frames = max(click_frames - 1, 0)

    for i in range(num_balls):
        pygame.draw.circle(window, colors[i], positions[i], radii[i])
    pygame.draw.circle(window, GREEN, border_center, border_radius, 2)
    pygame.draw.circle(window, GREEN, border_center, border_click_radius)

    # Debug 
    for i in range(num_balls):
        # Update velocity
        border_pos = positions[i] - border_center  # Position relative to the border center
        border_x = border_pos.x * border_radius / border_pos.magnitude()  # x pos of collision relative to the border center
        border_y = sign(border_pos.y) * math.sqrt(border_radius ** 2 - border_x ** 2) # y pos of collision relative to the border center
        norm_x = -1 * sign(border_pos.x) * math.sqrt(1 / (1 + border_y ** 2 / border_x ** 2))
        norm_y = border_y / border_x * norm_x
        norm = pygame.Vector2(norm_x, norm_y)
        angle = math.atan(-1 * border_pos.y / border_pos.x)  # Angle relative to border center

        collision_point = pygame.Vector2(border_x + border_center.x, border_y + border_center.y)
        pygame.draw.circle(window, GREEN, collision_point, 5)
        pygame.draw.line(window, BLUE, collision_point, collision_point + norm * 10)
        pygame.draw.line(window, BLUE, positions[i], positions[i] + 10 * velocities[i])

        angle_img = font.render("Angle: {:.2f}".format(math.degrees(angle)), True, RED)
        x_img = font.render("Border X: {:.2f}".format(border_pos.x), True, RED)
        y_img = font.render("Border Y: {:.2f}".format(border_pos.y), True, RED)
        # window.blit(angle_img, (5, 5))
        # window.blit(x_img, (5, 25))
        # window.blit(y_img, (5, 45))

    pygame.display.update()
    clock.tick(fps)
