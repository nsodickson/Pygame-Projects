import pygame
from pygame.locals import *
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initializing Pygame and Pygame Window
pygame.init()
w, h = 1000, 500
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Spelling Bee")
font = pygame.font.Font(None, 50)
large_font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()
bg_color = (255, 255, 255)
poly_color = (255, 174, 66)
font_color = (0, 0, 0)

main_center = (250, 250)
radius = 50

centers = [main_center]
for i in range(6):
    centers.append((main_center[0] + (math.sqrt(3) + 0.1) * radius * math.sin(math.pi / 3 * i), 
                    main_center[1] + (math.sqrt(3) + 0.1) * radius * math.cos(math.pi / 3 * i)))

polygons = []
for center in centers:
    polygons.append([])
    for i in range(6):
        polygons[-1].append((center[0] + radius * math.cos(math.pi / 3 * i), 
                             center[1] + radius * math.sin(math.pi / 3 * i)))
        
reset_button = pygame.Rect(350, 15, 125, 30)

# Integer and Boolean flags for multi-frame actions
delete = False
delete_timer = 0
display_timer = 0
message = ""

# Defining helper functions
def dist(p1, p2):
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)

# Randomly samples letters from a key
def genRandomLetters(key, num_letters):
    assert num_letters < len(key)
    return random.sample(key, num_letters)

# Randomly samples a word with a given number of unqiue letters from a key, shuffles the letters, and returns them
def genLetters(word_key, num_letters):
    word_key_shuffled = random.sample(word_key, len(word_key))
    for word in word_key_shuffled:
        letters = []
        for letter in word:
            if letter not in letters:
                letters.append(letter)
        if len(letters) == num_letters:
            random.shuffle(letters)
            return letters
    print("No letters found")
    return []

# Checks if a queue of letters contains every letter in a key at least once
def isPanogram(key, letter_queue):
    for letter in key:
        if letter not in letter_queue:
            return False
    return True

# Obtain master word and letter list
with open("words_medium.txt") as f:
    word_key = f.read().split("\n")
vowels = "aeiou"
consonants = "bcdfghjklmnpqrstvwxyz"
while True:
    gameOn = True
    
    letters = genLetters(word_key, 7)
    
    letter_queue = ""
    word_queue = []
    score = 0
    
    while gameOn:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
                
            elif event.type == TEXTINPUT:
                if event.text.lower() in letters:
                    letter_queue += event.text.lower()
            
            elif event.type == KEYDOWN:
                # Handling deleting letters
                if event.key == K_BACKSPACE:
                    letter_queue = letter_queue[0:-1]
                    delete = True
                    delete_timer = 5
                
                # Handling checking a word
                elif event.key == K_RETURN:
                    if letter_queue in word_queue:
                        message = "Already Found"
                    elif letters[0] not in letter_queue:
                        message = "Missing Center Letter"
                    elif len(letter_queue) < 4:
                        message = "Too Short"
                    elif letter_queue in word_key:
                        word_queue.append(letter_queue)
                        if isPanogram(letters, letter_queue):
                            message = "Pangram!"
                            score += len(letter_queue) + 7
                        elif len(letter_queue) == 4:
                            message = "+"
                            score += 1
                        else:
                            message = "+" 
                            score += len(letter_queue)
                    else:
                        message = "Not a Word"
                    display_timer = 10
                    letter_queue = ""
            
            # Handling stopping deleting letters
            elif event.type == KEYUP:
                if event.key == K_BACKSPACE:
                    delete = False
            
            # Handling clicking the new game button or a letter
            elif event.type == MOUSEBUTTONDOWN:
                for letter, center in zip(letters, centers):
                    if dist(center, event.pos) < math.sqrt(3) / 2 * radius:
                        letter_queue += letter
                if reset_button.collidepoint(event.pos):
                    gameOn = False
        
        win.fill(bg_color)
    
        if delete:
            if delete_timer > 0:
                delete_timer -= 1
            else:
                letter_queue = letter_queue[0:-1]
        
        # Drawing the new game button
        pygame.draw.rect(win, poly_color, reset_button)
        button_surf = small_font.render("New Game", True, font_color)   
        button_size = small_font.size("New Game")
        win.blit(button_surf, (350 + (125 - button_size[0]) / 2, 15 + button_size[1] / 2))
        
        # Drawing the score
        score_surf = font.render(f"Score: {score}", True, font_color)
        win.blit(score_surf, (15, 15))
        
        # Drawing the currently guessed letters
        letter_queue_surf = font.render(letter_queue, True, font_color)
        letter_queue_size = font.size(letter_queue)
        win.blit(letter_queue_surf, (250 - letter_queue_size[0] / 2, 50))
        
        # Drawing the letters
        for letter, polygon, center in zip(letters, polygons, centers):
            pygame.draw.polygon(win, poly_color, polygon)
            pygame.draw.polygon(win, BLACK, polygon, 3)
            letter_surf = font.render(letter, True, font_color)
            letter_size = font.size(letter)
            win.blit(letter_surf, (center[0] - letter_size[0] / 2, center[1] - letter_size[1] / 2))
        
        # Drawing the already guessed words
        pygame.draw.rect(win, font_color, (505, 5, 490, 490), width=5)
        x, y, max_length = 20, 20, 0
        for idx, word in enumerate(word_queue):
            max_length = max(small_font.size(word)[0], max_length)
            word_surf = small_font.render(word, False, font_color)
            win.blit(word_surf, (x + 500, y))
            if y >= 450:
                x += max_length + 15
                y = 20
                max_length = 0
            else:
                y += 30

         # Drawing the message after checking a word
        if display_timer > 0:
            message_surf = large_font.render(message, False, font_color)
            message_surf.set_alpha(255 - 25.5 * (10 - display_timer))
            message_size = large_font.size(message)
            win.blit(message_surf, (250 - message_size[0] / 2, 400))
            display_timer -= 1
            
        pygame.display.update()
        
        clock.tick(10)
