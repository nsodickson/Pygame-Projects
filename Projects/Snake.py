import pygame
from pygame.locals import *
import random

# Creatng the window and the grid
pygame.init()

# Adjust width and height as needed for computer display
w, h = 600, 600
grid_w, grid_h = 50, 50
size_w, size_h = w // grid_w, h // grid_h
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont(None, 25)

# Creating the snake
head = [25, 25]
snake = [[24, 25], [23, 25], [22, 25]]
direction = "RIGHT"
speed = 0

# Creating the food and the score
food = [random.randint(0, grid_w - 1), random.randint(0, grid_h - 1)]
score = 0

gameOn = True
gameOver = False
while gameOn:
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
        elif event.type == KEYDOWN:
            if event.key == K_w and direction != "DOWN":
                direction = "UP"
                break
            if event.key == K_a and direction != "RIGHT":
                direction = "LEFT"
                break
            if event.key == K_s and direction != "UP":
                direction = "DOWN"
                break
            if event.key == K_d and direction != "LEFT":
                direction = "RIGHT"
                break

    for i in range(grid_w):
        for n in range(grid_h):
            if (i + n) % 2 == 0:
                pygame.draw.rect(screen, (125, 195, 145), (n * size_w, i * size_h, size_w, size_h))
            else:
                pygame.draw.rect(screen, (90, 195, 100), (n * size_w, i * size_h, size_w, size_h))

    snake.insert(0, [head[0], head[1]])
    snake.pop(-1)

    if direction == "UP":
        head[1] -= 1
    elif direction == "LEFT":
        head[0] -= 1
    elif direction == "DOWN":
        head[1] += 1
    elif direction == "RIGHT":
        head[0] += 1

    # Drawing the head before the rest of the body
    pygame.draw.rect(screen, (0, 0, 255), (head[0] * size_w, head[1] * size_h, size_w, size_h))
    for i in snake:
        if head == i:
            gameOn = False
            gameOver = True
        pygame.draw.rect(screen, (0, 0, 255), (i[0] * size_w, i[1] * size_h, size_w, size_h))

    if head[0] < 0 or head[0] > grid_w - 1 or head[1] < 0 or head[1] > grid_h - 1:
        gameOn = False
        gameOver = True

    if head == food:
        score += 1
        speed += 1
        food = [random.randint(0, grid_w - 1), random.randint(0, grid_h - 1)]
        end = snake[-1]
        snake.append([end[0], end[1]])

    pygame.draw.rect(screen, (255, 0, 0), (food[0] * size_w, food[1] * size_h, size_w, size_h))

    score_surf = font.render(f"Score: {score}", False, (255, 0, 0))
    screen.blit(score_surf, (5, 5))

    pygame.display.flip()
    
    pygame.time.wait(max(50, 80 - 2 * score))

while gameOver:
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOver = False
    font = pygame.font.SysFont(None, 100, (255, 0, 0))
    game_over = font.render("Game Over", False, (255, 0, 0))
    size = font.size("Game Over")
    screen.blit(game_over, (w / 2 - size[0] / 2, h / 2 - size[1] / 2))
    pygame.display.flip()
