import copy

class Marble:
    def __init__(self, color):
        self.color = color

    def getColor(self):
        # Get the color of the marble
        return self.color

    def validateMove(self, from_position, to_position):
        # Implement logic to validate the move based on the given coordinates
        pass

    def __deepcopy__(self, memo):
        # Create a new instance of Marble with the same color
        # No need to deepcopy `self.color` if it's immutable (e.g., a string)
        return Marble(copy.deepcopy(self.color, memo))
