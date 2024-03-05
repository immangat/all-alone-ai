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
        return self.boardStates[-1]

    def get_last_score_state(self):
        return self.scoreStates[-1]

    def remove_last_states(self):
        self.boardStates.pop()
        self.scoreStates.pop()


