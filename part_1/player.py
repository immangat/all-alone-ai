from time import time

class Player:
    def __init__(self, color):
        self.color = color
        self.current_turn = False  # Initially, not the player's turn
        self.moves = 0
        self.score = 0
        self.timer = 0

    def getColor(self):
        # Get the color of the player
        return self.color

    def getCurrentTurn(self):
        # Check if it's the player's turn
        return self.current_turn

    def flipTurn(self):
        self.current_turn = not self.current_turn




    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

    def scoreUp(self):
        self.score += 1

    def reverseScore(self):
        self.score -= 1

    def moveUp(self):
        self.moves += 1

    def reverseMove(self):
        self.moves -= 1

    def getMoves(self):
        return self.moves