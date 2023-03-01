# Import libraries
import pygame
import sys
import game
from celestial_body import CelestialBody
from time import perf_counter
import random

pygame.init()

running = True
paused = True

def draw_screen(delta_time):
    game.WIN.fill((0, 0, 0))

    for object in game.OBJECTS:
        if not paused:
            object.update(delta_time)
        object.draw()

    pygame.display.update()

def mouse_down(mouse):
    x, y = mouse
    game.OBJECTS.append(CelestialBody(x, y, (0, 0), 100))

def quit():
    pygame.quit()
    sys.exit(0)

delta_time = 1

# Main loop
while running:
    start_time = perf_counter()

    draw_screen(delta_time)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_SPACE:
                paused = not paused

        elif event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            mouse_down(mouse)

    end_time = perf_counter()
    delta_time = end_time - start_time