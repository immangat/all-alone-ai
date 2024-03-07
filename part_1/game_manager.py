import copy

from board import Board
from part_1.directions import Direction
from user_interface2 import Displayer
from player import Player
from states import States


class Manager:
    def __init__(self):
        self.player1: Player = None
        self.player2: Player = None
        self.current_player: Player = None
        self.board = None
        # self.selected_circles = []
        self.direction = "right"
        self.displayer = Displayer(manager=self)
        self.states = States()

    def startGame(self, setup="default"):
        self.board = Board()
        self.board.setupBoard(setup)
        self.player1 = Player("Black")
        self.current_player = self.player1
        self.player2 = Player("White")
        self.saveState()
        self.displayBoard()

    def isGameOver(self):
        # Check if the game is over (implement logic later)
        pass

    def displayBoard(self):
        score = (self.player1.getScore(), self.player2.getScore())
        moves = (self.player1.getMoves(), self.player2.getMoves())
        currentPlayerColor = self.player1.getColor() if self.player1.getCurrentTurn() else self.player2.getColor()
        self.displayer.updateBoard(self.board, score, moves, currentPlayerColor)

    # TODO Lateral movement still needs to be implemented
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
                self.switchTurns()
                self.displayBoard()
            else:
                print("Invalid move")
        else:
            print("trying to move multiple marbles")
            print(self.direction)
            if self.direction == "left":
                self.moveMutipleMarbles(selected_circles, Direction.LEFT)
            elif self.direction == "right":
                self.moveMutipleMarbles(selected_circles, Direction.RIGHT)
            elif self.direction == "up_left":
                self.moveMutipleMarbles(selected_circles, Direction.UP_LEFT)
            elif self.direction == "up_right":
                self.moveMutipleMarbles(selected_circles, Direction.UP_RIGHT)
            elif self.direction == "down_right":
                self.moveMutipleMarbles(selected_circles, Direction.DOWN_RIGHT)
            elif self.direction == "down_left":
                self.moveMutipleMarbles(selected_circles, Direction.DOWN_LEFT)
            # self.moveMutipleMarbles(selected_circles, Direction.DOWN_LEFT)
            self.switchTurns()
            self.displayBoard()

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

    def switchTurns(self, save_state=True):
        # Switches the turn from one player to the other
        self.current_player.reset_timer()
        if save_state:
            self.player1.moveUp() if self.player1.getCurrentTurn() else self.player2.moveUp()
            self.saveState()
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        playerColor = self.player1.getColor() if self.player1.getCurrentTurn() else self.player2.getColor()

    def undoMove(self):

        deletedState = self.states.remove_last_states()
        if deletedState:
            self.board = self.states.get_last_board_state()
            score = self.states.get_last_score_state()
            self.player1.setScore(score[0])
            self.player2.setScore(score[1])
            self.player2.reverseMove() if self.player1.getCurrentTurn() else self.player1.reverseMove()
            self.switchTurns(save_state=False)
            self.displayBoard()

    def saveState(self):
        new_board = copy.deepcopy(self.board)
        self.states.add_state(new_board, (self.player1.getScore(), self.player2.getScore()))

    def moveMutipleMarbles(self, selected_circles, direction_enum):
        i = 0
        selected_circles.sort()
        if direction_enum in [Direction.DOWN_RIGHT, Direction.LEFT, Direction.DOWN_LEFT]:
            selected_circles.reverse()

        first_circle = selected_circles[0]
        self.recursive_move(first_circle, direction_enum, None)

    def recursive_move(self, selected_circle, direction, previous_marble=None):
        next_char = chr(ord(selected_circle[0]) + direction.value[0])
        next_num = selected_circle[1] + direction.value[1]
        next_circle = (next_char, next_num)

        curr_marble = self.board.getCircle(selected_circle[0], selected_circle[1]).marble

        # Check if the current marble is the one to be moved, and there is no previous marble
        if curr_marble is not None and previous_marble is None:
            # This means we are at the first marble to be moved, so we should remove it after copying
            self.board.getCircle(selected_circle[0], selected_circle[1]).marble = None

        next_circle_from_board = self.board.getCircle(next_char, next_num)
        print("This is the next circle from board {}".format(next_circle_from_board))

        curr_marble_copy = copy.deepcopy(curr_marble)

        # If there's no marble in the next position, move the current marble there
        if next_circle_from_board.marble is None:
            print("No marble found, stop recursive move")
            next_circle_from_board.marble = curr_marble_copy
            return
        else:
            print("Recursive move")
            self.recursive_move(next_circle, direction, curr_marble_copy)

        # print(selected_circle)
        # print(direction.value)
        # print(selected_circle[0])
        # print(selected_circle[1])
        # print(next_circle_from_board.marble)
        # print(next_num)
        # print(next_circle)
        # print(next_char)

    def get_time_to_display(self):
        player_one_time = self.player1.get_time()
        player_one_agg = self.player1.get_aggregate_time()
        player_one_last_move = self.player1.get_last_move_time()
        player_two_time = self.player2.get_time()
        player_two_agg = self.player2.get_aggregate_time()
        player_two_last_move = self.player2.get_last_move_time()
        seconds = self.current_player.increment_time()
        if seconds <= 0:
            self.switchTurns()
        return player_one_time, player_one_agg, player_one_last_move, player_two_time, player_two_agg, player_two_last_move


if __name__ == "__main__":
    manager = Manager()
    manager.startGame()
