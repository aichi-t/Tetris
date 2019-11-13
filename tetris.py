import pygame
import random
import json
from piece import Piece
# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


shapes = ['S','Z','I','O','J','L','T']


# shapes = [S, Z, I, O, J, L, T, o,i,P,j]
# shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
            #   (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128),(222,32,173),(255,255,255),(102,84,128),(240,247,16)]
# index 0 - 6 represent shape
# shapes = [j]
# shape_colors = [
            #    (240,247,16)]


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

    for i,line in enumerate(format):
        row = list(line)
        for j,column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i,pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j , i) for j in range(10) if grid[i][j] == (0,0,0)]  for i in range(20)]
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

def get_shape():
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

def update_shapes(new_level):
    if new_level == 5:
        shapes.append(i)
        shape_colors.append((255,255,255))
    if new_level == 10:
        shapes.append(P)
        shape_colors.append((117,22,255))
    if new_level == 15:
        shapes.append(J)
        shape_colors.append((255,0,162))

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

def main(win):

    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece  = get_shape()
    next_piece = get_shape()
    hold_piece = None
    hold_lock = False
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.3
    level_time = 0
    current_level = 1
    score = 0
    piece_landed = False
    landed_delay = 0
    leveled_up = False
    time_since_level_up = 0
    paused = False

    while run:
        swapped_piece = False

        grid = create_grid(locked_positions)

        if piece_landed:
            landed_delay += clock.get_rawtime()

        fall_time += clock.get_rawtime() 
        level_time += clock.get_rawtime()
        clock.tick()

            
        # Making the piece fall
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece,grid)) and current_piece.y >0:
                current_piece.y -= 1
                piece_landed = True
                if landed_delay > 1000:
                    change_piece = True
                    piece_landed = False
                    landed_delay = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1 
                    if piece_landed:
                        landed_delay -= 100
                    if not (valid_space(current_piece,grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if piece_landed:
                        landed_delay -= 100
                    if not (valid_space(current_piece,grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece,grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if piece_landed:
                        landed_delay -= 200
                    if not(valid_space(current_piece,grid)):
                        current_piece.rotation -= 1
                
                if event.key == pygame.K_SPACE:
                    current_piece.y += 2
                    if not (valid_space(current_piece,grid)):
                        current_piece.y -= 2
                
                if event.key == pygame.K_RSHIFT:
                    if not hold_lock:
                        swapped_piece = True
                        hold_lock = True
                        if hold_piece == None:
                            hold_piece = current_piece
                            hold_piece.reset_piece(5,0)
                            current_piece = next_piece
                            next_piece = get_shape()
                        else:
                            temp_current_piece = current_piece
                            current_piece = hold_piece
                            hold_piece = temp_current_piece 
                            hold_piece.reset_piece(5,0)
                            # next_piece = get_shape()
                
                if event.key == pygame.K_ESCAPE:
                    
                    paused = True
                     
                if landed_delay < 500:
                    landed_delay = 500

        while paused:
            draw_text_middle("Paused", 80, (255,255,255),win)
            pygame.display.update()
            unpaused = False
            while not unpaused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            paused = False
                            unpaused = True


        if not swapped_piece:
            shape_pos = convert_shape_format(current_piece)

            for i in range(len(shape_pos)):
                x,y = shape_pos[i]
                if y > -1:
                    grid[y][x] =  current_piece.color

            if change_piece:

                for pos in shape_pos:
                    p = (pos[0],pos[1])
                    locked_positions[p] = current_piece.color

                # print(locked_positions)
                # json_dict = json.dumps(locked_positions)
                # f = open("dict.json","w")
                # f.write(json_dict)
                # f.close()

                current_piece = next_piece
                next_piece = get_shape()
                change_piece = False
                score += clear_rows(grid, locked_positions) * 10
                hold_lock = False

        # Changing the speed of the piece fall as the level increases 
        if score >= current_level * 50:
            draw_level_up(win)
            leveled_up = True
            current_level += 1
            if fall_speed > 0.02:
                if current_level < 5:
                    fall_speed -= 0.015
                elif current_level < 10:
                    fall_speed -= 0.025
                else:
                    fall_speed -= 0.03

        draw_window(win,grid,score,current_level)
        draw_hold(hold_piece,win)
        draw_next_shape(next_piece,win)

        if leveled_up:
            time_since_level_up += clock.get_rawtime()
            draw_level_up(win)
            if time_since_level_up > 3000:
                leveled_up = False
                time_since_level_up = 0
                
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("Game Over!", 80, (255,255,255),win)
            pygame.display.update()
            pygame.time.delay(3000)
            run = False
            update_score(score)

def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle("Press Any Key To Play", 60, (255,255,255),win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
        
    pygame.display.quit()

win = pygame.display.set_mode((s_width,s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game
