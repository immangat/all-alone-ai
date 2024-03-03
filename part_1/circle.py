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


