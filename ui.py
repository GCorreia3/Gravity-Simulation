import pygame
import game
from celestial_body import CelestialBody, BinaryObject
from custom_maths import Vector2D
import math



class SpawnBinaryInterface():
    def __init__(self, position: Vector2D, width, height) -> None:
        self.position: Vector2D = position
        self.width = width
        self.height = height

        self.open = False

        self.mass1 = 1
        self.mass1_slider = Slider(Vector2D(game.WIDTH/2, game.HEIGHT/2 - 150), 300, 20, 0.05, 100, self.mass1, "Mass 1", (30, 30, 30), (255, 255, 255))

        self.mass2 = 1
        self.mass2_slider = Slider(Vector2D(game.WIDTH/2, game.HEIGHT/2 - 50), 300, 20, 0.05, 100, self.mass2, "Mass 2", (30, 30, 30), (255, 255, 255))

        self.distance = 300
        self.distance_slider = Slider(Vector2D(game.WIDTH/2, game.HEIGHT/2 + 50), 300, 20, 100, 30000, self.distance, "Distance", (30, 30, 30), (255, 255, 255))

        self.eccentricity = 0
        self.eccentricity_slider = Slider(Vector2D(game.WIDTH/2, game.HEIGHT/2 + 150), 300, 20, 0, 1, self.eccentricity, "Eccentricity", (30, 30, 30), (255, 255, 255))

        self.sliders = [self.mass1_slider, self.mass2_slider, self.distance_slider, self.eccentricity_slider]

        self.spawn_button = Button(Vector2D(game.WIDTH/2, game.HEIGHT/2 + self.height/2 - 50), 200, 50, "Spawn", (100, 100, 100), lambda: self.spawn_binary(self.mass1 * game.START_MASS, self.mass2 * game.START_MASS, self.distance * game.START_DIST, self.eccentricity))

    def check_click(self, mouse):
        for slider in self.sliders:
            distance = game.get_dist(mouse[0], mouse[1], slider.value_to_pos(slider.value).x, slider.value_to_pos(slider.value).y)

            if distance < 20:
                slider.dragging = True

                slider.drag_offset = Vector2D(slider.value_to_pos(slider.value).x - mouse[0], 0)
                return

        self.spawn_button.check_click(mouse)

    def check_dragging(self, mouse):
        for slider in self.sliders:
            if slider.dragging:
                slider.drag(mouse)
                return

    def release_drag(self):
        for slider in self.sliders:
            if slider.dragging:
                slider.dragging = False

    def spawn_binary(self, m1, m2, r, e):
        x1 = (m2 * r) / (m1 + m2)
        x2 = (m1 * r) / (m1 + m2)

        v1 = math.sqrt((game.G * m1 * m2 * x1) / (m1 * r**2)) * (1 - e)
        p1 = v1 * m1
        p2 = -p1
        v2 = p2 / m2

        object1 = BinaryObject(Vector2D(-x1, 0), Vector2D(0, v1), m1)
        object2 = BinaryObject(Vector2D(x2, 0), Vector2D(0, v2), m2)

        game.CENTRE_OF_MASS = (m1, m2, object1.position, object2.position)

        game.OBJECTS.append(object1)
        game.OBJECTS.append(object2)

        self.open = False
    
    def update(self):
        self.mass1 = int(self.mass1_slider.value)
        self.mass2 = int(self.mass2_slider.value)
        self.distance = int(self.distance_slider.value)
        self.eccentricity = self.eccentricity_slider.value

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
        if self.value < 10:
            text_surface = game.text_font.render(f"{round(self.value, 2)}", True, (255, 255, 255))
        else:
            text_surface = game.text_font.render(f"{round(self.value)}", True, (255, 255, 255))
        game.WIN.blit(text_surface, (self.value_to_pos(self.value) - Vector2D(text_surface.get_width()/2, 50)).to_coordinate())

        # Draw name text
        name_surface = game.text_font.render(self.name_text, True, (255, 255, 255))
        game.WIN.blit(name_surface, (self.position.x - self.width/2 - name_surface.get_width() - 30, self.position.y - name_surface.get_height()/2))



class Button():
    def __init__(self, position: Vector2D, width, height, text, background_colour, func) -> None:
        self.position: Vector2D = position
        self.width = width
        self.height = height

        self.text = text

        self.background_colour = background_colour

        self.func: function = func

    def check_click(self, mouse):
        if abs(mouse[0] - self.position.x) <= self.width/2 and abs(mouse[1] - self.position.y) <= self.height/2:
            self.pressed()

    def pressed(self):
        self.func()

    def draw(self):
        # Draw background rectangle
        pygame.draw.rect(game.WIN, self.background_colour, (self.position.x - self.width/2, self.position.y - self.height/2, self.width, self.height))

        # Draw button text
        text_surface = game.text_font.render(self.text, True, (255, 255, 255))
        game.WIN.blit(text_surface, (self.position.x - text_surface.get_width()/2, self.position.y - text_surface.get_height()/2))



class Toggle():
    def __init__(self, position: Vector2D, width, height, text, box_colour, condition: bool) -> None:
        self.position: Vector2D = position
        self.width = width
        self.height = height

        self.text = text

        self.box_colour = box_colour

        self.condition = condition

        self.toggle_offset = 5

    def check_click(self, mouse):
        if abs(mouse[0] - self.position.x) <= self.width/2 and abs(mouse[1] - self.position.y) <= self.height/2:
            self.pressed()
            return True
        
        return False

    def pressed(self):
        self.condition = not self.condition

    def draw(self):
        # Draw background rectangle
        pygame.draw.rect(game.WIN, self.box_colour, (self.position.x - self.width/2, self.position.y - self.height/2, self.width, self.height), 2)

        # Draw toggle
        if self.condition:
            pygame.draw.rect(game.WIN, (0, 255, 0), (self.position.x - self.width/2 + self.toggle_offset, self.position.y - self.height/2 + self.toggle_offset, self.width - 2*self.toggle_offset, self.height - 2*self.toggle_offset))

        # Draw toggle text
        text_surface = game.text_font.render(self.text, True, (255, 255, 255))
        game.WIN.blit(text_surface, (self.position.x + self.width, self.position.y - text_surface.get_height()/2))



class Graph():
    def __init__(self, position: Vector2D, width, height, colour, x_start, x_end, y_start, y_end, y_start2, y_end2, x_axis_title, y_axis_title, y_axis_title2) -> None:
        self.position: Vector2D = position
        self.width = width
        self.height = height
        self.colour = colour

        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.y_start2 = y_start2
        self.y_end2 = y_end2


        self.x_range = x_end - x_start
        self.y_range = y_end - y_start
        self.y_range2 = y_end2 - y_start2

        self.axis_offset = 25

        self.start_y_coords = Vector2D(self.position.x - self.width/2 + self.axis_offset, self.position.y + self.height/2 - self.axis_offset)
        self.end_y_coords = Vector2D(self.position.x - self.width/2 + self.axis_offset, self.position.y - self.height/2 + self.axis_offset)
        self.start_y_coords2 = Vector2D(self.position.x + self.width/2 - self.axis_offset, self.position.y + self.height/2 - self.axis_offset)
        self.end_y_coords2 = Vector2D(self.position.x + self.width/2 - self.axis_offset, self.position.y - self.height/2 + self.axis_offset)

        self.start_x_coords = Vector2D(self.position.x - self.width/2 + self.axis_offset, self.position.y + self.height/2 - self.axis_offset)
        self.end_x_coords = Vector2D(self.position.x + self.width/2 - self.axis_offset, self.position.y + self.height/2 - self.axis_offset)

        self.x_coord_range = self.end_x_coords.x - self.start_x_coords.x
        self.y_coord_range = self.end_y_coords.y - self.start_y_coords.y

        self.points = []
        self.points2 = []

        self.text_offset = 5

        self.x_axis_title = x_axis_title
        self.y_axis_title = y_axis_title
        self.y_axis_title2 = y_axis_title2

        self.x_axis_grid_separation = 0.0001
        self.y_axis_grid_separation = 100000

        self.graph_timer = 0
        self.graph_time = 0.00000000001
        self.graph_total_time = 0

    def point_to_position(self, point: Vector2D, index):

        x_proportion = point.x / self.x_range
        new_x = x_proportion * self.x_coord_range

        if index == 0:
            y_proportion = point.y / self.y_range
            new_y = y_proportion * self.y_coord_range
            return Vector2D(self.start_x_coords.x + new_x, self.start_y_coords.y + new_y)

        else:
            y_proportion = point.y / self.y_range2
            new_y = y_proportion * self.y_coord_range
            return Vector2D(self.start_x_coords.x + new_x, self.start_y_coords2.y + new_y)
    
    def add_point(self, point, point2):
        self.points.append(point)
        self.points2.append(point2)

    def draw_axis_info(self):
        # Draw x-axis labels
        axis_x_start = game.text_font.render(f"{self.x_start}", True, (255, 255, 255))
        game.WIN.blit(axis_x_start, (self.start_x_coords.x - axis_x_start.get_width()/2, self.start_x_coords.y + self.text_offset))

        axis_x_end = game.text_font.render(f"{round(self.x_end, 2)}", True, (255, 255, 255))
        game.WIN.blit(axis_x_end, (self.end_x_coords.x - axis_x_end.get_width()/2, self.end_x_coords.y + self.text_offset))

        # Draw y-axis labels
        axis_y_start = game.text_font.render(f"{self.y_start}", True, (100, 100, 255))
        game.WIN.blit(axis_y_start, (self.start_y_coords.x - axis_y_start.get_width() - self.text_offset, self.start_y_coords.y - axis_y_start.get_height()/2))

        axis_y_end = game.text_font.render(f"{round(self.y_end, 2)}", True, (100, 100, 255))
        game.WIN.blit(axis_y_end, (self.end_y_coords.x - axis_y_end.get_width() - self.text_offset, self.end_y_coords.y))

        # Draw y-axis labels 2
        axis_y_start2 = game.text_font.render(f"{self.y_start2}", True, (255, 165, 0))
        game.WIN.blit(axis_y_start2, (self.start_y_coords2.x + axis_y_start2.get_width()/2 + self.text_offset, self.start_y_coords2.y - axis_y_start2.get_height()/2))

        axis_y_end2 = game.text_font.render(f"{round(self.y_end2, 2)}", True, (255, 165, 0))
        game.WIN.blit(axis_y_end2, (self.end_y_coords2.x + axis_y_end2.get_width()/2, self.end_y_coords2.y))

        # Draw x-axis Title
        axis_x_title = game.text_font.render(self.x_axis_title, True, (255, 255, 255))
        game.WIN.blit(axis_x_title, (self.position.x - axis_x_title.get_width()/2, self.start_x_coords.y + self.text_offset))

        # Draw y-axis Title
        axis_y_title = game.text_font.render(self.y_axis_title, True, (100, 100, 255))
        axis_y_title = pygame.transform.rotate(axis_y_title, 90)
        game.WIN.blit(axis_y_title, (self.start_y_coords.x - axis_y_title.get_width()/2 - self.text_offset - 5, self.position.y - axis_y_title.get_height()/2))

        # Draw y-axis Title 2
        axis_y_title2 = game.text_font.render(self.y_axis_title2, True, (255, 165, 0))
        axis_y_title2 = pygame.transform.rotate(axis_y_title2, -90)
        game.WIN.blit(axis_y_title2, (self.start_y_coords2.x + axis_y_title2.get_width()/2, self.position.y - axis_y_title2.get_height()/2))

    def update(self, delta_time, y_input, y_input2):
        if self.graph_timer < self.graph_time:
            self.graph_timer += delta_time
            self.graph_total_time += delta_time
        else:
            self.add_point(Vector2D(self.graph_total_time, y_input), Vector2D(self.graph_total_time, y_input2))
            self.graph_timer = 0

        self.x_end = max(self.x_end, self.graph_total_time)
        self.x_range = self.x_end - self.x_start

        self.y_end = max(self.y_end, y_input)
        self.y_range = self.y_end - self.y_start

        self.y_end2 = max(self.y_end2, y_input2)
        self.y_range2 = self.y_end2 - self.y_start2

    def draw(self):
        # Draws background
        pygame.draw.rect(game.WIN, self.colour, (self.position.x - self.width/2, self.position.y - self.height/2, self.width, self.height))


        # Draw grid
        num_x_lines = (self.x_range) / self.x_axis_grid_separation
        if num_x_lines > 20:
            self.x_axis_grid_separation *= 2
            num_x_lines = self.x_range / self.x_axis_grid_separation

        num_y_lines = self.y_range / self.y_axis_grid_separation
        if num_y_lines > 10:
            self.y_axis_grid_separation *= 2
            num_y_lines = self.y_range / self.y_axis_grid_separation
        
        for x in range(int(num_x_lines)):
            pygame.draw.line(game.WIN, (100, 100, 100), (self.start_y_coords.x + (x+1)/(self.x_range / self.x_axis_grid_separation) * self.x_coord_range, self.start_y_coords.y), (self.end_y_coords.x + (x+1)/(self.x_range / self.x_axis_grid_separation) * self.x_coord_range, self.end_y_coords.y))
        
        for y in range(int(self.y_range / self.y_axis_grid_separation)):
            pygame.draw.line(game.WIN, (100, 100, 100), (self.start_x_coords.x, self.start_x_coords.y + (y+1)/(self.y_range / self.y_axis_grid_separation) * self.y_coord_range), (self.end_x_coords.x, self.end_x_coords.y + (y+1)/(self.y_range / self.y_axis_grid_separation) * self.y_coord_range))

        
        # X-axis
        pygame.draw.line(game.WIN, (255, 255, 255), self.start_x_coords.to_coordinate(), self.end_x_coords.to_coordinate())

        # Y-axis
        pygame.draw.line(game.WIN, (100, 100, 255), self.start_y_coords.to_coordinate(), self.end_y_coords.to_coordinate())
        pygame.draw.line(game.WIN, (255, 165, 0), self.start_y_coords2.to_coordinate(), self.end_y_coords2.to_coordinate())
        

        # Draws points
        if len(self.points) > 1:

            # Remove close points to improve performance
            if self.point_to_position(self.points[len(self.points)-1], 0).get_distance(self.point_to_position(self.points[len(self.points)-2], 0)) < 1:
                self.points.remove(self.points[len(self.points)-1])

            for i in range(len(self.points) - 1):
                pygame.draw.line(game.WIN, (100, 100, 255), self.point_to_position(self.points[i], 0).to_coordinate(), self.point_to_position(self.points[i+1], 0).to_coordinate(), 2)

            # Draws info on last point
            info_text = game.text_font.render(f"{round(self.points[len(self.points)-1].y, 2)}", True, (255, 255, 255))
            game.WIN.blit(info_text, (self.point_to_position(self.points[len(self.points)-1], 0).x + info_text.get_width()/2, self.point_to_position(self.points[len(self.points)-1], 0).y - info_text.get_height()/2))

        if len(self.points2) > 1:

            if self.point_to_position(self.points2[len(self.points2)-1], 1).get_distance(self.point_to_position(self.points2[len(self.points2)-2], 1)) < 1:
                self.points2.remove(self.points2[len(self.points2)-1])

            for i in range(len(self.points2) - 1):
                pygame.draw.line(game.WIN, (255, 165, 0), self.point_to_position(self.points2[i], 1).to_coordinate(), self.point_to_position(self.points2[i+1], 1).to_coordinate(), 2)

        
        #for point in self.points:
            #pygame.draw.circle(WIN, (255, 255, 255), self.point_to_position(point), 5)

        # Draws axis
        self.draw_axis_info()
