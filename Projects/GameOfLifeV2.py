import pygame
from pygame.locals import *
import numpy as np
import scipy.signal as signal

def tupleToVector2(p, type=float):
    return pygame.Vector2(type(p[0]), type(p[1]))

def vector2ToTuple(p, type=float):
    return (type(p[0]), type(p[1]))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

KERNEL = np.ones((3, 3))
KERNEL[1, 1] = 0

class Grid():
    def __init__(self, 
                 gw: int, 
                 gh: int):
        self.gw = gw
        self.gh = gh
        self.grid = np.zeros((self.gh, self.gw))

    def get_border(self):
        return np.concatenate([self.grid[:-1, 0],
                               self.grid[0, :-1],
                               self.grid[:-1, -1],
                               self.grid[-1, :-1]])
    
    def expand(self, 
               n: int=1):
        self.gw += 2 * n
        self.gh += 2 * n
        self.grid = np.pad(self.grid, n)
    
    def apply_rules(self):
        neighbors = signal.convolve2d(self.grid, KERNEL, mode="same")
        birth_flag = np.logical_or(neighbors == 3, False)
        death_flag = np.logical_or(neighbors < 2, neighbors > 3)
        self.grid[birth_flag] = 1
        self.grid[death_flag] = 0
    
    def step(self):
        self.apply_rules()
        if self.get_border().any():
            self.expand()
    
    def draw(self, 
             surf: pygame.Surface,
             _gw: int, 
             _gh: int, 
             grid_offset_x: int, 
             grid_offset_y: int, 
             draw_grid: bool=True, 
             full_grid: bool=True, 
             visualize_neighbors: bool=False):
        if visualize_neighbors:
            neighbors = signal.convolve2d(self.grid, KERNEL, mode="same")
        surf.fill(BLACK)
        w, h = surf.get_size()
        cell_size = w // _gw
        center_x = (self.gw + grid_offset_x) // 2
        center_y = (self.gh + grid_offset_y) // 2
        left = center_x - _gw // 2
        top = center_y - _gh // 2
        right = center_x + _gw // 2
        bottom = center_y + _gh // 2
        for i in range(_gw):
            for n in range(_gh):
                x = left + i
                y = top + n
                if 0 <= x < self.gw and 0 <= y < self.gh:
                    if visualize_neighbors:
                        cell = neighbors[y, x]
                        color_value = 255 * cell / 8
                        color = (color_value, color_value, color_value)
                        pygame.draw.rect(surf, color, (i * cell_size, n * cell_size, cell_size, cell_size))
                    else:
                        cell = self.grid[y, x]
                        color = WHITE if cell else BLACK
                        pygame.draw.rect(surf, color, (i * cell_size, n * cell_size, cell_size, cell_size))
        if draw_grid:
            if full_grid:
                grid_left = 0
                grid_top = 0
                grid_right = _gw
                grid_bottom = _gh
            else:
                if left < 0:
                    grid_left = min(_gw, abs(left))
                else:
                    grid_left = 0

                if top < 0:
                    grid_top = min(_gh, abs(top))
                else:
                    grid_top = 0
                
                if right > self.gw:
                    grid_right = min(_gw, _gw - (right - self.gw))
                else:
                    grid_right = _gw

                if bottom > self.gh:
                    grid_bottom = min(_gh, _gh - (bottom - self.gh))
                else:
                    grid_bottom = _gh
            for i in range(grid_left, grid_right + 1):
                pygame.draw.line(surf, BLUE, (i * cell_size, grid_top * cell_size), (i * cell_size, grid_bottom * cell_size))
            for i in range(grid_top, grid_bottom + 1):
                pygame.draw.line(surf, BLUE, (grid_left * cell_size, i * cell_size), (grid_right * cell_size, i * cell_size))

pygame.init()

w, h = 800, 800
window = pygame.display.set_mode((w, h))

even_divisors = []
for i in range(1, min(w + 1, h + 1)):
    if w % i == 0 and w / i % 2 == 0 and h % i == 0 and h / i % 2 == 0:
        even_divisors.append(i)
divisor_idx = 7
cell_size = even_divisors[divisor_idx]
gw, gh = w // cell_size, h // cell_size
grid = Grid(gw, gh)

print(even_divisors)

clock = pygame.time.Clock()
fps = 100

draw_grid = True
full_grid = True
visualize_neighbors = False
running = False
clicked = False
moved = False
pygame.display.set_caption("Conway's Game of Life (Paused)")

past_pos = tupleToVector2(pygame.mouse.get_pos())
offset = pygame.Vector2()

sim_on = True
while sim_on:
    if running:
        grid.step()

    for event in pygame.event.get():
        if event.type == QUIT:
            sim_on = False
        elif event.type == MOUSEBUTTONDOWN:
            clicked = True
        elif event.type == MOUSEBUTTONUP:
            if not moved:
                pos = tupleToVector2(event.pos)
                center_x = (grid.gw - int(offset.x // cell_size)) // 2
                center_y = (grid.gh - int(offset.y // cell_size)) // 2
                x = int(center_x + (pos.x - w // 2) // cell_size)
                y = int(center_y + (pos.y - h // 2) // cell_size)

                if x < 0 and y < 0:
                    grid.expand(max(abs(x), abs(y)) + 1)
                elif x < 0 and y > grid.gh - 1:
                    grid.expand(max(abs(x), y - grid.gh) + 1)
                elif x > grid.gw - 1 and y < 0:
                    grid.expand(max(x - grid.gw, abs(y)) + 1)
                elif x > grid.gw - 1 and y > grid.gw - 1:
                    grid.expand(max(x - grid.gw, y - grid.gh) + 1)
                elif x < 0:
                    grid.expand(abs(x) + 1)
                elif y < 0:
                    grid.expand(abs(y) + 1)
                elif x > grid.gw - 1:
                    grid.expand(x - grid.gw + 1)
                elif y > grid.gh - 1:
                    grid.expand(y - grid.gh + 1)

                center_x = (grid.gw - int(offset.x // cell_size)) // 2
                center_y = (grid.gh - int(offset.y // cell_size)) // 2
                x = int(center_x + (pos.x - w // 2) // cell_size)
                y = int(center_y + (pos.y - h // 2) // cell_size)

                grid.grid[y, x] = 0 if grid.grid[y, x] else 1
            clicked = False
            moved = False
        elif event.type == MOUSEMOTION:
            pos = tupleToVector2(event.pos)
            if clicked:
                pos_change = (pos - past_pos) * 2
                offset += pos_change
                if abs(pos_change.x // cell_size) > 0 or abs(pos_change.y // cell_size) > 0:
                    moved = True
            past_pos = pos
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                running = not running
                pygame.display.set_caption("Conway's Game of Life ({})".format("Running" if running else "Paused"))
            elif event.key == K_UP:
                if divisor_idx > 1:
                    offset *= even_divisors[divisor_idx - 1] / even_divisors[divisor_idx]
                divisor_idx = max(1, divisor_idx - 1)
                cell_size = even_divisors[divisor_idx]
                gw, gh = w // cell_size, h // cell_size
            elif event.key == K_DOWN:
                if divisor_idx < len(even_divisors) - 1:
                    offset *= even_divisors[divisor_idx + 1] / even_divisors[divisor_idx]
                divisor_idx = min(len(even_divisors) - 1, divisor_idx + 1)
                cell_size = even_divisors[divisor_idx]
                gw, gh = w // cell_size, h // cell_size
            elif event.key == K_RIGHT:
                grid.step()
            elif event.key == K_f:
                full_grid = not full_grid
            elif event.key == K_g:
                draw_grid = not draw_grid
            elif event.key == K_c:
                offset = pygame.Vector2(0, 0)
            elif event.key == K_n:
                visualize_neighbors = not visualize_neighbors

    grid.draw(window, 
              gw, 
              gh, 
              -int(offset.x // cell_size), 
              -int(offset.y // cell_size), 
              draw_grid=draw_grid, 
              full_grid=full_grid, 
              visualize_neighbors=visualize_neighbors)
    pygame.display.update()
    clock.tick(fps)

"""
Instructions:

Mouse button: Click on individual cells to set them as either alive (white) or dead (black)
Space bar: Start or pause the simulation
Up arrow: Zoom out
Down arrow: Zoom in
g: Toggle the grid
f: Toggle the display of the dynamically sized grid
"""
