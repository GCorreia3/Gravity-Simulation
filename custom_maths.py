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

    def __mul__(self, arg):
        if type(arg) == Vector2D:
            return Vector2D(self.x * arg.x, self.y * arg.y)
        else:
            return Vector2D(self.x * arg, self.y * arg)