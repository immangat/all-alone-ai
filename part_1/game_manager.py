from board import Board
from user_interface2 import Displayer
from player import Player


class Manager:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.board = None
        self.selected_circles = []
        self.displayer = Displayer(manager=self)

    def startGame(self, setup="default"):
        self.board = Board()
        self.board.setupBoard(setup)
        self.player1 = Player("Black")
        self.player1.flipTurn()
        self.player2 = Player("White")
        self.displayBoard()

    def isGameOver(self):
        # Check if the game is over (implement logic later)
        pass


    def displayBoard(self):
        self.displayer.updateBoard(self.board)

    def moveMarble(self, from_circle, to_circle):
        # Get the marble object from the starting circle
        marble = self.board.getCircle(*from_circle).getMarble()

        # Check if the move is valid (to be implemented)
        if self.isValidMove(from_circle, to_circle, marble):
            # If the move is valid, remove the marble from the starting circle
            self.board.getCircle(*from_circle).setMarble(None)

            # Then, place the marble in the ending circle
            self.board.getCircle(*to_circle).setMarble(marble)

            # Implement logic to handle pushing marbles off the board here

            # Update the display
            self.displayBoard()

            # # Switch turns
            # self.switchTurns()
        else:
            print("Invalid move")

    def isValidMove(self, from_circle, to_circle, marble):
        # Check if the to_circle is one of the valid neighbors of from_circle
        valid_neighbors = self.board.get_neighbors(*from_circle)
        if to_circle not in valid_neighbors:
            return False  # to_circle is not adjacent to from_circle

        # Check if the to_circle is empty
        to_circle_marble = self.board.getCircle(*to_circle).getMarble()
        if to_circle_marble is not None:
            return False  # to_circle is not empty

        # Add any additional rules specific to Abalone here
        # For example, marbles cannot move against the direction of push, etc.

        return True  # The move is valid

    def switchTurns(self):
        # Switches the turn from one player to the other
        self.player1.flipTurn()
        self.player2.flipTurn()


if __name__ == "__main__":
    manager = Manager()
    manager.startGame("belgian_daisy")
