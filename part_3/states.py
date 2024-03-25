from state import State


class States:

    def __init__(self):
        self.states = []

    def add_state(self, move, board):
        self.states.append(State(move, board))

    def create_initial_state(self, board):
        initial_state = State(None, board)
        self.states.append(initial_state)

    def remove_last_state(self):
        if len(self.states) > 1:  # Do not remove the first state as it is the initial board for the game
            self.states.pop()

    def get_last_state(self):
        return self.states[-1]

    def get_states(self):
        return self.states

    def clear_states(self):
        self.states = []

    def __len__(self):
        return len(self.states)

    def __iter__(self):
        return iter(self.states)
