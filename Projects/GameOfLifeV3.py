import pygame
from pygame.locals import *
import numpy as np
import scipy.signal as signal

def tupleToVector2(p, type=float):
    return pygame.Vector2(type(p[0]), type(p[1]))

def vector2ToTuple(p, type=float):
    return (type(p[0]), type(p[1]))

def gridTransform(x, y):
    return x + y % 2 * 0.5, y * np.sqrt(3) / 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

ODD_KERNEL = np.array([[1, 1, 0],
                       [1, 0, 1],
                       [1, 1, 0]])
EVEN_KERNEL = np.array([[0, 1, 1],
                        [1, 0, 1],
                        [0, 1, 1]])

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
        self.gw += 4 * n
        self.gh += 4 * n
        self.grid = np.pad(self.grid, 2 * n)  # Expand by 2 to avoid parity switches
    
    def apply_rules(self):
        even_neighbors = signal.convolve2d(self.grid, EVEN_KERNEL, mode="same")
        odd_neighbors = signal.convolve2d(self.grid, ODD_KERNEL, mode="same")
        neighbors = np.zeros_like(self.grid)
        neighbors[::2] = even_neighbors[::2]
        neighbors[1::2] = odd_neighbors[1::2]
        alive_flag = self.grid == 1
        dead_flag = self.grid == 0
        birth_flag = np.logical_or(neighbors == 2, False)
        death_flag = np.logical_or(neighbors < 3, neighbors > 4)
        self.grid[np.logical_and(birth_flag, dead_flag)] = 1
        self.grid[np.logical_and(death_flag, alive_flag)] = 0
    
    def step(self):
        self.apply_rules()
        if self.get_border().any():
            self.expand()
    
    def draw(self, 
             surf: pygame.Surface,
             _gw: int, 
             _gh: int,
             cell_size: int, 
             grid_offset_x: int, 
             grid_offset_y: int, 
             draw_grid: bool=True, 
             full_grid: bool=True,
             visualize_neighbors: bool=False):
        surf.fill(BLACK)
        if visualize_neighbors:
            even_neighbors = signal.convolve2d(self.grid, EVEN_KERNEL, mode="same")
            odd_neighbors = signal.convolve2d(self.grid, ODD_KERNEL, mode="same")
            neighbors = np.zeros_like(self.grid)
            neighbors[::2] = even_neighbors[::2]
            neighbors[1::2] = odd_neighbors[1::2]
        x_center = (self.gw + grid_offset_x) // 2
        y_center = (self.gh + grid_offset_y) // 2
        left = x_center - _gw // 2
        top = y_center - _gh // 2
        right = x_center + _gw // 2
        bottom = y_center + _gh // 2
        for i in range(_gh):
            for n in range(_gw):
                x_idx = left + n  # x in the original square lattice
                y_idx = top + i  # y in the original square lattice
                x_trans = n + y_idx % 2 * 0.5  # x in the transformed hexagon lattice
                y_trans = i * np.sqrt(3) / 2  # y in the transformed hexagon lattice
                if 0 <= x_idx < self.gw and 0 <= y_idx < self.gh:
                    if visualize_neighbors:
                        cell = neighbors[y_idx, x_idx]
                        color_value = 255 * cell / 6
                        color = (color_value, color_value, color_value)
                    else:
                        cell = self.grid[y_idx, x_idx]
                        color = WHITE if cell else BLACK
                    points = np.array([[x_trans, y_trans + np.sqrt(3) / 3],
                                       [x_trans + 0.5, y_trans + np.sqrt(3) / 6],
                                       [x_trans + 0.5, y_trans - np.sqrt(3) / 6],
                                       [x_trans, y_trans - np.sqrt(3) / 3],
                                       [x_trans - 0.5, y_trans - np.sqrt(3) / 6],
                                       [x_trans - 0.5, y_trans + np.sqrt(3) / 6]])
                    pygame.draw.polygon(surf, color, points * cell_size)
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
            for i in range(grid_top, grid_bottom):
                for n in range(grid_left, grid_right):
                    x_trans = n + (top + i) % 2 * 0.5
                    y_trans = i * np.sqrt(3) / 2
                    points = np.array([[x_trans, y_trans + np.sqrt(3) / 3],
                                       [x_trans + 0.5, y_trans + np.sqrt(3) / 6],
                                       [x_trans + 0.5, y_trans - np.sqrt(3) / 6],
                                       [x_trans, y_trans - np.sqrt(3) / 3],
                                       [x_trans - 0.5, y_trans - np.sqrt(3) / 6],
                                       [x_trans - 0.5, y_trans + np.sqrt(3) / 6]])
                    pygame.draw.polygon(surf, BLUE, points * cell_size, 1)

pygame.init()

w, h = 800, 800
window = pygame.display.set_mode((w, h))

even_divisors = []
for i in range(1, min(w + 1, h + 1)):
    if w % i == 0 and w / i % 2 == 0 and h % i == 0 and h / i % 2 == 0:
        even_divisors.append(i)
divisor_idx = 7
cell_size = even_divisors[divisor_idx]
gw = int(w // cell_size) + 2
gh = int(h // cell_size * 2 / np.sqrt(3)) + 2
grid = Grid(gw, gh)

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
                x_center = (grid.gw - int(offset.x // cell_size)) // 2
                y_center = (grid.gh - int(offset.y // cell_size)) // 2
                left = x_center - gw // 2
                top = y_center - gh // 2
                i = 0
                found = False
                while i < gh and not found:
                    n = 0
                    while n < gw and not found:
                        x_idx = left + n
                        y_idx = top + i
                        x_trans = n + y_idx % 2 * 0.5
                        y_trans = i * np.sqrt(3) / 2
                        if np.sqrt((pos.x / cell_size - x_trans) ** 2 + (pos.y / cell_size - y_trans) ** 2) < 0.5:
                            if x_idx < 0 and y_idx < 0:
                                grid.expand(max(abs(x_idx), abs(y_idx)) + 1)
                            elif x_idx < 0 and y_idx > grid.gh - 1:
                                grid.expand(max(abs(x_idx), y_idx - grid.gh) + 1)
                            elif x_idx > grid.gw - 1 and y_idx < 0:
                                grid.expand(max(x_idx - grid.gw, abs(y_idx)) + 1)
                            elif x_idx > grid.gw - 1 and y_idx > grid.gw - 1:
                                grid.expand(max(x_idx - grid.gw, y_idx - grid.gh) + 1)
                            elif x_idx < 0:
                                grid.expand(abs(x_idx) + 1)
                            elif y_idx < 0:
                                grid.expand(abs(y_idx) + 1)
                            elif x_idx > grid.gw - 1:
                                grid.expand(x_idx - grid.gw + 1)
                            elif y_idx > grid.gh - 1:
                                grid.expand(y_idx - grid.gh + 1)

                            x_center = (grid.gw - int(offset.x // cell_size)) // 2
                            y_center = (grid.gh - int(offset.y // cell_size)) // 2
                            left = x_center - gw // 2
                            top = y_center - gh // 2
                            x_idx = left + n
                            y_idx = top + i

                            grid.grid[y_idx, x_idx] = 0 if grid.grid[y_idx, x_idx] else 1
                            found = True
                        n += 1
                    i += 1
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
                if divisor_idx > 4:
                    offset *= even_divisors[divisor_idx - 1] / even_divisors[divisor_idx]
                divisor_idx = max(4, divisor_idx - 1)
                cell_size = even_divisors[divisor_idx]
                gw = int(w // cell_size) + 1
                gh = int(h // cell_size * 2 / np.sqrt(3)) + 2
            elif event.key == K_DOWN:
                if divisor_idx < len(even_divisors) - 1:
                    offset *= even_divisors[divisor_idx + 1] / even_divisors[divisor_idx]
                divisor_idx = min(len(even_divisors) - 1, divisor_idx + 1)
                cell_size = even_divisors[divisor_idx]
                gw = int(w // cell_size) + 1
                gh = int(h // cell_size * 2 / np.sqrt(3)) + 2
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
              cell_size, 
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
