from board import Board
import copy
class States:

    def __init__(self):
        self.boardStates = []
        self.scoreStates = []


    def add_state(self, board, score):
        self.boardStates.append(board)
        self.scoreStates.append(score)

    def __len__(self):
        return len(self.boardStates)

    def get_last_board_state(self):
        newboard = copy.deepcopy(self.boardStates[-1])
        return newboard

    def get_last_score_state(self):
        newscore = copy.deepcopy(self.scoreStates[-1])
        return newscore

    def remove_last_states(self):

        if len(self.scoreStates) > 1:
            del self.boardStates[-1]
            del self.scoreStates[-1]
            return True
        return False





