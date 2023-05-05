import math

class Vector2D():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, arg):
        if type(arg) == Vector2D:
            return Vector2D(self.x + arg.x, self.y + arg.y)
        else:
            return Vector2D(self.x + arg, self.y + arg)
        
    def __radd__(self, arg):
        if type(arg) == Vector2D:
            return Vector2D(self.x + arg.x, self.y + arg.y)
        else:
            return Vector2D(self.x + arg, self.y + arg)
    
    def __iadd__(self, arg):
        if type(arg) == Vector2D:
            self.x += arg.x
            self.y += arg.y
            return self
        else:
            self.x += arg
            self.y += arg
            return self
        
    def __sub__(self, arg):
        if type(arg) == Vector2D:
            return Vector2D(self.x - arg.x, self.y - arg.y)
        else:
            return Vector2D(self.x - arg, self.y - arg)

    def __mul__(self, arg):
        if type(arg) == Vector2D:
            return Vector2D(self.x * arg.x, self.y * arg.y)
        else:
            return Vector2D(self.x * arg, self.y * arg)
        
    def __truediv__(self, arg):
        if type(arg) == Vector2D:
            return Vector2D(self.x / arg.x, self.y / arg.y)
        else:
            return Vector2D(self.x / arg, self.y / arg)
        
    def __pow__(self, arg):
        return Vector2D(self.x**arg, self.y**arg)

    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5
    
    def normalise(self):
        magnitude = self.magnitude()

        self.x = self.x / magnitude
        self.y = self.y / magnitude

        return self
    
    def return_normalised(self):
        magnitude = self.magnitude()

        if magnitude > 0:
            x = self.x / magnitude
            y = self.y / magnitude
        else:
            x = self.x
            y = self.y

        return Vector2D(x, y)
    
    def to_coordinate(self):
        return (self.x, self.y)
    
    def rotate(self, angle):
        """Returns clockwise rotated vector by an angle in radians"""

        current_angle = math.atan2(self.y, self.x)

        return Vector2D(self.magnitude() * math.cos(current_angle + angle), self.magnitude() * math.sin(current_angle + angle))