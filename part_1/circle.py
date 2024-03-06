import copy

class Circle:
    def __init__(self, letter, number):
        self.letter = letter
        self.number = number
        self.marble = None  # Initially, no marble in the circle

    def isEmpty(self):
        # Check if the circle is empty
        return self.marble is None

    def getMarble(self):
        # Get the marble in the circle
        return self.marble

    def setMarble(self, marble):
        # Set the marble in the circle
        self.marble = marble

    def getPosition(self):
        # Get the position of the circle as (letter, number)
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