import pygame
from pygame.locals import *
import random
import math

pygame.init()

def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)

width = 1000
height = 750
bg_color = (0, 0, 255)
window = pygame.display.set_mode((width, height))
window.fill(bg_color)
fps = pygame.time.Clock()

font_color = (0, 255, 0)
font_size = 75
font = pygame.font.Font(None, font_size)

color = (255, 0, 0)

# Adjust based on the machine
speed_init = 5

# Creating the ball
ball_size = 25
ball = pygame.Rect(width / 2, height / 2, ball_size, ball_size)
ball_dx = 0.7
ball_dy = 0.7
ball_dir_x = 1
ball_dir_y = 1
ball_speed = speed_init

paddle_speed = speed_init
paddle_width = 20
paddle_height = 100
collide_buffer = 0

# Creating the left paddle
left_score = 0
left = pygame.Rect(width / 6, height / 2, paddle_width, paddle_height)
left_dy = 0

# Creating the right paddle
right_score = 0
right = pygame.Rect(width * 5 / 6, height / 2, paddle_width, paddle_height)
right_dy = 0

gameOn = True

while gameOn:
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                right_dy = -paddle_speed
            elif event.key == K_DOWN:
                right_dy = paddle_speed
            elif event.key == K_w:
                left_dy = -paddle_speed
            elif event.key == K_s:
                left_dy = paddle_speed
        elif event.type == KEYUP:
            if event.key == K_UP:
                right_dy = 0
            elif event.key == K_DOWN:
                right_dy = 0
            elif event.key == K_w:
                left_dy = 0
            elif event.key == K_s:
                left_dy = 0
    window.fill(bg_color)

    ball.move_ip(ball_dx * ball_dir_x * ball_speed, ball_dy * ball_dir_y * ball_speed)
    left.move_ip(0, left_dy)
    left.clamp_ip(window.get_rect())
    right.move_ip(0, right_dy)
    right.clamp_ip(window.get_rect())

    # Prevents consecutive buggy collisions
    if collide_buffer > 0:
        collide_buffer -= 1

    # Collision detection with window edges
    if ball.y <= 0 or ball.y + ball_size >= height:
        ball_dir_y *= -1

    if ball.x <= 0:
        ball_dir_x *= -1
        right_score += 1
        ball.x = width/2
        ball.y = height/2
        ball_speed = speed_init

    elif ball.x - ball_size >= width:
        ball_dir_x *= -1
        left_score += 1
        ball.x = width/2
        ball.y = height/2
        ball_speed = speed_init

    if ball.colliderect(left) and collide_buffer == 0:
        ball_dir_x *= -1
        ball_speed = clamp(ball_speed + speed_init / 10, speed_init, speed_init * 1.5)
        ball_mid = ball.y + ball_size / 2
        paddle_mid = left.y + paddle_height / 2
        distance = clamp(abs(paddle_mid - ball_mid), paddle_height / 10, paddle_height / 3)
        angle = distance / (paddle_height / 2) * (math.pi / 2)
        ball_dx = math.cos(angle)
        ball_dy = math.sin(angle)
        collide_buffer = 100

    elif ball.colliderect(right) and collide_buffer == 0:
        ball_dir_x *= -1
        ball_speed = clamp(ball_speed + speed_init / 10, speed_init, speed_init * 1.5)
        ball_mid = ball.y + ball_size / 2
        paddle_mid = right.y + paddle_height / 2
        distance = clamp(abs(paddle_mid - ball_mid), paddle_height / 10, paddle_height / 3)
        angle = distance / (paddle_height / 2) * (math.pi / 2)
        ball_dx = math.cos(angle)
        ball_dy = math.sin(angle)
        collide_buffer = 100

    left_score_img = font.render(str(left_score), False, font_color)
    right_score_img = font.render(str(right_score), False, font_color)

    pygame.draw.rect(window, color, ball)
    pygame.draw.rect(window, color, left)
    pygame.draw.rect(window, color, right)
    window.blit(left_score_img, (width / 15, height / 10))
    window.blit(right_score_img, (14 * width / 15 - font_size, height / 10))

    fps.tick(100)

    pygame.display.update()
