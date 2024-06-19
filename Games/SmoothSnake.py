import pygame
from pygame.locals import *
import random
import math

pygame.init()

width = 800
height = 800
grid_w = 25
grid_h = 25
square_w = width / grid_w
square_h = height / grid_h
bg_color = (0, 0, 0)

window = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
max_delay = 0
delay = max_delay
event_list = []

score = 0

snake = [[2, 12],
         [3, 12],
         [4, 12]]
head = [5, 12]
dirs = ["RIGHT", "RIGHT", "RIGHT"]
dir = "RIGHT"
snake_color = (50, 50, 200)
head_color = (150, 25, 250)
offset = 0

food = [random.randint(0, grid_w - 1), random.randint(0, grid_h - 1)]
food_color = (200, 75, 10)

game_on = True
while game_on:
    window.fill(bg_color)

    event_list += pygame.event.get()
    for event in event_list:
        if event.type == QUIT:
            game_on = False
    for event in event_list:
        if event.type == KEYDOWN:
            if delay > 0:
                delay -= 1
                break
            if event.key == K_w and dir != "DOWN":
                dir = "UP"
                event_list.pop(0)
                delay = max_delay
                break
            elif event.key == K_a and dir != "RIGHT":
                dir = "LEFT"
                event_list.pop(0)
                delay = max_delay
                break
            if event.key == K_s and dir != "UP":
                dir = "DOWN"
                event_list.pop(0)
                delay = max_delay
                break
            if event.key == K_d and dir != "LEFT":
                dir = "RIGHT"
                event_list.pop(0)
                delay = max_delay
                break

    offset = (offset + 1) % square_w

    if offset == 0:
        snake.append(head.copy())
        dirs.append(dir)
        if dir == "RIGHT":
            head[0] += 1
        elif dir == "UP":
            head[1] -= 1
        elif dir == "LEFT":
            head[0] -= 1
        elif dir == "DOWN":
            head[1] += 1
        snake.pop(0)
        dirs.pop(0)

    if head == food:
        score += 1
        food = [random.randint(0, grid_w - 1), random.randint(0, grid_h - 1)]
        dx = snake[1][0] - snake[0][0]
        dy = snake[1][1] - snake[0][1]
        new = [snake[0][0] - dx, snake[0][1] - dy]
        snake.insert(0, new)
        dirs.insert(0, dirs[0])

    # Drawing Screen
    for i in range(grid_w):
        for n in range(grid_h):
            if (i + n) % 2 == 0:
                pygame.draw.rect(window, (125, 195, 145), (n * square_w, i * square_h, square_w, square_h))
            else:
                pygame.draw.rect(window, (90, 195, 100), (n * square_w, i * square_h, square_w, square_h))

    # Drawing Snake
    for body_dir, body in zip(dirs, snake):
        if body_dir == "RIGHT":
            pygame.draw.rect(window, snake_color, (body[0] * square_w + offset, body[1] * square_h, square_w, square_h), border_radius=8)
        elif body_dir == "UP":
            pygame.draw.rect(window, snake_color, (body[0] * square_w, body[1] * square_h - offset, square_w, square_h), border_radius=8)
        elif body_dir == "LEFT":
            pygame.draw.rect(window, snake_color, (body[0] * square_w - offset, body[1] * square_h, square_w, square_h), border_radius=8)
        elif body_dir == "DOWN":
            pygame.draw.rect(window, snake_color, (body[0] * square_w, body[1] * square_h + offset, square_w, square_h), border_radius=8)
    
    """
    full_snake = snake + [head]
    full_dirs = dirs + [dir]
    for idx in range(len(full_snake) - 1):
        if full_dirs[idx] == "RIGHT":
            start = (full_snake[idx][0] * square_w + square_w / 2 + offset, full_snake[idx][1] * square_h + square_h / 2)
        elif full_dirs[idx] == "UP":
            start = (full_snake[idx][0] * square_w + square_w / 2, full_snake[idx][1] * square_h + square_h / 2 - offset)
        elif full_dirs[idx] == "LEFT":
            start = (full_snake[idx][0] * square_w + square_w / 2 - offset, full_snake[idx][1] * square_h + square_h / 2)
        elif full_dirs[idx] == "DOWN":
            start = (full_snake[idx][0] * square_w + square_w / 2, full_snake[idx][1] * square_h + square_h / 2 + offset)
        
        if full_dirs[idx + 1] == "RIGHT":
            end = (full_snake[idx + 1][0] * square_w + square_w / 2 + offset, full_snake[idx + 1][1] * square_h + square_h / 2)
        elif full_dirs[idx + 1] == "UP":
            end = (full_snake[idx + 1][0] * square_w + square_w / 2, full_snake[idx + 1][1] * square_h + square_h / 2 - offset)
        elif full_dirs[idx + 1] == "LEFT":
            end = (full_snake[idx + 1][0] * square_w + square_w / 2 - offset, full_snake[idx + 1][1] * square_h + square_h / 2)
        elif full_dirs[idx + 1] == "DOWN":
            end = (full_snake[idx + 1][0] * square_w + square_w / 2, full_snake[idx + 1][1] * square_h + square_h / 2 + offset)
        
        pygame.draw.line(window, 
                         snake_color, 
                         start, 
                         end, 
                         int(square_w // 2 + 1))
    """
    
    if dir == "RIGHT":
        pygame.draw.rect(window, head_color, (head[0] * square_w + offset, head[1] * square_h, square_w, square_h), border_radius=8)
    elif dir == "UP":
        pygame.draw.rect(window, head_color, (head[0] * square_w, head[1] * square_h - offset, square_w, square_h), border_radius=8)
    elif dir == "LEFT":
        pygame.draw.rect(window, head_color, (head[0] * square_w - offset, head[1] * square_h, square_w, square_h), border_radius=8)
    elif dir == "DOWN":
        pygame.draw.rect(window, head_color, (head[0] * square_w, head[1] * square_h + offset, square_w, square_h), border_radius=8)
    
    # Drawing Food
    pygame.draw.rect(window, food_color, (food[0] * square_w, food[1] * square_h, square_w, square_h), border_radius=8)
    
    pygame.display.update()

    clock.tick(200)