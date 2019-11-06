#!/usr/bin/python

# Author: Timothy Yang
# Date: October 2019

# Maze graphics program to showcase the maze and the strategy to solve the maze.
# All avatars need to explore the maze and meet up together before time ends.
# It reads a log file that has the outputed logs from our main code program that solves the maze, and showcase the result.
# Before using the program, please make sure to have Python 3 and the following python accessories downloaded.

import pygame
from pygame.locals import *
import sys
import argparse
from argparse import ArgumentParser
from pathlib2 import Path
from random import randrange
import array as arr

# Usage:
# python maze_graphics.py log_file resources_folder fancy_or_not
#
# Example:
# python maze_graphics.py maze_taiwana_10_2.log resources 0

### Part 1 - Parse arguments.
########################################################################################################################

parser = argparse.ArgumentParser(description='Process the logfile to show how the avatar work in the maze.')
parser.add_argument('log_file', type=argparse.FileType('r'),
                    help='the log file that the program use to animate the movements of avatars')

parser.add_argument('resources', type=Path,
                    help='the picture file that contains all wall and avatar sprites as well as background image')

# There are two modes, 0 shows the maze right away, while 1 showcases the full version of our strategy.
parser.add_argument('fancy_or_not', type=int, choices=range(0, 2), default=0,
                    help='either 0 or 1, where 0 is the normal one and 1 is the fancy, show case strategy version.')

args = parser.parse_args()


### Part 2 - Initialize maze with opening the file and initializing other modules.
########################################################################################################################

pygame.init()

# Command parse
file = args.log_file
byte = 0
line = file.readline() # Disregard first line
byte+=len(line)
line = file.readline() #Difficulty 2 Avatars 3 Mazewidth 12 Mazeheight 10
byte+=len(line)
DIFFICULTY, difficulty, AVATARS, n_avatars, MAZEWIDTH, width, MAZEHEIGHT, height = line.split(" ")

n_avatars = (int)(n_avatars)

wb = (int)(width) # This is how many block there is in width, get this from log
hb = (int)(height) # This is how many block there is in height, get this from log

# Each difficulty has a different height and width, and thus the master scales need to be personalized for each difficulty.
scale = 0
move_scale = 0
if ((int)(difficulty)==0):
    scale = 160
    move_scale = 5
if ((int)(difficulty)==1):
    scale = 90
    move_scale = 2
if ((int)(difficulty)==2):
    scale = 80
    move_scale = 1
if ((int)(difficulty)==3):
    scale = 42
    move_scale = 0.4
if ((int)(difficulty)==4):
    scale = 32
    move_scale = 0.2
if ((int)(difficulty)==5):
    scale = 25
    move_scale = 0.12
if ((int)(difficulty)==6):
    scale = 24
    move_scale = 0.09
if ((int)(difficulty)==7):
    scale = 20
    move_scale = 0.07
if ((int)(difficulty)==8):
    scale = 14
    move_scale = 0.05
if ((int)(difficulty)==9):
    scale = 8
    move_scale = 0.025

w = wb * scale
h = hb * scale
bw = w/wb # This is width divided by how many blocks there are, giving the average width for each block
bh = h/hb # This is hieght divided by how many blocks there are, giving the average height for each block
window = pygame.display.set_mode((w, h))
pygame.display.set_caption('Maze')
clock = pygame.time.Clock()

# Music
pygame.mixer.pre_init(44100, -16, 2, 2048) # Setup mixer to avoid sound lag
pygame.mixer.init()
pygame.mixer.music.load("resources/hbd.mp3")
pygame.mixer.music.play(-1)

### Part 3 - Load wallpaper and sprites into pygame for use.
########################################################################################################################

# First load image, then use convert_alpha to make transparent background, and lastly use pygame.trasform.scale to scale.
def load(file, w, wb, h, hb):
    return pygame.transform.scale((pygame.image.load(file).convert_alpha()), ((int)(bw), (int)(bh)))

crumb_sprite = pygame.image.load("resources/Crumb.png").convert_alpha()
crumb_sprite = pygame.transform.scale(crumb_sprite, ((int)(bw), (int)(bh)))

goal_sprite = pygame.image.load("resources/Goal.png").convert_alpha()
goal_sprite = pygame.transform.scale(goal_sprite, ((int)(bw), (int)(bh)))

# Array of wall_sprites
WALL_SPRITES = [load("resources/wall_0.png", w, wb, h, hb), load("resources/wall_1.png", w, wb, h, hb), load("resources/wall_2.png", w, wb, h, hb), load("resources/wall_3.png", w, wb, h, hb), load("resources/wall_4.png", w, wb, h, hb), load("resources/wall_5.png", w, wb, h, hb), load("resources/wall_6.png", w, wb, h, hb), load("resources/wall_7.png", w, wb, h, hb), load("resources/wall_8.png", w, wb, h, hb), load("resources/wall_9.png", w, wb, h, hb), load("resources/wall_10.png", w, wb, h, hb), load("resources/wall_11.png", w, wb, h, hb), load("resources/wall_12.png", w, wb, h, hb), load("resources/wall_13.png", w, wb, h, hb), load("resources/wall_14.png", w, wb, h, hb), load("resources/wall_15.png", w, wb, h, hb)]

# Array of fancy_wall_sprites
FANCY_WALL_SPRITES = [load("resources/fancy_wall_0.png", w, wb, h, hb), load("resources/fancy_wall_1.png", w, wb, h, hb), load("resources/fancy_wall_2.png", w, wb, h, hb), load("resources/fancy_wall_3.png", w, wb, h, hb), load("resources/fancy_wall_4.png", w, wb, h, hb), load("resources/fancy_wall_5.png", w, wb, h, hb), load("resources/fancy_wall_6.png", w, wb, h, hb), load("resources/fancy_wall_7.png", w, wb, h, hb), load("resources/fancy_wall_8.png", w, wb, h, hb), load("resources/fancy_wall_9.png", w, wb, h, hb), load("resources/fancy_wall_10.png", w, wb, h, hb), load("resources/fancy_wall_11.png", w, wb, h, hb), load("resources/fancy_wall_12.png", w, wb, h, hb), load("resources/fancy_wall_13.png", w, wb, h, hb), load("resources/fancy_wall_14.png", w, wb, h, hb), load("resources/fancy_wall_15.png", w, wb, h, hb)]

def load_avatar(file, w, wb, h, hb):
    return pygame.transform.scale((pygame.image.load(file).convert_alpha()), ((int)(bw * 0.7), (int)(bh * 0.7)))

# Array of avatars_sprites
AVATARS_SPRITE = [load_avatar("resources/Princey_sad.png", w, wb, h, hb), load_avatar("resources/Mindy_sad.png", w, wb, h, hb), load_avatar("resources/Tommy_sad.png", w, wb, h, hb), load_avatar("resources/Sarah_sad.png", w, wb, h, hb), load_avatar("resources/Crystian_sad.png", w, wb, h, hb), load_avatar("resources/Sam_sad.png", w, wb, h, hb), load_avatar("resources/Aadil_sad.png", w, wb, h, hb), load_avatar("resources/Vanellope_sad.png", w, wb, h, hb), load_avatar("resources/Chase_sad.png", w, wb, h, hb), load_avatar("resources/Zoe_sad.png", w, wb, h, hb), ]

# Array of avatars_sprites_Happy
AVATARS_SPRITE_HAPPY = [load_avatar("resources/Princey_happy.png", w, wb, h, hb), load_avatar("resources/Mindy_happy.png", w, wb, h, hb), load_avatar("resources/Tommy_happy.png", w, wb, h, hb), load_avatar("resources/Sarah_happy.png", w, wb, h, hb), load_avatar("resources/Crystian_happy.png", w, wb, h, hb), load_avatar("resources/Sam_happy.png", w, wb, h, hb), load_avatar("resources/Aadil_happy.png", w, wb, h, hb), load_avatar("resources/Vanellope_happy.png", w, wb, h, hb), load_avatar("resources/Chase_happy.png", w, wb, h, hb), load_avatar("resources/Zoe_happy.png", w, wb, h, hb), ]

def load_bg(file, w, h):
    return pygame.transform.scale((pygame.image.load(file).convert()), (w, h))

# Array of all wallpaper pictures
WALLPAPER_PICS = [load_bg("resources/wallpaper_0.tiff", w, h), load_bg("resources/wallpaper_1.jpg", w, h), load_bg("resources/wallpaper_2.png", w, h), load_bg("resources/wallpaper_3.jpg", w, h), load_bg("resources/wallpaper_4.jpg", w, h), load_bg("resources/wallpaper_5.png", w, h), load_bg("resources/wallpaper_6.png", w, h), load_bg("resources/wallpaper_7.jpg", w, h), load_bg("resources/wallpaper_8.png", w, h), load_bg("resources/wallpaper_9.png", w, h), load_bg("resources/wallpaper_10.jpg", w, h), load_bg("resources/wallpaper_11.png", w, h)]

# Pause function for Gameover Scene
def paused(movesnumber):
    color = (250, 250, 100)
    fontsize = 100
    if ((int)(difficulty) == 1):
        fontsize = 60
    font = pygame.font.Font("resources/StardustAdventure.ttf", fontsize)
    text1 = font.render('CONGRATULATIONS!', True, color)
    text1Rect = text1.get_rect()
    text1Rect.center = (w // 2, h // 2)
    window.blit(text1, text1Rect)

    color = (250, 250, 100)
    font = pygame.font.Font("resources/StardustAdventure.ttf", 80)
    intstr = str(movesnumber)
    text2 = font.render("MOVES: " + intstr, True, color)
    text2Rect = text2.get_rect()
    text2Rect.center = (w // 2, h // 2 + h/8)
    window.blit(text2, text2Rect)

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(15)

### Part 4 - Use the sprites and wallpapers and blit onto the screen (currently putting it on temporary background).
########################################################################################################################

# Fill background once
background = pygame.Surface(window.get_size())
background = background.convert()
background.blit(WALLPAPER_PICS[6], (0, 0)) # This is the most clear background, good for checking functionality

# Creates a list containing h lists, each of w items, all set to 0.
MazeWalls = [[0 for x in range(hb)] for y in range(wb)]

# Hard code maze level 0 - 2, using user 0 option can see the maze directly:
if (args.fancy_or_not == 0):

    # Difficulty level 0
    if ((int)(difficulty) == 0):
        # Maze 0 - WB: 5 HB: 5
        MazeWalls[0][0] = WALL_SPRITES[11]
        MazeWalls[1][0] = WALL_SPRITES[9]
        MazeWalls[2][0] = WALL_SPRITES[1]
        MazeWalls[3][0] = WALL_SPRITES[5]
        MazeWalls[4][0] = WALL_SPRITES[3] # End of row 0
        MazeWalls[0][1] = WALL_SPRITES[12]
        MazeWalls[1][1] = WALL_SPRITES[6]
        MazeWalls[2][1] = WALL_SPRITES[10]
        MazeWalls[3][1] = WALL_SPRITES[11]
        MazeWalls[4][1] = WALL_SPRITES[14] # End of row 1
        MazeWalls[0][2] = WALL_SPRITES[9]
        MazeWalls[1][2] = WALL_SPRITES[5]
        MazeWalls[2][2] = WALL_SPRITES[6]
        MazeWalls[3][2] = WALL_SPRITES[12]
        MazeWalls[4][2] = WALL_SPRITES[3] # End of row 2
        MazeWalls[0][3] = WALL_SPRITES[8]
        MazeWalls[1][3] = WALL_SPRITES[3]
        MazeWalls[2][3] = WALL_SPRITES[9]
        MazeWalls[3][3] = WALL_SPRITES[5]
        MazeWalls[4][3] = WALL_SPRITES[6] # End of row 3
        MazeWalls[0][4] = WALL_SPRITES[14]
        MazeWalls[1][4] = WALL_SPRITES[12]
        MazeWalls[2][4] = WALL_SPRITES[4]
        MazeWalls[3][4] = WALL_SPRITES[5]
        MazeWalls[4][4] = WALL_SPRITES[7] # End of row 4

        # Draw walls on background once
        for y in range(0, hb):
            for x in range(0, wb):
                background.blit(MazeWalls[x][y], (x * bw, y * bh))

    # Difficulty level 1
    if ((int)(difficulty) == 1):
        # Maze 1 - WB: 6 HB: 9
        MazeWalls[0][0] = WALL_SPRITES[11]
        MazeWalls[1][0] = WALL_SPRITES[9]
        MazeWalls[2][0] = WALL_SPRITES[1]
        MazeWalls[3][0] = WALL_SPRITES[7]
        MazeWalls[4][0] = WALL_SPRITES[9]
        MazeWalls[5][0] = WALL_SPRITES[3]  # End of row 0
        MazeWalls[0][1] = WALL_SPRITES[10]
        MazeWalls[1][1] = WALL_SPRITES[10]
        MazeWalls[2][1] = WALL_SPRITES[12]
        MazeWalls[3][1] = WALL_SPRITES[5]
        MazeWalls[4][1] = WALL_SPRITES[6]
        MazeWalls[5][1] = WALL_SPRITES[10]  # End of row 1
        MazeWalls[0][2] = WALL_SPRITES[8]
        MazeWalls[1][2] = WALL_SPRITES[4]
        MazeWalls[2][2] = WALL_SPRITES[3]
        MazeWalls[3][2] = WALL_SPRITES[13]
        MazeWalls[4][2] = WALL_SPRITES[3]
        MazeWalls[5][2] = WALL_SPRITES[10]  # End of row 2
        MazeWalls[0][3] = WALL_SPRITES[10]
        MazeWalls[1][3] = WALL_SPRITES[11]
        MazeWalls[2][3] = WALL_SPRITES[12]
        MazeWalls[3][3] = WALL_SPRITES[5]
        MazeWalls[4][3] = WALL_SPRITES[6]
        MazeWalls[5][3] = WALL_SPRITES[10]  # End of row 3
        MazeWalls[0][4] = WALL_SPRITES[10]
        MazeWalls[1][4] = WALL_SPRITES[12]
        MazeWalls[2][4] = WALL_SPRITES[5]
        MazeWalls[3][4] = WALL_SPRITES[3]
        MazeWalls[4][4] = WALL_SPRITES[9]
        MazeWalls[5][4] = WALL_SPRITES[6]  # End of row 4
        MazeWalls[0][5] = WALL_SPRITES[10]
        MazeWalls[1][5] = WALL_SPRITES[9]
        MazeWalls[2][5] = WALL_SPRITES[3]
        MazeWalls[3][5] = WALL_SPRITES[10]
        MazeWalls[4][5] = WALL_SPRITES[12]
        MazeWalls[5][5] = WALL_SPRITES[3]  # End of row 5
        MazeWalls[0][6] = WALL_SPRITES[12]
        MazeWalls[1][6] = WALL_SPRITES[6]
        MazeWalls[2][6] = WALL_SPRITES[10]
        MazeWalls[3][6] = WALL_SPRITES[10]
        MazeWalls[4][6] = WALL_SPRITES[9]
        MazeWalls[5][6] = WALL_SPRITES[6]  # End of row 6
        MazeWalls[0][7] = WALL_SPRITES[9]
        MazeWalls[1][7] = WALL_SPRITES[3]
        MazeWalls[2][7] = WALL_SPRITES[10]
        MazeWalls[3][7] = WALL_SPRITES[12]
        MazeWalls[4][7] = WALL_SPRITES[6]
        MazeWalls[5][7] = WALL_SPRITES[11]  # End of row 7
        MazeWalls[0][8] = WALL_SPRITES[14]
        MazeWalls[1][8] = WALL_SPRITES[12]
        MazeWalls[2][8] = WALL_SPRITES[4]
        MazeWalls[3][8] = WALL_SPRITES[5]
        MazeWalls[4][8] = WALL_SPRITES[5]
        MazeWalls[5][8] = WALL_SPRITES[6]  # End of row 8

        # Draw walls on background once
        for y in range(0, hb):
            for x in range(0, wb):
                background.blit(MazeWalls[x][y], (x * bw, y * bh))

    # Difficulty level 2
    if ((int)(difficulty) == 2):
        # Maze 2 - WB: 12 HB: 10
        MazeWalls[0][0] = WALL_SPRITES[13]
        MazeWalls[1][0] = WALL_SPRITES[1]
        MazeWalls[2][0] = WALL_SPRITES[5]
        MazeWalls[3][0] = WALL_SPRITES[5]
        MazeWalls[4][0] = WALL_SPRITES[3]
        MazeWalls[5][0] = WALL_SPRITES[11]
        MazeWalls[6][0] = WALL_SPRITES[9]
        MazeWalls[7][0] = WALL_SPRITES[5]
        MazeWalls[8][0] = WALL_SPRITES[1]
        MazeWalls[9][0] = WALL_SPRITES[5]
        MazeWalls[10][0] = WALL_SPRITES[3]
        MazeWalls[11][0] = WALL_SPRITES[11]  # End of row 0
        MazeWalls[0][1] = WALL_SPRITES[9]
        MazeWalls[1][1] = WALL_SPRITES[6]
        MazeWalls[2][1] = WALL_SPRITES[9]
        MazeWalls[3][1] = WALL_SPRITES[3]
        MazeWalls[4][1] = WALL_SPRITES[12]
        MazeWalls[5][1] = WALL_SPRITES[6]
        MazeWalls[6][1] = WALL_SPRITES[10]
        MazeWalls[7][1] = WALL_SPRITES[11]
        MazeWalls[8][1] = WALL_SPRITES[10]
        MazeWalls[9][1] = WALL_SPRITES[11]
        MazeWalls[10][1] = WALL_SPRITES[12]
        MazeWalls[11][1] = WALL_SPRITES[2]   # End of row 1
        MazeWalls[0][2] = WALL_SPRITES[8]
        MazeWalls[1][2] = WALL_SPRITES[5]
        MazeWalls[2][2] = WALL_SPRITES[6]
        MazeWalls[3][2] = WALL_SPRITES[12]
        MazeWalls[4][2] = WALL_SPRITES[5]
        MazeWalls[5][2] = WALL_SPRITES[5]
        MazeWalls[6][2] = WALL_SPRITES[4]
        MazeWalls[7][2] = WALL_SPRITES[6]
        MazeWalls[8][2] = WALL_SPRITES[10]
        MazeWalls[9][2] = WALL_SPRITES[8]
        MazeWalls[10][2] = WALL_SPRITES[3]
        MazeWalls[11][2] = WALL_SPRITES[10]   # End of row 2
        MazeWalls[0][3] = WALL_SPRITES[10]
        MazeWalls[1][3] = WALL_SPRITES[9]
        MazeWalls[2][3] = WALL_SPRITES[3]
        MazeWalls[3][3] = WALL_SPRITES[9]
        MazeWalls[4][3] = WALL_SPRITES[3]
        MazeWalls[5][3] = WALL_SPRITES[9]
        MazeWalls[6][3] = WALL_SPRITES[3]
        MazeWalls[7][3] = WALL_SPRITES[9]
        MazeWalls[8][3] = WALL_SPRITES[6]
        MazeWalls[9][3] = WALL_SPRITES[14]
        MazeWalls[10][3] = WALL_SPRITES[12]
        MazeWalls[11][3] = WALL_SPRITES[2]   # End of row 3
        MazeWalls[0][4] = WALL_SPRITES[12]
        MazeWalls[1][4] = WALL_SPRITES[6]
        MazeWalls[2][4] = WALL_SPRITES[12]
        MazeWalls[3][4] = WALL_SPRITES[6]
        MazeWalls[4][4] = WALL_SPRITES[12]
        MazeWalls[5][4] = WALL_SPRITES[6]
        MazeWalls[6][4] = WALL_SPRITES[10]
        MazeWalls[7][4] = WALL_SPRITES[12]
        MazeWalls[8][4] = WALL_SPRITES[5]
        MazeWalls[9][4] = WALL_SPRITES[5]
        MazeWalls[10][4] = WALL_SPRITES[3]
        MazeWalls[11][4] = WALL_SPRITES[10]   # End of row 4
        MazeWalls[0][5] = WALL_SPRITES[9]
        MazeWalls[1][5] = WALL_SPRITES[7]
        MazeWalls[2][5] = WALL_SPRITES[9]
        MazeWalls[3][5] = WALL_SPRITES[5]
        MazeWalls[4][5] = WALL_SPRITES[5]
        MazeWalls[5][5] = WALL_SPRITES[3]
        MazeWalls[6][5] = WALL_SPRITES[10]
        MazeWalls[7][5] = WALL_SPRITES[9]
        MazeWalls[8][5] = WALL_SPRITES[5]
        MazeWalls[9][5] = WALL_SPRITES[3]
        MazeWalls[10][5] = WALL_SPRITES[10]
        MazeWalls[11][5] = WALL_SPRITES[10]   # End of row 5
        MazeWalls[0][6] = WALL_SPRITES[8]
        MazeWalls[1][6] = WALL_SPRITES[5]
        MazeWalls[2][6] = WALL_SPRITES[6]
        MazeWalls[3][6] = WALL_SPRITES[9]
        MazeWalls[4][6] = WALL_SPRITES[3]
        MazeWalls[5][6] = WALL_SPRITES[8]
        MazeWalls[6][6] = WALL_SPRITES[6]
        MazeWalls[7][6] = WALL_SPRITES[10]
        MazeWalls[8][6] = WALL_SPRITES[9]
        MazeWalls[9][6] = WALL_SPRITES[6]
        MazeWalls[10][6] = WALL_SPRITES[10]
        MazeWalls[11][6] = WALL_SPRITES[10]   # End of row 6
        MazeWalls[0][7] = WALL_SPRITES[12]
        MazeWalls[1][7] = WALL_SPRITES[5]
        MazeWalls[2][7] = WALL_SPRITES[3]
        MazeWalls[3][7] = WALL_SPRITES[10]
        MazeWalls[4][7] = WALL_SPRITES[10]
        MazeWalls[5][7] = WALL_SPRITES[14]
        MazeWalls[6][7] = WALL_SPRITES[9]
        MazeWalls[7][7] = WALL_SPRITES[6]
        MazeWalls[8][7] = WALL_SPRITES[10]
        MazeWalls[9][7] = WALL_SPRITES[13]
        MazeWalls[10][7] = WALL_SPRITES[2]
        MazeWalls[11][7] = WALL_SPRITES[12]   # End of row 7
        MazeWalls[0][8] = WALL_SPRITES[11]
        MazeWalls[1][8] = WALL_SPRITES[9]
        MazeWalls[2][8] = WALL_SPRITES[6]
        MazeWalls[3][8] = WALL_SPRITES[10]
        MazeWalls[4][8] = WALL_SPRITES[12]
        MazeWalls[5][8] = WALL_SPRITES[5]
        MazeWalls[6][8] = WALL_SPRITES[6]
        MazeWalls[7][8] = WALL_SPRITES[11]
        MazeWalls[8][8] = WALL_SPRITES[12]
        MazeWalls[9][8] = WALL_SPRITES[3]
        MazeWalls[10][8] = WALL_SPRITES[12]
        MazeWalls[11][8] = WALL_SPRITES[3]   # End of row 8
        MazeWalls[0][9] = WALL_SPRITES[12]
        MazeWalls[1][9] = WALL_SPRITES[4]
        MazeWalls[2][9] = WALL_SPRITES[7]
        MazeWalls[3][9] = WALL_SPRITES[12]
        MazeWalls[4][9] = WALL_SPRITES[5]
        MazeWalls[5][9] = WALL_SPRITES[5]
        MazeWalls[6][9] = WALL_SPRITES[5]
        MazeWalls[7][9] = WALL_SPRITES[6]
        MazeWalls[8][9] = WALL_SPRITES[13]
        MazeWalls[9][9] = WALL_SPRITES[4]
        MazeWalls[10][9] = WALL_SPRITES[5]
        MazeWalls[11][9] = WALL_SPRITES[6]   # End of row 9

        # Draw walls on background once
        for y in range(0, hb):
            for x in range(0, wb):
                background.blit(MazeWalls[x][y], (x * bw, y * bh))

else:
    # Initialize vertical borders
    for y in range(0, hb):
        background.blit(WALL_SPRITES[8], (0, y * bh)) # West borders
        background.blit(WALL_SPRITES[2], (w - bw, y * bh)) # East borders

    # Initialize horizontal borders
    for x in range(0, wb):
        background.blit(WALL_SPRITES[1], (x * bw, 0)) # North borders
        background.blit(WALL_SPRITES[4], (x * bw, h - bh)) # South borders

# Blit everything to the screen
window.blit(background, (0, 0))

### Part 5 - Initialize avatars by reading 1 line and returning the first line.
########################################################################################################################

move_x_avatar = arr.array('d', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
move_y_avatar = arr.array('d', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

# Initialize avatars' x y positions using first move line
line = file.readline()
if (line.startswith("MOVE") == True):
    commandArray = line.split()
    r = range(3, len(commandArray))
    avatarNumberFloat = (len(commandArray) - 3) / 2

    # Create a 2D array for movements and comparison
    compareArray = [[0 for x in range(2)] for y in range((int)(avatarNumberFloat + 1))]

    for x in r:
        if (x % 2 == 1):
            avatarNumber = (int)(x / 2) - 1  # Avatar number
            compareArray[avatarNumber][0] = commandArray[x]
            compareArray[avatarNumber][1] = commandArray[x + 1]

    # Update each avatar's x movement
    for i in range(0, n_avatars):
        move_x_avatar[i] = (int)(compareArray[i][0])

    # Update each avatar's y movement
    for i in range(0, n_avatars):
        move_y_avatar[i] = (int)(compareArray[i][1])

# Back to first line.
file.seek(byte)

### Part 6 - begin actual while loop to read through each line of movements in log file
########################################################################################################################
while True:

    # Read line to see what to do with it
    line = file.readline()

    if (line.startswith("MOVE")):

        byte+=len(line) # Store the line that we left off from so we can come back to start the loop again and read next line
        next_line = file.readline() #

        ##### End program when there's nothing in next line ##### 
        if (next_line.startswith("MAZE")):
            MAZE, SOLVED, DIFFICULTY, dnumber, AVATARS, anumber, MOVES, movesnumber, HASH, hashn = next_line.split(" ")
            pause = True
            paused(movesnumber) # Game over congratulations scene

        # Compare with the next line that actually starts with move
        while(next_line.startswith("MOVE")!=True):
            next_line = file.readline()

        ##### Parsing Command for Avatar Movements #####
        commandArray = line.split()
        r = range(3, len(commandArray))
        avatarNumberFloat = (len(commandArray) - 3) / 2

        # Create a 2D array for movements and comparison
        compareArray = [[0 for x in range(2)] for y in range((int)(avatarNumberFloat + 1))]

        for x in r:
            if (x % 2 == 1):
                avatarNumber = (int)(x / 2) - 1  # Avatar number
                compareArray[avatarNumber][0] = commandArray[x]
                compareArray[avatarNumber][1] = commandArray[x + 1]

        ##### Parsing command ##### 
        commandArray2 = next_line.split()
        r = range(3, len(commandArray2))
        avatarNumberFloat = (len(commandArray2) - 3) / 2

        for x in r:
            if (x % 2 == 1):
                avatarNumber = (int)(x / 2) - 1

                if (compareArray[avatarNumber][0] != commandArray2[x]):
                    compareArray[avatarNumber][0] = commandArray2[x]

                    # Update each avatar's x location
                    for i in range(0, n_avatars):
                        move_x_avatar[i] = (int)(compareArray[i][0])

                if (compareArray[avatarNumber][1] != commandArray2[x + 1]):
                    compareArray[avatarNumber][1] = commandArray2[x + 1]

                    # Update each avatar's y location
                    for i in range(0, n_avatars):
                        move_y_avatar[i] = (int)(compareArray[i][1])

        # Go back to the line that's skipped because of reading next_line but still needs to be compared
        file.seek(byte)

    ##### If line starts with Wall, add wall
    elif (line.startswith("WALL")):
        # If user wants it to be a fancy program, do this:
        if (args.fancy_or_not == 1):
            character, type, x, y, wall_number = line.split(" ")

            # Add normal wall
            if (type == "FOUND"):
                MazeWalls[(int)(x)][(int)(y)] = WALL_SPRITES[(int)(wall_number)]
                background.blit(MazeWalls[(int)(x)][(int)(y)], ((int)(x) * bw, (int)(y) * bh))

            # Add fancy wall
            if (type == "ADDED"):
                MazeWalls[(int)(x)][(int)(y)] = FANCY_WALL_SPRITES[(int)(wall_number)]
                background.blit(MazeWalls[(int)(x)][(int)(y)], ((int)(x) * bw, (int)(y) * bh))

        # If user doesn't want it to be a fancy program, simply add normal wall
        else:
            character, type, x, y, wall_number = line.split(" ")
            MazeWalls[(int)(x)][(int)(y)] = WALL_SPRITES[(int)(wall_number)]
            background.blit(MazeWalls[(int)(x)][(int)(y)], ((int)(x) * bw, (int)(y) * bh))

    ##### If line starts with crumb, add crumb
    elif (line.startswith("CRUMB")):
        if (args.fancy_or_not == 1):
            character, x, y = line.split(" ")
            MazeWalls[(int)(x)][(int)(y)] = crumb_sprite
            background.blit(MazeWalls[(int)(x)][(int)(y)], ((int)(x) * bw, (int)(y) * bh))

    ##### If line starts with crumb, add crumb
    elif (line.startswith("GOAL")):
        if (args.fancy_or_not == 1):
            character, x, y = line.split(" ")
            MazeWalls[(int)(x)][(int)(y)] = goal_sprite
            background.blit(MazeWalls[(int)(x)][(int)(y)], ((int)(x) * bw, (int)(y) * bh))

    ##### Update the screen (FINALLY.)
    ##############################################################################################################

    # Blit everything to the screen
    window.blit(background, (0, 0))
    PRESENT_SPRITES = [None] * 10

    # Update each avatar's locations
    for i in range(0, n_avatars):
        for j in range(0, n_avatars):
            if (j != i):
                if ((move_x_avatar[i] == move_x_avatar[j]) and (move_y_avatar[i] == move_y_avatar[j])):
                    PRESENT_SPRITES[i] = AVATARS_SPRITE_HAPPY[i]
                    PRESENT_SPRITES[j] = AVATARS_SPRITE_HAPPY[j]
                elif ((move_x_avatar[i] == move_x_avatar[j] + 1) and (move_y_avatar[i] == move_y_avatar[j])):
                    PRESENT_SPRITES[i] = AVATARS_SPRITE_HAPPY[i]
                    PRESENT_SPRITES[j] = AVATARS_SPRITE_HAPPY[j]
                elif ((move_x_avatar[i] == move_x_avatar[j] - 1) and (move_y_avatar[i] == move_y_avatar[j])):
                    PRESENT_SPRITES[i] = AVATARS_SPRITE_HAPPY[i]
                    PRESENT_SPRITES[j] = AVATARS_SPRITE_HAPPY[j]
                elif ((move_x_avatar[i] == move_x_avatar[j]) and (move_y_avatar[i] == move_y_avatar[j] + 1)):
                    PRESENT_SPRITES[i] = AVATARS_SPRITE_HAPPY[i]
                    PRESENT_SPRITES[j] = AVATARS_SPRITE_HAPPY[j]
                elif ((move_x_avatar[i] == move_x_avatar[j]) and (move_y_avatar[i] == move_y_avatar[j] - 1)):
                    PRESENT_SPRITES[i] = AVATARS_SPRITE_HAPPY[i]
                    PRESENT_SPRITES[j] = AVATARS_SPRITE_HAPPY[j]
                else:
                    if (PRESENT_SPRITES[i] == None):
                        PRESENT_SPRITES[i] = AVATARS_SPRITE[i]

    for i in range(0, n_avatars):
        window.blit(PRESENT_SPRITES[i], (move_x_avatar[i] * bw + move_scale * wb, move_y_avatar[i] * bh + move_scale * hb))

    pygame.display.update()
    clock.tick(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

pygame.quit()
quit()
