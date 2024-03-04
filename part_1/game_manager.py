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
        # ???: What is the point of the flip cart
        self.player1.flipTurn()
        self.player2 = Player("White")
        self.displayBoard()

    def isGameOver(self):
        # Check if the game is over (implement logic later)
        pass

    def displayBoard(self):
        self.displayer.updateBoard(self.board)

    def _get_to_circle(self, selected_circle_row, selected_circle_number, direction):
        print("selected_row", selected_circle_row)
        print("selected_number", selected_circle_number)
        to_circle = None
        if direction == "R":
            to_circle = (selected_circle_row, selected_circle_number + 1)
        elif direction == "L":
            to_circle = (selected_circle_row, selected_circle_number - 1)
        elif direction == "UL":
            to_circle = (chr(ord(selected_circle_row) + 1), selected_circle_number)
        elif direction == "UR":
            to_circle = (chr(ord(selected_circle_row) + 1), selected_circle_number + 1)
        elif direction == "DL":
            to_circle = (chr(ord(selected_circle_row) - 1), selected_circle_number - 1)
        elif direction == "DR":
            to_circle = (chr(ord(selected_circle_row) - 1), selected_circle_number )
        return to_circle

    def move_marble2(self, selected_circle, direction):
        selected_circle_row, selected_circle_number = selected_circle
        marble = self.board.getCircle(*selected_circle).getMarble()
        to_circle = self._get_to_circle(selected_circle_row, selected_circle_number, direction)
        print("circle", to_circle)
        self.board.getCircle(*selected_circle).setMarble(None)
        # Then, place the marble in the ending circle
        self.board.getCircle(*to_circle).setMarble(marble)
        # Update the display
        self.displayBoard()

    # TODO Only works for single marbles and the top two rows have issues, need to fix
    def moveMarble(self, selected_circles, to_circle):
        # Get the marble object from the starting circle
        if isinstance(selected_circles, tuple):  # handles the case when only one marble is selected
            marble = self.board.getCircle(*selected_circles).getMarble()
            if self.isValidMove(selected_circles, to_circle, marble):
                # If the move is valid, remove the marble from the starting circle
                self.board.getCircle(*selected_circles).setMarble(None)
                # Then, place the marble in the ending circle
                self.board.getCircle(*to_circle).setMarble(marble)
                # Update the display
                self.displayBoard()
            else:
                print("Invalid move")

        # else: # handles the case when multiple marbles are selected
        # TODO This logic is currently not functional
        # print("list of marbles selected")
        # for marble in selected_circles:
        #     if self.isValidMove(marble, to_circle, marble):
        #         # If the move is valid, remove the marble from the starting circle
        #         self.board.getCircle(*marble).setMarble(None)
        #         # Then, place the marble in the ending circle
        #         self.board.getCircle(*to_circle).setMarble(marble)
        #         # Update the display
        #         self.displayBoard()
        #     else:
        #         print("Invalid move")

    def isValidMove2(self, selected_circle, direction):
        selected_circle_row, selected_circle_number = selected_circle
        to_circle = self._get_to_circle(selected_circle_row, selected_circle_number, direction)
        print("to circle", to_circle)
        to_circle_marble = self.board.getCircle(*to_circle).getMarble()
        if to_circle_marble is None:
            return True
        return False

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
