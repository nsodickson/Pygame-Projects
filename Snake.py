import pygame
from pygame.locals import *
import random

pygame.init()
w, h = 750, 750
screen = pygame.display.set_mode((w, h))
fps = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)
speed = 0
size = w / 50
head = [w / 2, h / 2]
head_rect = pygame.Rect(head[0], head[1], size, size)
snake = [[w / 2, h / 2], [w / 2 + size * 1, h / 2], [w / 2 + size * 2, h / 2], [w / 2 + size * 3, h / 2]]
direction = [-size, 0]

# Directions
# [1, 0] --> Right
# [-1, 0] --> Left
# [0, 1] --> Down
# [0, -1] --> Up

score = 0
food = [random.randint(0, w) // size * size, random.randint(0, h) // size * size]
food_rect = pygame.Rect(food[0], food[1], size, size)

gameOn = True
while gameOn:
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
        elif event.type == KEYDOWN:
            if event.key == K_w and direction[1] == 0:  # If pressing w and direction isn't already up or down
                direction = [0, -size]
            if event.key == K_a and direction[0] == 0:  # If pressing a and direction isn't already right or left
                direction = [-size, 0]
            if event.key == K_s and direction[1] == 0:  # If pressing s and direction isn't already up or down
                direction = [0, size]
            if event.key == K_d and direction[0] == 0:  # If pressing d and direction isn't already right or left
                direction = [size, 0]
    screen.fill((0, 0, 0))

    head[0] += direction[0]
    head[1] += direction[1]
    head_rect = pygame.Rect(head[0], head[1], size, size)
    snake.insert(0, [head[0], head[1]])
    snake.pop(-1)

    # Drawing the head before the rest of the body
    pygame.draw.rect(screen, (0, 0, 255), head_rect)
    for i in snake[1:]:
        if head == i:
            gameOn = False
        pygame.draw.rect(screen, (0, 0, 255), (i[0], i[1], size, size))

    if head[0] < 0 or head[0] > w - size or head[1] < 0 or head[1] > h - size:
        gameOn = False

    if head_rect.colliderect(food_rect):
        score += 1
        speed += 1
        food = [random.randint(0, w) // size * size, random.randint(0, h) // size * size]
        food_rect = pygame.Rect(food[0], food[1], size, size)
        snake.append([snake[-1][0] - direction[0], snake[-1][1] - direction[1]])

    pygame.draw.rect(screen, (0, 255, 0), food_rect)

    score_surf = font.render(f"Score: {score}", False, (255, 0, 0))
    screen.blit(score_surf, (5, 5))

    pygame.display.flip()

    fps.tick(15 + speed//5)

gameOn = True
while gameOn:
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
    font = pygame.font.SysFont(None, 150, (255, 0, 0))
    game_over = font.render("Game Over", False, (255, 0, 0))
    size = font.size("Game Over")
    screen.blit(game_over, (w / 2 - size[0] / 2, h / 2 - size[1] / 2))
    pygame.display.flip()
