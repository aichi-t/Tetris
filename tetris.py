# 3 * 3 piece
# save fall speed
# Instant drop fit bug

import pygame
import json
from tetris_ext import *

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
# shapes = ['I','O']
original_shapes = ['S','Z','I','O','J','L','T']



def main(win):
    global shapes
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece  = get_shape(shapes)
    next_piece = get_shape(shapes)
    hold_piece = None
    hold_lock = False
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.6
    fall_speed_limit = 0.02
    level_time = 0
    current_level = 1
    score = 0
    piece_landed = False
    landed_delay = 0
    delay_limit = 700
    leveled_up = False
    time_since_level_up = 0
    paused = False

    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.mixer.music.load('./sounds/mario.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

    rotation_sound = pygame.mixer.Sound('./sounds/type.wav')
    four_row_sound = pygame.mixer.Sound('./sounds/four_rows.wav')
    hold_sound = pygame.mixer.Sound('./sounds/nandeyanen.wav')

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
                if landed_delay > delay_limit:
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
                    rotation_sound.play()
                    current_piece.rotation += 1
                    if piece_landed:
                        landed_delay -= 200
                    if not(valid_space(current_piece,grid)):
                        current_piece.rotation -= 1
                
                if event.key == pygame.K_SPACE:
                    current_piece.y += 3
                    if not (valid_space(current_piece,grid)):
                        current_piece.y -= 3

                if event.key == pygame.K_LSHIFT:
                    for i in range(20,0,-1):
                        current_piece.y += i
                        if not (valid_space(current_piece,grid)):
                            current_piece.y -= i
                        else:
                            break
                    change_piece = True

                # if event.key == pygame.K_RETURN:
                    # current_piece.y += 4
                    # if not (valid_space(current_piece,grid)):
                        # current_piece.y -= 4
                
                if event.key == pygame.K_RSHIFT:
                    if not hold_lock:
                        hold_sound.play()
                        swapped_piece = True
                        hold_lock = True
                        if hold_piece == None:
                            hold_piece = current_piece
                            hold_piece.reset_piece(5,0)
                            current_piece = next_piece
                            next_piece = get_shape(shapes)
                            next_piece = check_duplicate(hold_piece,current_piece,next_piece,shapes)
                        else:
                            temp_current_piece = current_piece
                            current_piece = hold_piece
                            hold_piece = temp_current_piece 
                            hold_piece.reset_piece(5,0)
                
                if event.key == pygame.K_ESCAPE:
                    
                    paused = True
                     
                if landed_delay < 500:
                    landed_delay = 500

        saved = False
        loaded = False
        loadable = True 
        while paused:
            draw_text_middle("Paused", 80, (255,255,255),win)
            pygame.display.update()
            unpaused = False
            while not unpaused:
                if not saved:
                    draw_text_around_middle("Press 'S' to save state",30,(244, 208, 63),win,50)
                else:
                    draw_text_around_middle("State Saved Successfully",30,(46, 204, 113),win,80)

                if not loaded:
                    draw_text_around_middle("Press 'L' to load state",30,(244, 208, 63),win,110)
                if not loadable:
                    draw_text_around_middle("There is no saved state to load",30,(231, 76, 60),win,170)
                elif loaded:
                    draw_text_around_middle("Saved state loaded",30,(46, 204, 113),win,140)


                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            paused = False
                            unpaused = True
                        if event.key == pygame.K_s:
                            save_state(locked_positions,current_piece,next_piece,hold_piece,current_level,score)
                            saved = True
                        if event.key == pygame.K_l:
                            with open('saved_state.txt','r') as f:
                                lines = f.readlines()
                                f.close()
                            if len(lines) == 0:
                                loadable = False
                            else:
                                loadable = True
                                loaded = True
                                states = load_state()
                                locked_positions = states[0]
                                current_piece = states[1]
                                next_piece = states[2]
                                hold_piece = states[3]
                                current_level = states[4]
                                score = states[5]
                                update_shapes(shapes,current_level)





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

                last_piece = current_piece
                current_piece = next_piece
                next_piece = get_shape(shapes)
                next_piece = check_duplicate(last_piece,current_piece,next_piece,shapes)
                change_piece = False
                deleted_lines = clear_rows(grid,locked_positions)
                if deleted_lines >= 4:
                    four_row_sound.play()
                score += deleted_lines * 10
                hold_lock = False

        # Changing the speed of the piece fall as the level increases 
        if score >= current_level * 50:
            draw_level_up(win)
            leveled_up = True
            current_level += 1
            shapes = update_shapes(shapes,current_level)
            if fall_speed > fall_speed_limit:
                if current_level < 5:
                    fall_speed -= 0.03
                elif current_level < 10:
                    fall_speed -= 0.035
                else:
                    fall_speed -= 0.025
                

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
            shapes = original_shapes
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
