import pygame
import game
import math
from custom_maths import Vector2D



class VectorArrow():
    def __init__(self, position: Vector2D, direction: Vector2D, magnitude, width, colour) -> None:
        self.position = position
        self.direction = direction
        self.magnitude = magnitude
        self.width = width
        self.colour = colour

    def update(self, pos, dir, mag):
        self.position = pos
        self.direction = dir
        self.magnitude = mag

    def draw(self):
        end_pos: Vector2D = self.position + self.direction * self.magnitude

        # Draw initial line
        pygame.draw.line(game.WIN, self.colour, (self.position.x, self.position.y), (end_pos.x, end_pos.y), self.width)

        # Draw arrow head
        right_arrow_pos = end_pos + self.direction.rotate(3*math.pi/4) * self.magnitude/5
        pygame.draw.line(game.WIN, self.colour, (end_pos.x, end_pos.y), (right_arrow_pos.x, right_arrow_pos.y), self.width)

        left_arrow_pos = end_pos + self.direction.rotate(-3*math.pi/4) * self.magnitude/5
        pygame.draw.line(game.WIN, self.colour, (end_pos.x, end_pos.y), (left_arrow_pos.x, left_arrow_pos.y), self.width)