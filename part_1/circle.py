import copy


class Circle:
    """
    Represents a spot or circle on the board that can contain a marble
    """
    def __init__(self, letter, number):
        """
        Constructs a new Circle
        :param letter: is the letter of board or row number as a character
        :param number: is the column of board or column number as an Int
        """
        self.letter = letter
        self.number = number
        self.marble = None  # Initially, no marble in the circle

    def is_empty(self):
        """ Checks if the circle is empty"""
        return self.marble is None

    def get_marble(self):
        """ Returns the marble of the circle"""
        return self.marble

    def set_marble(self, marble):
        """
        Set the marble in the circle
        :param marble: is the marble to set
        """
        self.marble = marble

    def get_position(self):
        """ Gets the position of the circle as (letter, number) """
        return self.letter, self.number

    def __lt__(self, other):
        # Compare circles based on their positions
        if self.letter == other.letter:
            return self.number < other.number
        return self.letter < other.letter

    def __deepcopy__(self, memo):
        # Create a new instance of the Circle class with the same attributes
        new_circle = Circle(copy.deepcopy(self.letter, memo), copy.deepcopy(self.number, memo))

        # Deep copy the marble attribute if it exists
        if self.marble is not None:
            new_circle.marble = copy.deepcopy(self.marble, memo)

        return new_circle
