from board import Board
from directions import Direction
from move import Move
from state import State
import copy


class StateSpaceGen:
    """
    Class for generating the state space for a given board and player color.
    """

    def __init__(self):
        """
        Initialize the StateSpaceGen object.
        """
        self.board = None
        self.curr_player = None
        self.moves = []
        self.boards = []

    def get_boards(self):
        """
        Get the generated boards.

        Returns:
        - List: A list of board states.
        """
        return self.boards

    def get_moves(self):
        """
        Get the generated moves.

        Returns:
        - List: A list of Move objects.
        """
        return self.moves

    def clear_states(self):
        """
        Clear the generated states.
        """
        self.__init__()

    def get_index_from_board(self, board):
        """
        Get the index of a board state in the generated boards list.

        Args:
        - board: The board state.

        Returns:
        - int: The index of the board state.
        """
        return self.boards.index(board)

    def get_index_from_board_string(self, board):
        """
        Get the index of a board state from its string representation.

        Args:
        - board: The string representation of the board state.

        Returns:
        - int: The index of the board state.
        """
        board_string = str(board.get_circles())
        for b in self.boards:
            if board_string == str(b):
                return self.boards.index(b)

    def generate_state_space(self, board, player_color):
        """
        Generate the state space for a given board and player color.

        Args:
        - board: The board state.
        - player_color: The color of the current player.
        """
        self.board = board
        self.curr_player = player_color

        curr_marbles = self.board.get_marbles_by_color(self.curr_player)
        self.check_single_marble(curr_marbles)

    def check_single_marble(self, curr_marbles):
        """
        Check for possible moves with a single marble.

        Args:
        - curr_marbles: List of coordinates of current player's marbles.
        """
        for marble in curr_marbles:
            for direction in Direction:
                next_marble_logic = self.get_direction_logic(direction)
                neighbor = (marble[0] + next_marble_logic[0], marble[1] + next_marble_logic[1])
                if neighbor in Board.BOARD_COORD:
                    if self.board.get_marble(neighbor) == self.curr_player:
                        two_marbles = [marble, neighbor]
                        self.check_mult_marbles(two_marbles, direction)
                    elif self.board.get_marble(neighbor) is None:
                        new_move = Move("i", direction, [marble])
                        new_board_dict = self.board.get_circles()
                        new_board_dict[neighbor] = self.curr_player
                        new_board_dict[marble] = None
                        self.moves.append(new_move)
                        self.boards.append(new_board_dict)

    def check_mult_marbles(self, coords, direction):
        """
        Check for possible moves with multiple marbles in a direction.

        Args:
        - coords: List of coordinates of marbles involved in the move.
        - direction: The direction of the move.
        """
        # check inline movement
        inline_logic = self.get_direction_logic(direction)
        next_in_line = (coords[-1][0] + inline_logic[0], coords[-1][1] + inline_logic[1])
        if next_in_line in Board.BOARD_COORD:
            if self.board.get_marble(next_in_line) == self.curr_player:
                if len(coords) < 3:
                    three_marbles = coords + [next_in_line]
                    self.check_mult_marbles(three_marbles, direction)
            elif self.board.get_marble(next_in_line) is None:
                new_move = Move("i", direction, coords)
                new_board_dict = self.board.get_circles()
                new_board_dict[next_in_line] = self.curr_player
                new_board_dict[coords[0]] = None
                self.moves.append(new_move)
                self.boards.append(new_board_dict)
            else:
                self.check_sumito(coords, direction)

        # now check side movement
        opposite_inline = self.get_inline_opposite(direction)
        possible_side = [posDir for posDir in Direction if posDir != direction and posDir != opposite_inline]
        duplicate_check = True if coords[-1][1] < coords[0][1] or coords[-1][0] < coords[0][0] else False
        if not duplicate_check:
            for posDir in possible_side:
                direction_logic = self.get_direction_logic(posDir)
                blocked = False
                for coord in coords:
                    next_in_side = (coord[0] + direction_logic[0], coord[1] + direction_logic[1])
                    if next_in_side not in Board.BOARD_COORD or self.board.get_marble(next_in_side) is not None:
                        blocked = True
                        break
                if not blocked:
                    new_board_dict = self.board.get_circles()
                    for coord in coords:
                        next_in_side = (coord[0] + direction_logic[0], coord[1] + direction_logic[1])
                        new_board_dict[next_in_side] = self.curr_player
                        new_board_dict[coord] = None
                    new_move = Move("s", posDir, coords)
                    self.moves.append(new_move)
                    self.boards.append(new_board_dict)

    def check_sumito(self, coords, direction):
        """
        Check for sumito move.

        Args:
        - coords: List of coordinates of marbles involved in the move.
        - direction: The direction of the move.
        """
        inline_logic = self.get_direction_logic(direction)
        next_coord = (coords[-1][0] + inline_logic[0], coords[-1][1] + inline_logic[1])
        opponent_marbles = 1
        pushable = True
        while next_coord in Board.BOARD_COORD and self.board.get_marble(next_coord) is not None:
            next_coord_marble = self.board.get_marble(next_coord)
            if next_coord_marble == self.curr_player or opponent_marbles > 2 or len(coords) <= opponent_marbles:
                pushable = False
                break
            next_coord = (next_coord[0] + inline_logic[0], next_coord[1] + inline_logic[1])
            opponent_marbles += 1
        if pushable:
            new_move = Move("i", direction, coords, sumito=True)
            opponent_color = self.board.get_marble((coords[-1][0] + inline_logic[0], coords[-1][1] + inline_logic[1]))
            new_board_dict = self.board.get_circles()
            if next_coord in Board.BOARD_COORD:
                new_board_dict[next_coord] = opponent_color
            new_board_dict[(coords[-1][0] + inline_logic[0], coords[-1][1] + inline_logic[1])] = self.curr_player
            new_board_dict[coords[0]] = None
            self.moves.append(new_move)
            self.boards.append(new_board_dict)

    def get_inline_opposite(self, direction):
        """
        Get the opposite inline direction.

        Args:
        - direction: The direction.

        Returns:
        - Direction: The opposite inline direction.
        """
        opposite_map = {
            Direction.UP_LEFT: Direction.DOWN_RIGHT,
            Direction.DOWN_RIGHT: Direction.UP_LEFT,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.UP_RIGHT: Direction.DOWN_LEFT,
            Direction.DOWN_LEFT: Direction.UP_RIGHT
        }
        return opposite_map.get(direction, None)

    def get_direction_logic(self, direction):
        """
        Get the logic for a given direction.

        Args:
        - direction: The direction.

        Returns:
        - Tuple: The logic for the direction.
        """
        if direction == Direction.UP_RIGHT:
            return (1, 1)
        elif direction == Direction.RIGHT:
            return (0, 1)
        elif direction == Direction.DOWN_RIGHT:
            return (-1, 0)
        elif direction == Direction.DOWN_LEFT:
            return (-1, -1)
        elif direction == Direction.LEFT:
            return (0, -1)
        else:
            return (1, 0)

    def validate_move(self, board, marbles, direction):
        """
        Validate a move based on the given board, marbles, and direction.

        Args:
        - board: The board state.
        - marbles: List of coordinates of marbles involved in the move.
        - direction: The direction of the move.

        Returns:
        - Tuple: A tuple containing the Move object and the new board state if the move is valid, otherwise (None, None).
        """
        self.board = board
        player_color = self.board.get_marble(marbles[0])
        sort_marbles = sorted(marbles, key=lambda x: (x[0], x[1]))
        self.clear_states()
        self.generate_state_space(board, player_color)
        move_state = self.find_move_in_list(sort_marbles, direction)

        if move_state is not None:
            move_index = self.moves.index(move_state)
            board_state = self.boards[move_index]
            return (move_state, board_state)
        return (None, None)

    def find_move_in_list(self, marbles, direction):
        """
        Find a move in the list of generated moves.

        Args:
        - marbles: List of coordinates of marbles involved in the move.
        - direction: The direction of the move.

        Returns:
        - Move: The Move object if found, otherwise None.
        """
        for move in self.moves:
            sorted_marbles = sorted(move.get_marbles(), key=lambda x: (x[0], x[1]))
            if direction == move.get_direction() and marbles == sorted_marbles:
                return move
        return None

    def get_neighbors(self, coord):
        """
        Get the neighbors of a given coordinate.

        Args:
        - coord: The coordinate.

        Returns:
        - Tuple: A tuple containing a list of neighbor coordinates and a list of corresponding directions.
        """
        neighbors = []
        directions_temp = [direction for direction in Direction]
        neighbors_directions = []
        x = coord[0]
        y = coord[1]
        temp = [(x + 1, y + 1), (x, y + 1), (x - 1, y), (x - 1, y - 1), (x, y - 1), (x + 1, y)]
        for neighbor in temp:
            if neighbor in Board.BOARD_COORD:
                neighbors.append(neighbor)
                neighbors_directions.append(directions_temp[temp.index(neighbor)])
        return (neighbors, neighbors_directions)

    def create_states(self):
        """
        Create State objects based on the generated moves and boards.

        Returns:
        - List: A list of State objects.
        """
        states_list = []
        for move in self.moves:
            move_index = self.moves.index(move)
            new_state = State(move, self.board[move_index])
            self.states.append(new_state)
        return states_list
