# Created a separate script just for this class to make code in each file cleaner

import pygame
import game
import math


# Class for the objects
class CelestialBody():
    # Init function is run upon when the class is initialised
    def __init__(self, x, y, initial_velocity, mass): # When initialised these arguments are passed into the function
        # self is this current object. A variable which is of self can access be accessed from inside or outside the class.
        # EXAMPLE: if you call object.x (where object is just a random instance of this class) it would take the x value of the object.
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = (self.mass / math.pi)**0.5 # Making radius related to mass (mass = area)

        self.velocity = initial_velocity
        self.acceleration = (0, 0) # Acceleration starts off as 0 in the x axis and 0 in the y axis

    def update(self, delta_time):
        self.attract() # Calls attract function every frame that this object is updated
        self.velocity = (self.velocity[0] + self.acceleration[0] * delta_time, self.velocity[1] + self.acceleration[1] * delta_time) # calculates velocity based on acceleration

        # Adds velocity to x and y position. Multiplied by delta_time to ensure that if the frame rates are different, the same amount of velocity will be added to the x and y per unit or real time
        self.x += self.velocity[0] * delta_time
        self.y += self.velocity[1] * delta_time
    
    def attract(self):
        accelerations = [] # list of accelerations (each object causes the other to accelerate and so a list can be used to store all of the accelerations with every object)
        objects_to_remove = []
        object_to_add = []

        # loops through all objects in the main object list
        for object in game.OBJECTS:
            if object != self: # makes sure you will not attract yourself
                distance = game.get_dist(self.x, self.y, object.x, object.y) # Example of using functions from game

                # Calculates if the object and self are colliding
                if distance < self.radius:
                    combined_mass = self.mass + object.mass
                    # Adds new celestial body to list with new initial states of the combination of the two previous states
                    object_to_add.append(CelestialBody(self.x, self.y, ((self.mass*self.velocity[0] + object.mass*object.velocity[0]) / combined_mass, (self.mass*self.velocity[1] + object.mass*object.velocity[1]) / combined_mass), combined_mass))

                    # Adds the two colliding celestial bodies to a list to then be removed later
                    objects_to_remove.append(self)
                    objects_to_remove.append(object)
                else:
                    # Run if the objects are not colliding e.i. they are attracting each other

                    # Newtons gravity
                    force = game.G * (self.mass * object.mass / (distance)**2) # Only gets the magnitude of the force

                    # Gets direction from self to object
                    direction = (object.x - self.x, object.y - self.y)
                    direction_magnitude = (direction[0]**2 + direction[1]**2)**0.5

                    force_direction = (direction[0] * (force / direction_magnitude), direction[1] * (force / direction_magnitude)) # Gives the force a direction with magnitude of the force magnitude calculated from newtons equation

                    # a = F/ m
                    accelerations.append((force_direction[0] / self.mass, force_direction[1] / self.mass))

        # The reason for adding the objects to add and remove to a separate list before doing the functions on the main list is due to the fact that
        # you cannot change the list while you are iterating through it. Therefore, just add what you want to add and remove from the list to some temporary lists
        # and add/ remove them after the loop has finished
        for object in object_to_add:
            game.OBJECTS.append(object)

        for object in objects_to_remove:
            game.OBJECTS.remove(object)
        
        # Quick code to add up the x and y's of all of the accelerations calculated with every other object
        x = 0
        y = 0
        for i in range(len(accelerations)):
            x += accelerations[i][0]
            y += accelerations[i][1]

        self.acceleration = (x, y) # Sets the main acceleration variable to the sum

    def draw(self):
        # Draws circle
        pygame.draw.circle(game.WIN, (255, 0, 0), (self.x, self.y), self.radius)