# This is the main function which has the main loop running in it. For all the scripts to work, you must run this python file

# Import libraries
import pygame
import sys
import game
from celestial_body import CelestialBody
from custom_maths import Vector2D
from time import perf_counter
import math
import copy

pygame.init() # Initialises pygame (only needs to be done once)

running = True
paused = True

start_mouse_pos = (0, 0)
end_mouse_pos = (0, 0)

is_pressed = False

calculating_trajectory = False

positions = list()

# Function which is called every frame to draw the objects
def draw_screen(positions):
    game.WIN.fill((0, 0, 0)) # fills screen with colour

    for particle in game.PARTICLES:
        particle.draw()

    # Loops through objects which are in the game list
    for object in game.OBJECTS:
        object.draw()

    if game.CENTRE_OF_MASS:
        com = centre_of_mass(game.CENTRE_OF_MASS[0], game.CENTRE_OF_MASS[1], game.CENTRE_OF_MASS[2], game.CENTRE_OF_MASS[3])
        pygame.draw.circle(game.WIN, (100, 100, 100), (com.x, com.y), 2)

    if is_pressed:
        pygame.draw.line(game.WIN, (0, 0, 255), start_mouse_pos, end_mouse_pos, 4)
        pygame.draw.circle(game.WIN, (255, 0, 0), start_mouse_pos, (game.START_MASS / math.pi)**0.5)

    for i, pos in enumerate(positions):
        if i < len(positions) - 1:
            pygame.draw.line(game.WIN, (255, 255, 255), (pos.x, pos.y), (positions[i+1].x, positions[i+1].y), 2)

    pygame.display.update() # This just updates the screen


def update_objects(delta_time):
    for particle in game.PARTICLES:
        if not paused:
            particle.update(delta_time)

    for object in game.OBJECTS:
        if not paused:
            object.update(delta_time)


def update_trajectory(delta_time, positions):
    if is_pressed:
        if calculating_trajectory:
            object = CelestialBody(Vector2D(start_mouse_pos[0], start_mouse_pos[1]), Vector2D(end_mouse_pos[0] - start_mouse_pos[0], end_mouse_pos[1] - start_mouse_pos[1]), game.START_MASS)
            game.TRAJECTORY_OBJECTS = copy.deepcopy(game.OBJECTS)
            game.TRAJECTORY_OBJECTS.append(object)
            for i in range(2000):
                for i, o in enumerate(game.TRAJECTORY_OBJECTS):
                    o.position = iterate_pos(delta_time, o)
                    if i == len(game.TRAJECTORY_OBJECTS) - 1:
                        positions.append(copy.deepcopy(o.position))

    else:
        positions.clear()

    return positions


def iterate_pos(delta_time, object: CelestialBody):
    accelerations = []

    for o in game.TRAJECTORY_OBJECTS:
        if o != object:
                
            o: CelestialBody = o
            distance = game.get_dist(o.position.x, o.position.y, object.position.x, object.position.y)

            force = game.G * (object.mass * o.mass / (distance)**2) # Only gets the magnitude of the force

            # Gets direction from self to object
            direction = Vector2D(o.position.x - object.position.x, o.position.y - object.position.y)
            direction_magnitude = (direction.x**2 + direction.y**2)**0.5

            force_direction = Vector2D(direction.x * (force / direction_magnitude), direction.y * (force / direction_magnitude)) # Gives the force a direction with magnitude of the force magnitude calculated from newtons equation

            # a = F/ m
            accelerations.append((force_direction.x / object.mass, force_direction.y / object.mass))

    x = 0
    y = 0
    for i in range(len(accelerations)):
        x += accelerations[i][0]
        y += accelerations[i][1]

    object.acceleration = Vector2D(x, y)

    object.velocity = Vector2D(object.velocity.x + object.acceleration.x * delta_time, object.velocity.y + object.acceleration.y * delta_time)

    object.position += object.velocity * delta_time

    return object.position


def spawn_binary(m1, m2, r):
    x1 = (m2 * r) / (m1 + m2)
    x2 = (m1 * r) / (m1 + m2)

    v1 = math.sqrt((game.G * m1 * m2 * x1) / (m1 * r**2))
    p1 = v1 * m1
    p2 = -p1
    v2 = p2 / m2

    object1 = CelestialBody(Vector2D(-x1 + (game.WIDTH / 2), game.HEIGHT / 2), Vector2D(0, v1), m1)
    object2 = CelestialBody(Vector2D(x2 + (game.WIDTH / 2), game.HEIGHT / 2), Vector2D(0, v2), m2)

    game.CENTRE_OF_MASS = (m1, m2, object1.position, object2.position)

    game.OBJECTS.append(object1)
    game.OBJECTS.append(object2)


def centre_of_mass(m1, m2, pos1: Vector2D, pos2: Vector2D):
    return (pos1*m1 + pos2*m2) / (m1 + m2)


def mouse_up(start_mouse_pos, end_mouse_pos, start_mass):
    # Spawn new celestial body at the mouse position
    initial_velocity = Vector2D(end_mouse_pos[0] - start_mouse_pos[0], end_mouse_pos[1] - start_mouse_pos[1])

    game.OBJECTS.append(CelestialBody(Vector2D(start_mouse_pos[0], start_mouse_pos[1]), initial_velocity, start_mass))


def quit():
    # closes pygame and quits the application
    pygame.quit()
    sys.exit(0)

delta_time = 1

# Main loop
while running:
    # Get start time of this frame
    start_time = perf_counter()

    update_objects(delta_time)
    positions = update_trajectory(delta_time, positions)

    calculating_trajectory = False

    draw_screen(positions)

    # Loops through all of the events (there are many many types of events) that occur in this frame
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_m:
                game.OBJECTS.append(CelestialBody(Vector2D(game.WIDTH / 2, game.HEIGHT / 2), Vector2D(0, 0), 30000))

            if event.key == pygame.K_UP:
                if is_pressed:
                    game.START_MASS *= 2

            if event.key == pygame.K_DOWN:
                if is_pressed:
                    game.START_MASS *= 0.5

            if event.key == pygame.K_r:
                game.OBJECTS.clear()
                game.PARTICLES.clear()
                game.CENTRE_OF_MASS = None

            if event.key == pygame.K_b:
                spawn_binary(1000, 1000, 300)

        # Checks if the quit button in the top right is pressed on the window
        elif event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_mouse_pos = pygame.mouse.get_pos()
            is_pressed = True
            calculating_trajectory = True
        
        elif event.type == pygame.MOUSEMOTION:
            end_mouse_pos = pygame.mouse.get_pos()
            positions.clear()
            calculating_trajectory = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_up(start_mouse_pos, end_mouse_pos, game.START_MASS)
            is_pressed = False

    end_time = perf_counter() # Get end time of the frame
    delta_time = end_time - start_time # delta_time is how long it takes for each frame to compute, this can then be used to make code frame rate independent