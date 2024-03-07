import copy

from board import Board
from part_1.directions import Direction
from part_1.move import Move
from user_interface2 import Displayer
from player import Player
from states import States


class Manager:
    """
    The manager class is responsible for managing the game state
    """
    def __init__(self):
        self.player1: Player = None
        self.player2: Player = None
        self.current_player: Player = None
        self.board = None
        self.direction = "right"
        self.displayer = Displayer(manager=self)
        self.states = States()
        self.game_paused = False

    def start_game(self, setup="Default", game_type="Human x Human"):
        """
        Starts the game using the given setup
        :param setup: Specify the game board setup as a string
        :param game_type: Specifies the game as a string
        :return:
        """
        self.game_over()
        self.board = Board()
        self.board.setup_board(setup)
        self.define_player(game_type)
        self.current_player = self.player1
        self.save_state()
        self.reset_timers()
        self.display_board()

    def define_player(self, game_type="Human x Human"):
        """
        Defines the types of players in the game
        :param game_type: what type of players or playing ei Human or Ai
        """
        if game_type == "Human x Human":
            self.player2 = Player("Black", "Human")
            self.player1 = Player("White", "Human")
        elif game_type == "AI(B) x Human(W)":
            self.player2 = Player("Black", "AI")
            self.player1 = Player("White", "Human")
        else:
            self.player2 = Player("Black", "Human")
            self.player1 = Player("White", "AI")

    def is_game_over(self):
        # Check if the game is over (implement logic later)
        pass

    def game_over(self):
        """
        Ends the games and clears the board for another
        """
        self.board = None
        self.states.clear_all_states()

    def display_board(self):
        """
        Displays the board for the game for the Human players to see
        :return:
        """
        score = (self.player1.get_score(), self.player2.get_score())
        moves = (self.player1.get_moves(), self.player2.get_moves())
        # currentPlayerColor = self.player1.get_color() if self.player1.get_current_turn() else self.player2.get_color()
        self.displayer.update_board(self.board, score, moves, self.current_player.get_color())

    def move_marble(self, selected_circles, to_circle):
        """
        Moves the selected marbles towards the direction that was selected in to_circle
        :param selected_circles: The selected circles to be moved
        :param to_circle: A circle used to help determine the action the user wants
        """
        # Get the marble object from the starting circle
        if isinstance(selected_circles, tuple):  # handles the case when only one marble is selected
            marble = self.board.get_circle(*selected_circles).get_marble()
            if self.is_valid_move(selected_circles, to_circle):
                self.direction = Manager.aligned_two([selected_circles, to_circle])
                # If the move is valid, remove the marble from the starting circle
                self.board.get_circle(*selected_circles).set_marble(None)
                # Then, place the marble in the ending circle
                self.board.get_circle(*to_circle).set_marble(marble)
                # Update the display
                move_to_add = Move([selected_circles], self.direction)
                self.current_player.move_list.append(move_to_add)
                self.switch_turns()
                self.display_board()
            else:
                print("Invalid move")
        else:
            neighbors = []
            for selected_circle in selected_circles:
                neighbors.append(self.board.get_neighbors_with_direction(*selected_circle))

            filtered_neighbours = [
                {direction: pos for direction, pos in neighbour.items() if pos not in selected_circles} for neighbour in
                neighbors]

            aligned = Manager.are_circles_adjacent_and_aligned(selected_circles)

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
                self.move_multiple_marbles(selected_circles, Direction.LEFT)
            elif self.direction == "right":
                self.move_multiple_marbles(selected_circles, Direction.RIGHT)
            elif self.direction == "up_left":
                self.move_multiple_marbles(selected_circles, Direction.UP_LEFT)
            elif self.direction == "up_right":
                self.move_multiple_marbles(selected_circles, Direction.UP_RIGHT)
            elif self.direction == "down_right":
                self.move_multiple_marbles(selected_circles, Direction.DOWN_RIGHT)
            elif self.direction == "down_left":
                self.move_multiple_marbles(selected_circles, Direction.DOWN_LEFT)
            self.switch_turns()
            self.display_board()

    @staticmethod
    def are_circles_adjacent_and_aligned(circles):
        """
        Checks to see if the circles are adjacent and aligned.
        """
        if len(circles) == 2:
            direction = Manager.aligned_two(circles)
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
            return Manager.aligned_three(circles)

    @staticmethod
    def aligned_two(circles):
        """
        Checks to see if two circles are aligned with one another
        """
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

    @staticmethod
    def aligned_three(circles):
        """
        Checks to see if three circles are aligned with one another
        :param circles: is an array of circles
        """
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

    def is_valid_move(self, from_circle, to_circle):
        """
        Checks to see if selected circles to be moved is a valid move
        :param from_circle: the original circle that marble is on
        :param to_circle: the circle and or direction the marble is being moved to
        :return:
        """
        # Check if the to_circle is one of the valid neighbors of from_circle
        valid_neighbors = self.board.get_neighbors(*from_circle)
        if to_circle not in valid_neighbors:
            return False  # to_circle is not adjacent to from_circle

        # Check if the to_circle is empty
        to_circle_marble = self.board.get_circle(*to_circle).get_marble()
        if to_circle_marble is not None:
            return False  # to_circle is not empty

        # Add any additional rules specific to Abalone here
        # For example, marbles cannot move against the direction of push, etc.

        return True  # The move is valid

    def switch_turns(self, save_state=True):
        """
        Switches the turn from one player to another
        :param save_state: is the save state of the game
        """
        self.current_player.reset_timer()
        if save_state:
            self.player1.move_up() if self.player1.get_current_turn() else self.player2.move_up()
            self.save_state()
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        self.player1.flip_turn()
        self.player2.flip_turn()

    def undo_move(self):
        """
        Undoes the last move made in the game
        """

        deleted_state = self.states.remove_last_states()
        if deleted_state:

            self.board = self.states.get_last_board_state()
            score = self.states.get_last_score_state()
            self.player1.set_score(score[0])
            self.player2.set_score(score[1])
            self.player2.reverse_move() if self.player1.get_current_turn() else self.player1.reverse_move()
            self.switch_turns(save_state=False)
            self.current_player.remove_last_move()
            self.display_board()

    def save_state(self):
        """
        Saves the current state of the game and saves it to the states array for a history
        """
        new_board = copy.deepcopy(self.board)
        self.states.add_state(new_board, (self.player1.get_score(), self.player2.get_score()))

    def move_multiple_marbles(self, selected_circles, direction_enum):
        """
        Provides logic to move multiple marbles in one move
        :param selected_circles: is an array of circles containing the marbles that are to be moved
        :param direction_enum: is the direction that will be applied to the marbles
        """
        selected_circles.sort()
        move = Move(selected_circles, direction_enum)
        self.current_player.move_list.append(move)
        if direction_enum in [Direction.DOWN_RIGHT, Direction.LEFT, Direction.DOWN_LEFT]:
            selected_circles.reverse()
        all_but_last = selected_circles[-2::-1]
        last_circle = selected_circles[-1]
        self.recursive_move(last_circle, direction_enum, None)

        for circle in all_but_last:

            next_circle = self.board.get_circle(chr(ord(circle[0]) + direction_enum.value[0]), circle[1] + direction_enum.value[1])
            curr_circle = self.board.get_circle(circle[0], circle[1])
            next_circle.set_marble(curr_circle.get_marble())
            curr_circle.set_marble(None)

    def recursive_move(self, selected_circle, direction, previous_marble=None):
        """
        Recursively moves the marble so that each marble in the back will push the next
        :param selected_circle: the selected circle that has a marble
        :param direction: the direction of the marble traveling as an Enum
        :param previous_marble: the previous marble that was pushed to the current circle
        """
        next_char = chr(ord(selected_circle[0]) + direction.value[0])
        next_num = selected_circle[1] + direction.value[1]
        next_circle = (next_char, next_num)

        curr_marble = self.board.get_circle(selected_circle[0], selected_circle[1]).marble

        # Check if the current marble is the one to be moved, and there is no previous marble
        if curr_marble is not None and previous_marble is None:
            # This means we are at the first marble to be moved, so we should remove it after copying
            self.board.get_circle(selected_circle[0], selected_circle[1]).marble = None

        next_circle_from_board = self.board.get_circle(next_char, next_num)

        curr_marble_copy = copy.deepcopy(curr_marble)

        # If there's no marble in the next position, move the current marble there
        if next_circle_from_board.marble is None:
            next_circle_from_board.marble = curr_marble_copy
            return
        else:
            self.recursive_move(next_circle, direction, curr_marble_copy)

    def get_time_to_display(self):
        """
        Returns each players time as and aggregate of all their moves
        as well as the last moves total time in seconds as well as the number of
        remaining for the players current moves
        """
        player_one_time = self.player1.get_time()
        player_one_agg = self.player1.get_aggregate_time()
        player_one_last = self.player1.get_last_move_time()
        player_two_time = self.player2.get_time()
        player_two_agg = self.player2.get_aggregate_time()
        player_two_last_move = self.player2.get_last_move_time()
        seconds = self.current_player.increment_time()
        if seconds <= 0:
            self.switch_turns()
        return player_one_time, player_one_agg, player_one_last, player_two_time, player_two_agg, player_two_last_move

    def reset_timers(self):
        """
        Resets the current turn timers for both players
        """
        self.player1.clear_clock()
        self.player2.clear_clock()

    def toggle_pause_game(self):
        """
        Toggles the game from paused to unpause
        """
        self.game_paused = not self.game_paused

    def print_moves(self):
        """
        Prints the current games players moves to the terminal
        """
        print(f"Player 1\t\t\t\t\t\t\t\t\t\t\tPlayer 2")

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
    manager.start_game("German Daisy")
