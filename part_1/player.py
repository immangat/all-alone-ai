class Player:
    def __init__(self, color):
        self.color = color
        self.current_turn = False  # Initially, not the player's turn

    def getColor(self):
        # Get the color of the player
        return self.color

    def getCurrentTurn(self):
        # Check if it's the player's turn
        return self.current_turn

    def flipTurn(self):
        # Switch the turn to the opposite
        self.current_turn = not self.current_turn
