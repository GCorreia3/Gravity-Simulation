import pygame
import game
from celestial_body import CelestialBody
from custom_maths import Vector2D
import math



class SpawnBinaryInterface():
    def __init__(self, position: Vector2D, width, height) -> None:
        self.position: Vector2D = position
        self.width = width
        self.height = height

        self.open = False

        self.spawn_button = Button(Vector2D(game.WIDTH/2, game.HEIGHT/2 + self.height/2 - 50), 200, 50, "Spawn", (100, 100, 100))

        self.mass1 = 1000
        self.mass1_slider = Slider(Vector2D(game.WIDTH/2, game.HEIGHT/2 - 100), 300, 20, 50, 10000, self.mass1, "Mass 1", (30, 30, 30), (255, 255, 255))

        self.mass2 = 1000
        self.mass2_slider = Slider(Vector2D(game.WIDTH/2, game.HEIGHT/2), 300, 20, 50, 10000, self.mass2, "Mass 2", (30, 30, 30), (255, 255, 255))

        self.distance = 300
        self.distance_slider = Slider(Vector2D(game.WIDTH/2, game.HEIGHT/2 + 100), 300, 20, 100, 1000, self.distance, "Distance", (30, 30, 30), (255, 255, 255))

        self.sliders = [self.mass1_slider, self.mass2_slider, self.distance_slider]

    def check_click(self, mouse):
        for slider in self.sliders:
            distance = game.get_dist(mouse[0], mouse[1], slider.value_to_pos(slider.value).x, slider.value_to_pos(slider.value).y)

            if distance < 20:
                slider.dragging = True

                slider.drag_offset = Vector2D(slider.value_to_pos(slider.value).x - mouse[0], 0)
                return

        if abs(mouse[0] - self.spawn_button.position.x) <= self.spawn_button.width/2 and abs(mouse[1] - self.spawn_button.position.y) <= self.spawn_button.height/2:
            self.spawn_binary(self.mass1, self.mass2, self.distance)
            self.open = False

    def check_dragging(self, mouse):
        for slider in self.sliders:
            if slider.dragging:
                slider.drag(mouse)
                return

    def release_drag(self):
        for slider in self.sliders:
            if slider.dragging:
                slider.dragging = False

    def spawn_binary(self, m1, m2, r):
        x1 = (m2 * r) / (m1 + m2)
        x2 = (m1 * r) / (m1 + m2)

        v1 = math.sqrt((game.G * m1 * m2 * x1) / (m1 * r**2))
        #v1 = 25
        p1 = v1 * m1
        p2 = -p1
        v2 = p2 / m2

        object1 = CelestialBody(Vector2D(-x1 + (game.WIDTH / 2), game.HEIGHT / 2), Vector2D(0, v1), m1)
        object2 = CelestialBody(Vector2D(x2 + (game.WIDTH / 2), game.HEIGHT / 2), Vector2D(0, v2), m2)

        game.CENTRE_OF_MASS = (m1, m2, object1.position, object2.position)

        game.OBJECTS.append(object1)
        game.OBJECTS.append(object2)
    
    def update(self):
        self.mass1 = int(self.mass1_slider.value)
        self.mass2 = int(self.mass2_slider.value)
        self.distance = int(self.distance_slider.value)

    def draw(self):
        if not self.open: return

        # Draw background rectangle
        pygame.draw.rect(game.WIN, (25, 25, 30), (self.position.x - self.width/2, self.position.y - self.height/2, self.width, self.height))

        # Draw Title
        title_surface = game.title_font.render("Spawn Binary Menu", True, (255, 255, 255))
        game.WIN.blit(title_surface, (self.position.x - title_surface.get_width()/2, self.position.y - self.height/2 + title_surface.get_height()/2))

        # Draw sliders
        for slider in self.sliders:
            slider.draw()

        # Draw spawn button
        self.spawn_button.draw()


class Slider():
    def __init__(self, position: Vector2D, width, height, min_value, max_value, default_value, name_text, background_colour, slider_colour) -> None:
        self.position: Vector2D = position
        self.width = width
        self.height = height

        self.min_value = min_value
        self.max_value = max_value
        self.value_range = self.max_value - self.min_value

        self.name_text = name_text

        self.background_colour = background_colour
        self.slider_colour = slider_colour

        self.value = default_value

        self.dragging = False
        self.drag_offset: Vector2D = Vector2D(0, 0)

    def value_to_width(self, value):
       value_ratio = (value - self.min_value) / (self.max_value - self.min_value)
       return value_ratio * self.width
    
    def value_to_pos(self, value):
        pixel_width = self.value_to_width(value)

        dist_from_centre = pixel_width - self.width/2

        return Vector2D(self.position.x + dist_from_centre, self.position.y)
    
    def pos_to_value(self, pos):
        x_difference = pos[0] - self.value_to_pos(self.min_value).x + self.drag_offset.x
        value = (x_difference / self.width) * self.value_range

        value += self.min_value

        return min(self.max_value, max(self.min_value, value))
    
    def drag(self, mouse):
        self.value = self.pos_to_value(mouse)

    def draw(self):
        # Draw background rectangle
        pygame.draw.rect(game.WIN, self.background_colour, (self.position.x - self.width/2, self.position.y - self.height/2, self.width, self.height))

        # Draw slider
        pygame.draw.rect(game.WIN, self.slider_colour, (self.position.x - self.width/2, self.position.y - self.height/2, self.value_to_width(self.value), self.height))

        # Draw handle
        pygame.draw.circle(game.WIN, self.slider_colour, self.value_to_pos(self.value).to_coordinate(), 1.5 * self.height/2)

        # Draw value text
        text_surface = game.text_font.render(f"{round(self.value)}", True, (255, 255, 255))
        game.WIN.blit(text_surface, (self.value_to_pos(self.value) - Vector2D(text_surface.get_width()/2, 50)).to_coordinate())

        # Draw name text
        name_surface = game.text_font.render(self.name_text, True, (255, 255, 255))
        game.WIN.blit(name_surface, (self.position.x - self.width/2 - name_surface.get_width() - 30, self.position.y - name_surface.get_height()/2))



class Button():
    def __init__(self, position: Vector2D, width, height, text, background_colour) -> None:
        self.position: Vector2D = position
        self.width = width
        self.height = height

        self.text = text

        self.background_colour = background_colour

    def draw(self):
        # Draw background rectangle
        pygame.draw.rect(game.WIN, self.background_colour, (self.position.x - self.width/2, self.position.y - self.height/2, self.width, self.height))

        # Draw button text
        text_surface = game.text_font.render(self.text, True, (255, 255, 255))
        game.WIN.blit(text_surface, (self.position.x - text_surface.get_width()/2, self.position.y - text_surface.get_height()/2))
