import pygame
from pygame.locals import *

pygame.init()

adjacent_cells = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

w, h = 800, 800
cell_size = 10
cells = [[0 for i in range(w // cell_size)] for n in range(h // cell_size)]
rects_to_update = []

screen = pygame.display.set_mode((w, h))
screen.fill((0, 0, 0))

clock = pygame.time.Clock()
timer = 100

def applyRules():
    global rects_to_update
    global cells

    for y, row in enumerate(cells):
        for x, cell in enumerate(row):
            adj_cell_count = 0
            for adj_cell in adjacent_cells:
                adj_cell_y = y + adj_cell[1]
                adj_cell_x = x + adj_cell[0]
                if 0 <= adj_cell_y < h / cell_size and 0 <= adj_cell_x < w / cell_size:
                    adj_cell_count += cells[adj_cell_y][adj_cell_x]
            if cell == 0:
                if adj_cell_count == 3:
                    rects_to_update.append((x * cell_size, y * cell_size, cell_size, cell_size))
            elif cell == 1:
                if adj_cell_count < 2 or adj_cell_count > 3:
                    rects_to_update.append((x * cell_size, y * cell_size, cell_size, cell_size))

setupOn = True
pygame.display.set_caption("Game of Life Setup (Press enter to begin sim)")
while setupOn:
    rects_to_update = []

    for event in pygame.event.get():
        if event.type == QUIT:
            setupOn = False
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                setupOn = False
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos[0] // cell_size, event.pos[1] // cell_size
            rect = (x * cell_size, y * cell_size, cell_size, cell_size)
            rects_to_update.append(rect)
            if cells[y][x] == 0:
                cells[y][x] = 1
                pygame.draw.rect(screen, (255, 255, 255), rect)
            else:
                cells[y][x] = 0
                pygame.draw.rect(screen, (0, 0, 0), rect)

    pygame.display.update(rects_to_update)

simOn = True
pygame.display.set_caption("Game of Life Simulation")
while simOn:
    rects_to_update = []
    applyRules()

    for rect in rects_to_update:
        x, y = rect[0] // cell_size, rect[1] // cell_size
        value = cells[y][x]
        if value == 0:
            cells[y][x] = 1
            pygame.draw.rect(screen, (255, 255, 255), rect)
        else:
            cells[y][x] = 0
            pygame.draw.rect(screen, (0, 0, 0), rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            simOn = False
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos[0] // cell_size, event.pos[1] // cell_size
            rect = (x * cell_size, y * cell_size, cell_size, cell_size)
            rects_to_update.append(rect)
            if cells[y][x] == 0:
                cells[y][x] = 1
                pygame.draw.rect(screen, (255, 255, 255), rect)
            else:
                cells[y][x] = 0
                pygame.draw.rect(screen, (0, 0, 0), rect)

    clock.tick()
    timer -= 1
    if timer == 0:
        print(f"FPS: {clock.get_fps()}")
        timer = 100
    pygame.display.update(rects_to_update)
