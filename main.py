# This is the main function which has the main loop running in it. For all the scripts to work, you must run this python file

# Import libraries
import pygame
import sys
import game
from celestial_body import CelestialBody
from time import perf_counter

pygame.init() # Initialises pygame (only needs to be done once)

running = True
paused = True

# Function which is called every frame to draw and update the objects
def draw_screen(delta_time):
    game.WIN.fill((0, 0, 0)) # fills screen with colour

    # Loops through objects which are in the game list
    for object in game.OBJECTS:
        if not paused:
            # Runs the update function of the object (calculates new positions etc before then drawing it)
            object.update(delta_time)
        # Runs the draw function of the object (draws the circle)
        object.draw()

    pygame.display.update() # This just updates the screen

def mouse_down(mouse):
    x, y = mouse
    # Spawn new celestial body at the mouse position
    game.OBJECTS.append(CelestialBody(x, y, (0, 0), 100))

def quit():
    # closes pygame and quits the application
    pygame.quit()
    sys.exit(0)

delta_time = 1

# Main loop
while running:
    # Get start time of this frame
    start_time = perf_counter()

    draw_screen(delta_time)

    # Loops through all of the events (there are many many types of events) that occur in this frame
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_SPACE:
                paused = not paused

        # Checks if the quit button in the top right is pressed on the window
        elif event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            mouse_down(mouse)

    end_time = perf_counter() # Get end time of the frame
    delta_time = end_time - start_time # delta_time is how long it takes for each frame to compute, this can then be used to make code frame rate independent