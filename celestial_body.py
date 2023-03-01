import pygame
import game



class CelestialBody():
    def __init__(self, x, y, initial_velocity, mass, radius) -> None:
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius

        self.velocity = initial_velocity
        self.acceleration = (0, 0)

    def update(self, delta_time):
        self.attract()
        self.velocity = (self.velocity[0] + self.acceleration[0] * delta_time, self.velocity[1] + self.acceleration[1] * delta_time)

        self.x += self.velocity[0]
        self.y += self.velocity[1]
    
    def attract(self):
        accelerations = []
        objects_to_remove = []
        object_to_add = []
        for object in game.OBJECTS:
            if object != self:
                distance = game.get_dist(self.x, self.y, object.x, object.y)

                if distance < self.radius:
                    combined_mass = self.mass + object.mass
                    object_to_add.append(CelestialBody(self.x, self.y, ((self.mass*self.velocity[0] + object.mass*object.velocity[0]) / combined_mass, (self.mass*self.velocity[1] + object.mass*object.velocity[1]) / combined_mass), combined_mass, self.radius + (object.radius / 2)))
                    objects_to_remove.append(self)
                    objects_to_remove.append(object)
                else:
                    force = game.G * (self.mass * object.mass / (distance)**2)
                    direction = (object.x - self.x, object.y - self.y)
                    direction_magnitude = (direction[0]**2 + direction[1]**2)**0.5
                    force_direction = (direction[0] * (force / direction_magnitude), direction[1] * (force / direction_magnitude))
                    accelerations.append((force_direction[0] / self.mass, force_direction[1] / self.mass))

        for object in object_to_add:
            game.OBJECTS.append(object)

        for object in objects_to_remove:
            game.OBJECTS.remove(object)
        
        x = 0
        y = 0
        for i in range(len(accelerations)):
            x += accelerations[i][0]
            y += accelerations[i][1]

        self.acceleration = (x, y)

    def draw(self):
        pygame.draw.circle(game.WIN, (255, 0, 0), (self.x, self.y), self.radius)