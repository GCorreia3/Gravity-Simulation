import pygame
import game



class CelestialBody():
    def __init__(self, x, y, initial_velocity, mass, radius) -> None:
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius

        self.velocity = initial_velocity

    def update(self, delta_time):
        return

    def draw(self):
        pygame.draw.circle(game.WIN, (255, 0, 0), (self.x, self.y), self.radius)