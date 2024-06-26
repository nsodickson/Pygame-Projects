import pygame
from pygame.locals import *
import random
import math

pygame.init()

# Grid
width = 800
height = 800
grid_w = 25
grid_h = 25
square_w = width / grid_w
square_h = height / grid_h
bg_color = (0, 0, 0)
window = pygame.display.set_mode((width, height))

# Time and Events
clock = pygame.time.Clock()
fps = 300
event_list = []

# Fonts
font = pygame.font.Font(None, 80)

# Snake
snake = [[2, 12],
         [3, 12],
         [4, 12]]
head = [5, 12]
dirs = ["RIGHT", "RIGHT", "RIGHT"]
dir = "RIGHT"
snake_color = (50, 50, 200)
head_color = (150, 25, 250)
offset = 0
buffer = 0.3

# Food
food = [random.randint(0, grid_w - 1), random.randint(0, grid_h - 1)]
food_color = (200, 75, 10)
score = 0

game_on = True
while game_on:
    window.fill(bg_color)

    # Event Handling
    event_list += pygame.event.get()
    for event in event_list:
        if event.type == QUIT:
            game_on = False
    if offset < 1e-6:
        for event in event_list:
            if event.type == KEYDOWN:
                if event.key == K_w and dir != "DOWN" and dirs[-1] != "DOWN":
                    dir = "UP"
                    event_list.pop(0)
                elif event.key == K_a and dir != "RIGHT" and dirs[-1] != "RIGHT":
                    dir = "LEFT"
                if event.key == K_s and dir != "UP" and dirs[-1] != "UP":
                    dir = "DOWN"
                    event_list.pop(0)
                if event.key == K_d and dir != "LEFT" and dirs[-1] != "LEFT":
                    dir = "RIGHT"
                    event_list.pop(0)

    # Incrementing Offset
    offset = (offset + 1) % square_w

    # Moving Snake
    if offset < 1e-6:
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

    # Food Collisions
    ate = False
    if dir == "RIGHT":
        if head[1] == food[1] and math.ceil(head[0] - buffer + offset / square_w) == food[0]:
            ate = True
    elif dir == "UP":
        if head[0] == food[0] and math.floor(head[1] + buffer - offset / square_h) == food[1]:
            ate = True
    elif dir == "LEFT":
        if head[1] == food[1] and math.floor(head[0] + buffer - offset / square_w) == food[0]:
            ate = True
    elif dir == "DOWN":
        if head[0] == food[0] and math.ceil(head[1] - buffer + offset / square_h) == food[1]:
            ate = True
    if ate:
        score += 1
        overlaps = True
        while overlaps:
            food = [random.randint(0, grid_w - 1), random.randint(0, grid_h - 1)]
            overlaps = False
            for body in snake + [head]:
                if body == food:
                    overlaps = True
        dx = snake[1][0] - snake[0][0]
        dy = snake[1][1] - snake[0][1]
        new = [snake[0][0] - dx, snake[0][1] - dy]
        snake.insert(0, new)
        dirs.insert(0, dirs[0])
    
    # Body Collisions
    for body in snake:
        if dir == "RIGHT":
            if head[1] == body[1] and math.ceil(head[0] + offset / square_w) == body[0]:
                game_on = False
        elif dir == "UP":
            if head[0] == body[0] and math.floor(head[1] - offset / square_h) == body[1]:
                game_on = False
        elif dir == "LEFT":
            if head[1] == body[1] and math.floor(head[0] - offset / square_w) == body[0]:
                game_on = False
        elif dir == "DOWN":
            if head[0] == body[0] and math.ceil(head[1] + offset / square_h) == body[1]:
                game_on = False
    
    # Wall Collisions
    if dir == "RIGHT":
        if math.ceil(head[0] - buffer + offset / square_w) >= grid_w:
            game_on = False
    elif dir == "UP":
        if math.ceil(head[1] + buffer - offset / square_h) <= 0:
            game_on = False
    elif dir == "LEFT":
        if math.ceil(head[0] + buffer - offset / square_w) <= 0:
            game_on = False
    elif dir == "DOWN":
        if math.ceil(head[1] - buffer + offset / square_h) >= grid_h:
            game_on = False

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
    
    # Drawing lines between body parts
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
    
    # Drawing Head
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
    
    # Drawing Score
    score_surf = font.render(str(score), True, (255, 0, 0))
    window.blit(score_surf, (15, 15))

    pygame.display.update()
    clock.tick(fps + min(score * 2, 100))