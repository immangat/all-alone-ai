class State:
    def __init__(self, move, board):
        self.move = move
        self.board = board

    def get_move(self):
        return self.move

    def get_board(self):
        return self.board

    def __str__(self):
        return f"{self.move} -> {self.board}"
