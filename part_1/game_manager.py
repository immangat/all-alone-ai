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

            # Switch turns
            self.switchTurns()
        else:
            print("Invalid move")

    def isValidMove(self, from_circle, to_circle, marble):
        # Implement the logic to validate the move
        # Check if the target circle is within bounds and is empty
        # Check if the path is clear for in-line moves or side-steps
        # Check if the move is in accordance with the rules (like not moving more than 3 marbles)
        return True  # Placeholder, real implementation needed

    def switchTurns(self):
        # Switches the turn from one player to the other
        self.player1.flipTurn()
        self.player2.flipTurn()


if __name__ == "__main__":
    manager = Manager()
    manager.startGame("belgian_daisy")
