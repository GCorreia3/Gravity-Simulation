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
        if game.draw_arrows:
            end_pos: Vector2D = self.position + self.direction * self.magnitude

            # Draw initial line
            pygame.draw.line(game.WIN, self.colour, (self.position.x / game.DIST_PER_PIXEL + game.WIDTH / 2, self.position.y / game.DIST_PER_PIXEL + game.HEIGHT / 2), (end_pos.x / game.DIST_PER_PIXEL + game.WIDTH / 2, end_pos.y / game.DIST_PER_PIXEL + game.HEIGHT / 2), self.width)

            # Draw arrow head
            right_arrow_pos = end_pos + self.direction.rotate(3*math.pi/4) * self.magnitude/5
            pygame.draw.line(game.WIN, self.colour, (end_pos.x / game.DIST_PER_PIXEL + game.WIDTH / 2, end_pos.y / game.DIST_PER_PIXEL + game.HEIGHT / 2), (right_arrow_pos.x / game.DIST_PER_PIXEL + game.WIDTH / 2, right_arrow_pos.y / game.DIST_PER_PIXEL + game.HEIGHT / 2), self.width)

            left_arrow_pos = end_pos + self.direction.rotate(-3*math.pi/4) * self.magnitude/5
            pygame.draw.line(game.WIN, self.colour, (end_pos.x / game.DIST_PER_PIXEL + game.WIDTH / 2, end_pos.y / game.DIST_PER_PIXEL + game.HEIGHT / 2), (left_arrow_pos.x / game.DIST_PER_PIXEL + game.WIDTH / 2, left_arrow_pos.y / game.DIST_PER_PIXEL + game.HEIGHT / 2), self.width)