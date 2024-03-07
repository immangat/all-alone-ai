from enum import Enum


class Direction(Enum):
    """
    Enumeration of possible directions in abalone games
    """
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP_LEFT = (1, 0)
    UP_RIGHT = (1, 1)
    DOWN_LEFT = (-1, -1)
    DOWN_RIGHT = (-1, 0)
