import pygame
from pygame.locals import *
import random
import math

pygame.init()

# Creating Window and Clock
width = 800
height = 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Creating Fonts
font_big = pygame.font.Font(None, 80)
font_med = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 12)

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Creating Start and Restart Banners
start = font_big.render("Click to Start", True, (0, 0, 255))
start_size = font_big.size("Clock to Start")
start_pos = (width / 2 - start_size[0] / 2, height / 2 - start_size[1] / 2)
start_rect = pygame.Rect(start_pos[0], start_pos[1], start_size[0], start_size[1])

restart = font_big.render("Click to Restart", True, (0, 0, 255))
restart_size = font_big.size("Click to Restart")
restart_pos = (width / 2 - restart_size[0] / 2, height / 2 - restart_size[1] / 2)
restart_rect = pygame.Rect(restart_pos[0], restart_pos[1], restart_size[0], restart_size[1])

# Reverse Mode
reverse = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

class Game():
    def __init__(self, snake_color, head_color, apple_color, grid_w=25, grid_h=25, buffer="AUTO", smoothness=1, fps=20):
        # Grid Constants
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.square_w = width / self.grid_w

        # Colors
        self.snake_color = snake_color
        self.head_color = head_color
        self.apple_color = apple_color

        # Display Constants
        self.smoothness = smoothness
        self.increment = (1 - smoothness) * (self.square_w - 1) + 1
        self.fps = fps
        self.scaled_fps = self.fps * int(self.square_w / self.increment)
        if buffer == "AUTO":
            self.buffer = self.increment / self.square_w
        else:
            self.buffer = buffer
        
        # Score History
        self.score_list = []

    def initialize(self, modes=None, start_length=3, num_apples=1):
        self.score_list.append(0)
        self.event_list = []
       
       # Open Spaces Tracker
        self.open_spaces = []
        for i in range(self.grid_w):
            for n in range(self.grid_h):
                self.open_spaces.append([n, i])

        # Snake and Head
        self.snake = []
        for i in range(2, start_length + 2):
            self.snake.append([i, 12])
            self.open_spaces.remove([i, 12])
        self.head = [start_length + 2, 12]
        self.open_spaces.remove([start_length + 2, 12])
        self.dirs = ["RIGHT" for i in range(2, start_length + 2)]
        self.dir = "RIGHT"

        # Apples
        self.apples = []
        for i in range(num_apples):
            if len(self.open_spaces) > 0:
                rand_idx = random.randint(0, len(self.open_spaces) - 1)
                self.apples.append(self.open_spaces[rand_idx])
                self.open_spaces.pop(rand_idx)
        self.score = 0

        # Initializing Modes
        self.modes = []
        if modes is not None:
            for mode in modes:
                self.modes.append(mode.upper())

        # Drawing Background
        self.background = pygame.Surface((width, height))
        for i in range(self.grid_w):
            for n in range(self.grid_h):
                if (i + n) % 2 == 0:
                    pygame.draw.rect(self.background, (125, 195, 145), (n * self.square_w, i * self.square_w, self.square_w, self.square_w))
                else:
                    pygame.draw.rect(self.background, (90, 195, 100), (n * self.square_w, i * self.square_w, self.square_w, self.square_w))

    def display(self, offset, draw_dir=False):
        # Drawing Screen
        window.blit(self.background, (0, 0))

        # Drawing Snake
        for body_dir, body in zip(self.dirs, self.snake):
            dir_img = font_small.render(body_dir, True, RED)
            dir_img_size = font_small.size(body_dir)
            if body_dir == "RIGHT":
                pygame.draw.rect(window, self.snake_color, (body[0] * self.square_w + offset, body[1] * self.square_w, self.square_w, self.square_w), border_radius=5)
                if draw_dir:
                    window.blit(dir_img, (body[0] * self.square_w + offset + self.square_w / 2 - dir_img_size[0] / 2, body[1] * self.square_w + self.square_w / 2 - dir_img_size[1] / 2))
            elif body_dir == "UP":
                pygame.draw.rect(window, self.snake_color, (body[0] * self.square_w, body[1] * self.square_w - offset, self.square_w, self.square_w), border_radius=5)
                if draw_dir:
                    window.blit(dir_img, (body[0] * self.square_w + self.square_w / 2 - dir_img_size[0] / 2, body[1] * self.square_w - offset + self.square_w / 2 - dir_img_size[1] / 2))
            elif body_dir == "LEFT":
                pygame.draw.rect(window, self.snake_color, (body[0] * self.square_w - offset, body[1] * self.square_w, self.square_w, self.square_w), border_radius=5)
                if draw_dir:
                    window.blit(dir_img, (body[0] * self.square_w - offset + self.square_w / 2 - dir_img_size[0] / 2, body[1] * self.square_w + self.square_w / 2 - dir_img_size[1] / 2))
            elif body_dir == "DOWN":
                pygame.draw.rect(window, self.snake_color, (body[0] * self.square_w, body[1] * self.square_w + offset, self.square_w, self.square_w), border_radius=5)
                if draw_dir:
                    window.blit(dir_img, (body[0] * self.square_w + self.square_w / 2 - dir_img_size[0] / 2, body[1] * self.square_w + offset + self.square_w / 2 - dir_img_size[1] / 2))

        # Drawing Head
        if self.dir == "RIGHT":
            pygame.draw.rect(window, self.head_color, (self.head[0] * self.square_w + offset, self.head[1] * self.square_w, self.square_w, self.square_w), border_radius=5)
            if draw_dir:
                window.blit(dir_img, (self.head[0] * self.square_w + offset + self.square_w / 2 - dir_img_size[0] / 2, self.head[1] * self.square_w + self.square_w / 2 - dir_img_size[1] / 2))
        elif self.dir == "UP":
            pygame.draw.rect(window, self.head_color, (self.head[0] * self.square_w, self.head[1] * self.square_w - offset, self.square_w, self.square_w), border_radius=5)
            if draw_dir:
                window.blit(dir_img, (self.head[0] * self.square_w + self.square_w / 2 - dir_img_size[0] / 2, self.head[1] * self.square_w - offset + self.square_w / 2 - dir_img_size[1] / 2))
        elif self.dir == "LEFT":
            pygame.draw.rect(window, self.head_color, (self.head[0] * self.square_w - offset, self.head[1] * self.square_w, self.square_w, self.square_w), border_radius=5)
            if draw_dir:
                window.blit(dir_img, (self.head[0] * self.square_w - offset + self.square_w / 2 - dir_img_size[0] / 2, self.head[1] * self.square_w + self.square_w / 2 - dir_img_size[1] / 2))
        elif self.dir == "DOWN":
            pygame.draw.rect(window, self.head_color, (self.head[0] * self.square_w, self.head[1] * self.square_w + offset, self.square_w, self.square_w), border_radius=5)
            if draw_dir:
                window.blit(dir_img, (self.head[0] * self.square_w + self.square_w / 2 - dir_img_size[0] / 2, self.head[1] * self.square_w + offset + self.square_w / 2 - dir_img_size[1] / 2))

        # Drawing Apple
        for apple in self.apples:
            pygame.draw.rect(window, self.apple_color, (apple[0] * self.square_w, apple[1] * self.square_w, self.square_w, self.square_w), border_radius=5)
        
        # Drawing Score
        score_surf = font_big.render(str(self.score), True, BLUE)
        window.blit(score_surf, (15, 15))

    def run(self, debug_mode=False):
        offset = 0
        game_on = True
        paused = False
        while game_on:
            window.fill((0, 0, 0))

            # Event Handling
            self.event_list += pygame.event.get(eventtype=[KEYDOWN, QUIT])
            for event in self.event_list:
                if event.type == QUIT:
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_k: # Insta Kill Button
                        game_on = False
            if offset < self.increment:
                while len(self.event_list) > 0:
                    event = self.event_list[0]
                    self.event_list.pop(0)
                    if event.type == KEYDOWN:  # Not technically needed
                        if (event.key == K_w or event.key == K_UP) and self.dir != "DOWN" and self.dirs[-1] != "DOWN":
                            self.dir = "UP"
                            break
                        elif (event.key == K_a or event.key == K_LEFT) and self.dir != "RIGHT" and self.dirs[-1] != "RIGHT":
                            self.dir = "LEFT"
                            break
                        elif (event.key == K_s or event.key == K_DOWN) and self.dir != "UP" and self.dirs[-1] != "UP":
                            self.dir = "DOWN"
                            break
                        elif (event.key == K_d or event.key == K_RIGHT) and self.dir != "LEFT" and self.dirs[-1] != "LEFT":
                            self.dir = "RIGHT"
                            break
                        elif event.key == K_SPACE:
                            paused = True

            # Incrementing Offset
            offset = (offset + self.increment) % self.square_w

            # Moving Snake
            if offset < self.increment:
                self.snake.append(self.head.copy())
                self.dirs.append(self.dir)
                if self.dir == "RIGHT":
                    self.head[0] += 1
                elif self.dir == "UP":
                    self.head[1] -= 1
                elif self.dir == "LEFT":
                    self.head[0] -= 1
                elif self.dir == "DOWN":
                    self.head[1] += 1

                if "PEACEFUL" in self.modes:
                    for i, body in enumerate(self.snake):
                        self.snake[i] = [body[0] % self.grid_w, body[1] % self.grid_h]
                    self.head = [self.head[0] % self.grid_w, self.head[1] % self.grid_h]

                if self.snake[0] not in self.apples and self.snake[0] not in self.snake[1:]:
                    self.open_spaces.append(self.snake[0].copy())
                if self.head in self.open_spaces:
                    self.open_spaces.remove(self.head.copy())
                self.snake.pop(0)
                self.dirs.pop(0)

            # Apple Collisions
            for i, apple in enumerate(self.apples):
                ate = False
                if self.dir == "RIGHT":
                    if self.head[1] == apple[1] and math.ceil(self.head[0] - self.buffer + offset / self.square_w) % self.square_w == apple[0]:
                        ate = True
                elif self.dir == "UP":
                    if self.head[0] == apple[0] and math.floor(self.head[1] + self.buffer - offset / self.square_w) % self.square_w == apple[1]:
                        ate = True
                elif self.dir == "LEFT":
                    if self.head[1] == apple[1] and math.floor(self.head[0] + self.buffer - offset / self.square_w) % self.square_w == apple[0]:
                        ate = True
                elif self.dir == "DOWN":
                    if self.head[0] == apple[0] and math.ceil(self.head[1] - self.buffer + offset / self.square_w) % self.square_w == apple[1]:
                        ate = True
                if ate:
                    self.score += 1
                    self.score_list[-1] += 1
                    if len(self.open_spaces) > 0:
                        rand_idx = random.randint(0, len(self.open_spaces) - 1)
                        self.apples.pop(i)
                        self.apples.insert(i, self.open_spaces[rand_idx])
                        self.open_spaces.pop(rand_idx)
                    else:
                        self.apples.pop(i)
                    
                    if "REVERSE" in self.modes:
                        self.snake.reverse()
                        self.dirs.reverse()

                        old_head = self.head.copy()
                        old_tail = self.snake[-1].copy()
                        self.head = old_tail
                        self.snake.pop(-1)
                        self.snake.insert(0, old_head)
                        old_head_dir = self.dir
                        old_tail_dir = self.dirs[-1]
                        self.dir = reverse[old_tail_dir]
                        self.dirs.pop(-1)
                        self.dirs.insert(0, reverse[old_head_dir])

                        for i in range(1, len(self.dirs)):
                            self.dirs[i] = reverse[self.dirs[i]]
                        
                        for body_dir, body in zip(self.dirs, self.snake):
                            if body_dir == "RIGHT":
                                body[0] -= 1
                            elif body_dir == "UP":
                                body[1] += 1
                            elif body_dir == "LEFT":
                                body[0] += 1
                            elif body_dir == "DOWN":
                                body[1] -= 1
                        
                        if self.dir == "RIGHT":
                            self.head[0] -= 1
                        elif self.dir == "UP":
                            self.head[1] += 1
                        elif self.dir == "LEFT":
                            self.head[0] += 1
                        elif self.dir == "DOWN":
                            self.head[1] -= 1
                        
                    dx = self.snake[1][0] - self.snake[0][0]
                    dy = self.snake[1][1] - self.snake[0][1]
                    new = [self.snake[0][0] - dx, self.snake[0][1] - dy]
                    if new.copy() in self.open_spaces:
                        self.open_spaces.remove(new.copy())
                    self.snake.insert(0, new)
                    self.dirs.insert(0, self.dirs[0])
            
            # Body Collisions
            if "PEACEFUL" not in self.modes:
                for body in self.snake:
                    if self.dir == "RIGHT":
                        if self.head[1] == body[1] and math.ceil(self.head[0] + offset / self.square_w) == body[0]:
                            game_on = False
                    elif self.dir == "UP":
                        if self.head[0] == body[0] and math.floor(self.head[1] - offset / self.square_w) == body[1]:
                            game_on = False
                    elif self.dir == "LEFT":
                        if self.head[1] == body[1] and math.floor(self.head[0] - offset / self.square_w) == body[0]:
                            game_on = False
                    elif self.dir == "DOWN":
                        if self.head[0] == body[0] and math.ceil(self.head[1] + offset / self.square_w) == body[1]:
                            game_on = False
            
            # Wall Collisions
            if "PEACEFUL" not in self.modes:
                if self.dir == "RIGHT":
                    if math.ceil(self.head[0] - self.buffer + offset / self.square_w) >= self.grid_w:
                        game_on = False
                elif self.dir == "UP":
                    if math.ceil(self.head[1] + self.buffer - offset / self.square_w) <= 0:
                        game_on = False
                elif self.dir == "LEFT":
                    if math.ceil(self.head[0] + self.buffer - offset / self.square_w) <= 0:
                        game_on = False
                elif self.dir == "DOWN":
                    if math.ceil(self.head[1] - self.buffer + offset / self.square_w) >= self.grid_h:
                        game_on = False

            self.display(offset, draw_dir=debug_mode)

            # Debug Section ----------
            # Printing
            if paused:
                pass

            # Freezing Frame
            next_frame = False
            while paused and not next_frame:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                    if event.type == KEYDOWN:
                        if event.key == K_f:
                            next_frame = True
                        if event.key == K_SPACE:
                            paused = False
            
            if debug_mode:
                for space in self.open_spaces:
                    pygame.draw.rect(window, GREEN, (space[0] * self.square_w + 5, space[1] * self.square_w + 5, self.square_w - 10, self.square_w - 10))
            # ------------------------

            pygame.display.update()

            clock.tick(self.scaled_fps + min(self.score * 0.0, 50))

# Colors
snake_color = (50, 50, 200)
head_color = (150, 25, 250)
apple_color = (200, 75, 10)

game = Game(snake_color=snake_color, head_color=head_color, apple_color=apple_color, grid_w=25, grid_h=25, smoothness=0.75, fps=10)
game.initialize(modes=[], num_apples=3)

start_flag = True
while start_flag:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                start_flag = False
        
        game.display(0)
        window.blit(start, start_pos)
        pygame.display.update()

game.run(debug_mode=False)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            if restart_rect.collidepoint(event.pos):
                game.initialize(modes=[], num_apples=3)
                game.run(debug_mode=False)
    
    highscore = font_big.render("Highest: {}".format(max(game.score_list)), True, (0, 0, 255))
    highscore_size = font_med.size("Highest: {}".format(max(game.score_list)))
    highscore_pos = (width / 2 - highscore_size[0] / 2, restart_pos[1] + restart_size[1] + 5)
    
    window.blit(highscore, highscore_pos)
    window.blit(restart, restart_pos)

    pygame.display.update()
