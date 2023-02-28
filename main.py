# Import libraries
import pygame
import sys
import game
from celestial_body import CelestialBody
from time import perf_counter

pygame.init()

game.OBJECTS.append(CelestialBody(game.WIDTH / 4, game.HEIGHT/2, (0, 0), 100, 20))
game.OBJECTS.append(CelestialBody(game.WIDTH*3 / 4, game.HEIGHT/2, (0, 0), 100, 20))

running = True

def draw_screen(delta_time):
    game.WIN.fill((0, 0, 0))

    for object in game.OBJECTS:
        object.update(delta_time)
        object.draw()

    pygame.display.update()

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

        elif event.type == pygame.QUIT:
            quit()

    end_time = perf_counter()
    delta_time = end_time - start_time