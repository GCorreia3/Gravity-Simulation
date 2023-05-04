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

START_MASS = 100


fps_font = pygame.font.SysFont("bahnschrift", 20)
title_font = pygame.font.SysFont("Calibri", 40)
text_font = pygame.font.SysFont("Calibri", 20)

# Function to use across files
def get_dist(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5