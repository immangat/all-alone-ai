class Move:
    """
    Class to represent a move in the game
    """
    def __init__(self, circles, enum_direction):
        """
        Initialise the move object
        :param circles: are the circles objects selected for the move as a list
        :param enum_direction: is the direction of the move applied to each circle
        """
        self.circles = circles  # list of tuples that represent the circles
        self.enum_direction = enum_direction # not value of direction but the enum of direction

    def __str__(self):
        """
        A string representation of the move object
        :return: is the string representation of the move object
        """
        return f"Move: {self.circles} {self.enum_direction.name}\t"
