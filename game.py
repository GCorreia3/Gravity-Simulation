# This file is for constants or for anything which all files could need. Having a file like this reduces circular import issues

import pygame

WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.init()

# Main list of objects which you append new objects into. This is great since you are able to access this list form any file if you import game
OBJECTS = []
TRAJECTORY_OBJECTS = []
PARTICLES = []

CENTRE_OF_MASS = None

# Gravitational constant
G = 1000
C = 300#4.5e21

START_MASS = 100

DIST_PER_PIXEL = 1
ZOOM_ACCELERATION = 1

TIME_SPEED = 1

draw_arrows = True
draw_trails = True

fps_font = pygame.font.SysFont("bahnschrift", 20)
title_font = pygame.font.SysFont("Calibri", 40)
text_font = pygame.font.SysFont("Calibri", 20)

# Function to use across files
def get_dist(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def get_distance(object1, object2):
    return ((object2.x - object1.x)**2 + (object2.y - object1.y)**2)**0.5

def dist_to(pos1, pos2):
    return ((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)**0.5