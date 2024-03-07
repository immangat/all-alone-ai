from board import Board
import copy


class States:
    """
    This class represents the state of the game and board
    """

    def __init__(self):
        """
        Initialize the state of the game and board
        """
        self.boardStates = []
        self.scoreStates = []
        self.moves = []

    def add_state(self, board, score):
        """
        Add a state to the board and score states as a history
        :param board: The board of the game
        :param score: The score of the game
        """
        self.boardStates.append(board)
        self.scoreStates.append(score)

    def __len__(self):
        """
        Return the number of states in the game has been in so far
        :return: the number of states as an Int
        """
        return len(self.boardStates)

    def get_last_board_state(self):
        """
        Getter for the last state or most recent state the board was in
        return: is the board as a list
        """
        new_board = copy.deepcopy(self.boardStates[-1])
        return new_board

    def get_last_score_state(self):
        """
        Getter for the latest stored score state in the game
        :return: the score state
        """
        new_score = copy.deepcopy(self.scoreStates[-1])
        return new_score

    def remove_last_states(self):
        """
        Removes the most recently added states from the object
        :return: is Boolean for if was successfully removed
        """
        if len(self.scoreStates) > 1:
            del self.boardStates[-1]
            del self.scoreStates[-1]
            return True
        return False

    def clear_all_states(self):
        """
        Clears the all the states in the game
        """
        self.boardStates = []
        self.scoreStates = []