import copy


class Marble:
    """
    Represents a single marble on the board
    """
    def __init__(self, color):
        self.color = color

    def get_color(self):
        """
        Returns the color of the marble
        :return: is a color represented as a String
        """
        return self.color

    def validate_move(self, from_position, to_position):
        # Implement logic to validate the move based on the given coordinates
        pass

    def __deepcopy__(self, memo):
        # Create a new instance of Marble with the same color
        # No need to deepcopy `self.color` if it's immutable (e.g., a string)
        return Marble(copy.deepcopy(self.color, memo))
