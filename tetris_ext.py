import pygame
import random
from piece import Piece


# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height



def create_grid(locked_positions={}):

    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i]
                     [j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x ,y = pos
        if y < 1:
            return True
    return False

def get_shape(shapes):
    return Piece(5,0,random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans",size, bold = True)
    label = font.render(text, 1, color)

    
    surface.blit(label,(top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))

def draw_level_up(surface):
    font = pygame.font.SysFont("comicsans",30, bold = True)
    label = font.render("Level Up!!!", 1, (255,244,18))

    sx = top_left_x + play_width + 50
    sy = top_left_y + (play_height / 2) + 10

    surface.blit(label, (sx + 20, sy + 130))

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    
    for i in range(len(grid)):
        pygame.draw.line(surface,(128,128,128),(sx,sy+i*block_size), (sx+play_width,sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface,(128,128,128),(sx + j*block_size,sy), (sx+j*block_size,sy + play_height))

def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid) -1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    
    if inc > 0:
        for key in sorted(list(locked), key = lambda x:x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x,y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))


    sx = top_left_x + play_width + 50
    sy = top_left_y  + 50

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size,block_size),0)
    
    surface.blit(label,(sx + 10, sy - 30))

def draw_hold(shape,surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Hold', 1, (255,255,255))

    sx = top_left_x - 150 
    sy = top_left_y

    if shape != None:
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j*block_size - 45, sy + i*block_size, block_size,block_size),0)
        
    surface.blit(label,(sx + 10, sy - 30))


def draw_window(surface,grid,score,current_level):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width /
                         2 - (label.get_width()/2), 30))

    # Displaying current level
    font = pygame.font.SysFont('comiscans',30)
    label = font.render('Level: '+ str(current_level), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + (play_height / 2) + 10

    surface.blit(label, (sx + 20, sy + 160))

    # Displaying score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + (play_height / 2) + 50

    surface.blit(label, (sx + 20,sy + 160))
    
    # Displaying high score
    with open('scores.txt','r') as f:
        lines = f.readlines()
        high_score = lines[0].strip()    

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('High Score:' + high_score, 1, (255,255,255))

    sx = top_left_x - play_width + 100
    sy = top_left_y + play_height / 2 - 200

    surface.blit(label, (sx + 20,sy + 160))
 


    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size,block_size),0)

    pygame.draw.rect(surface, (255,255,255), (top_left_x,top_left_y,play_width,play_height),4)

    draw_grid(surface,grid)
    # pygame.display.update()

def update_shapes(shapes,new_level):
    if new_level == 5:
        shapes.append('1')
    elif new_level == 10:
        shapes.append('P')
    elif new_level == 15:
        shapes.append('W')

def update_score(nscore):
    with open('scores.txt', 'r') as f: 
        lines = f.readlines()
        score = lines[0].strip()
        print(score)
    with open('scores.txt','w') as f:
        if int(score) > nscore:
            f.write(score)
        else:
            f.write(str(nscore))

