class Move:
    def __init__(self, circles, enum_direction):
        self.circles = circles  # list of tuples that represent the circles
        self.enum_direction = enum_direction # not value of direction but the enum of direction

    def __str__(self):
        return f"Move: {self.circles} {self.enum_direction}\t"
