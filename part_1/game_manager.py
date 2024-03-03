from board import Board
from user_interface2 import Displayer
from player import Player


class Manager:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.board = None
        self.selected_circles = []
        self.displayer = Displayer()

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
        pass



if __name__ == "__main__":
    manager = Manager()
    manager.startGame("belgian_daisy")
