import pygame
import game



class SpawnBinaryInterface():
    def __init__(self, pos, width, height) -> None:
        self.pos = pos
        self.width = width
        self.height = height

        self.open = False

    def draw(self):
        if not self.open: return

        # Draw background rectangle
        pygame.draw.rect(game.WIN, (25, 25, 30), (self.pos[0] - self.width/2, self.pos[1] - self.height/2, self.width, self.height))

        # Draw Title
        title_surface = game.title_font.render("Spawn Binary Menu", True, (255, 255, 255))
        game.WIN.blit(title_surface, (self.pos[0] - title_surface.get_width()/2, self.pos[1] - self.height/2 + title_surface.get_height()/2))

        # Draw
        