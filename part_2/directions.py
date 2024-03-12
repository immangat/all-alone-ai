from enum import Enum


class Direction(Enum):
    """
    Enumeration of possible directions in abalone games
    """
    UP_RIGHT = 1
    RIGHT = 3
    DOWN_RIGHT = 5
    DOWN_LEFT = 7
    LEFT = 9
    UP_LEFT = 11
