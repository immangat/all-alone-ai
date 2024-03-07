import copy

from board import Board
from part_1.directions import Direction
from part_1.move import Move
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
        self.game_paused = False

    def startGame(self, setup="Default", game_type="Human x Human"):
        self.game_over()
        self.board = Board()
        self.board.setupBoard(setup)
        self.define_player(game_type)
        self.current_player = self.player1
        self.saveState()
        self.reset_timers()
        self.displayBoard()

    def define_player(self, game_type="Human x Human"):
        if game_type == "Human x Human":
            self.player1 = Player("Black", "Human")
            self.player2 = Player("White", "Human")
        elif game_type == "AI(B) x Human(W)":
            self.player1 = Player("Black", "AI")
            self.player2 = Player("White", "Human")
        else:
            self.player1 = Player("Black", "Human")
            self.player2 = Player("White", "AI")

    def isGameOver(self):
        # Check if the game is over (implement logic later)
        pass

    def game_over(self):
        self.board = None
        self.states.clear_all_states()

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
                self.direction = self._aligned_two([selected_circles, to_circle])
                # If the move is valid, remove the marble from the starting circle
                self.board.getCircle(*selected_circles).setMarble(None)
                # Then, place the marble in the ending circle
                self.board.getCircle(*to_circle).setMarble(marble)
                # Update the display
                move_to_add = Move([selected_circles], self.direction)
                self.current_player.move_list.append(move_to_add)
                self.switchTurns()
                self.displayBoard()
            else:
                print("Invalid move")
        else:
            neighbors = []
            for selected_circle in selected_circles:
                neighbors.append(self.board.get_neighbors_with_direction(*selected_circle))

            filtered_neighbours = [
                {direction: pos for direction, pos in neighbour.items() if pos not in selected_circles} for neighbour in
                neighbors]


            aligned = self.are_circles_adjacent_and_aligned(selected_circles)

            if aligned == "diagonalLeft":
                filtered_neighbours = [
                    {k: v for k, v in neighbour.items() if k in ['up_left', 'down_right']}
                    for neighbour in filtered_neighbours
                ]
            elif aligned == "diagonalRight":
                filtered_neighbours = [
                    {k: v for k, v in neighbour.items() if k in ['up_right', 'down_left']}
                    for neighbour in filtered_neighbours
                ]
            elif aligned == "horizontal":
                filtered_neighbours = [
                    {k: v for k, v in neighbour.items() if k in ['left', 'right']}
                    for neighbour in filtered_neighbours
                ]



            for filtered_neighbour in filtered_neighbours:
                if to_circle in filtered_neighbour.values():
                    self.direction = list(filtered_neighbour.keys())[0]
                    break


            # if (selected_circles in neighbors.values()):
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

    def are_circles_adjacent_and_aligned(self, circles):
        if len(circles) == 2:
            direction = self._aligned_two(circles)
            if direction == Direction.RIGHT or direction == Direction.LEFT:
                direction = "horizontal"
                return direction
            elif direction == Direction.UP_RIGHT or direction == Direction.DOWN_LEFT:
                direction = "diagonalRight"
                return direction
            elif direction == Direction.UP_LEFT or direction == Direction.DOWN_RIGHT:
                direction = "diagonalLeft"
                return direction
        elif len(circles) == 3:
            return self._aligned_three(circles)

    def _aligned_two(self, circles):
        if len(circles) != 2:
            return False  # Only checking pairs of circles

        # Extract row and column from each circle
        row1, col1 = circles[0]
        row2, col2 = circles[1]

        # Calculate differences
        row_diff = ord(row2) - ord(row1)
        col_diff = col2 - col1

        # Define all possible directions
        directions = {
            Direction.LEFT: (0, -1),
            Direction.RIGHT: (0, 1),
            Direction.UP_LEFT: (1, 0),
            Direction.UP_RIGHT: (1, 1),
            Direction.DOWN_LEFT: (-1, -1),
            Direction.DOWN_RIGHT: (-1, 0),
        }
        key = None
        for k, value in directions.items():
            if value == (row_diff, col_diff):
                key = k
                break

        if key is None:
            return False
        else:
            return key

    def _aligned_three(self, circles):
        # Sort the circles by rows first (from 'A' to 'I'), and then by columns (from 1 to 9)
        circles = sorted(circles, key=lambda x: (x[0], x[1]))

        # Vectors for possible axis considering the Abalone board layout
        axis = {
            'horizontal': (0, 1),
            'diagonalLeft': (1, 0),
            'diagonalRight': (1, 1),
        }

        # Calculate vectors between consecutive circles
        vectors = [(ord(circles[i + 1][0]) - ord(circles[i][0]), circles[i + 1][1] - circles[i][1]) for i in
                   range(len(circles) - 1)]

        # Check if all vectors are the same
        if all(vector == vectors[0] for vector in vectors):
            # Create a reverse lookup dictionary from axis
            reverse_directions = {v: k for k, v in axis.items()}
            # Return the direction if it's one of the predefined ones
            return reverse_directions.get(vectors[0], None)

        return None

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
        self.player1.flipTurn()
        self.player2.flipTurn()

    def undoMove(self):

        deletedState = self.states.remove_last_states()
        if deletedState:

            self.board = self.states.get_last_board_state()
            score = self.states.get_last_score_state()
            self.player1.setScore(score[0])
            self.player2.setScore(score[1])
            self.player2.reverseMove() if self.player1.getCurrentTurn() else self.player1.reverseMove()
            self.switchTurns(save_state=False)
            self.current_player.remove_last_move()
            self.displayBoard()

    def saveState(self):
        new_board = copy.deepcopy(self.board)
        self.states.add_state(new_board, (self.player1.getScore(), self.player2.getScore()))

    def moveMutipleMarbles(self, selected_circles, direction_enum):
        i = 0
        selected_circles.sort()
        move = Move(selected_circles, direction_enum)
        self.current_player.move_list.append(move)
        if direction_enum in [Direction.DOWN_RIGHT, Direction.LEFT, Direction.DOWN_LEFT]:
            selected_circles.reverse()
        all_but_last = selected_circles[-2::-1]
        last_circle = selected_circles[-1]
        self.recursive_move(last_circle, direction_enum, None)

        for circle in all_but_last:

            next_circle = self.board.getCircle(chr(ord(circle[0]) + direction_enum.value[0]), circle[1] + direction_enum.value[1])
            curr_circle = self.board.getCircle(circle[0], circle[1])
            next_circle.setMarble(curr_circle.getMarble())
            curr_circle.setMarble(None)

    # def display_moves(self):
    #     self.displayer.display_moves(self.board)

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

        curr_marble_copy = copy.deepcopy(curr_marble)

        # If there's no marble in the next position, move the current marble there
        if next_circle_from_board.marble is None:
            next_circle_from_board.marble = curr_marble_copy
            return
        else:
            self.recursive_move(next_circle, direction, curr_marble_copy)

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


    def reset_timers(self):
        self.player1.clear_clock()
        self.player2.clear_clock()

    def toggle_pause_game(self):
        self.game_paused = not self.game_paused


    def print_moves(self):
        print(f"Player 1\t\t\t\t\t\t\t\t\t\t\tPlayer 2")
        # for player1, player2 in zip(self.player1.get_move_list(), self.player2.get_move_list()):
        #     print(f"{player1}\t\t\t\t\t{player2}")

        #for loop but with max
        for i in range(max(len(self.player1.get_move_list()), len(self.player2.get_move_list()))):
            if i < len(self.player1.get_move_list()):
                player1 = self.player1.get_move_list()[i]
            else:
                player1 = ""
            if i < len(self.player2.get_move_list()):
                player2 = self.player2.get_move_list()[i]
            else:
                player2 = ""
            print(f"{player1}\t\t\t\t\t\t{player2}")


if __name__ == "__main__":
    manager = Manager()
    manager.startGame("German Daisy")
