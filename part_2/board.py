import copy


class Board:
    """
    This class is the representation of an abalone board
    """
    BOARD_COORD = [
        (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
        (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
        (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
        (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
        (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9),
        (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9),
        (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9),
        (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)
    ]

    def __init__(self):
        """
        Initialise the board with the empty board
        """

        self.circles = {}  # This will map board coordinates to Circle objects
        # self.starting_numbers = [5, 4, 3, 2, 1, 1, 1, 1, 1]
        # self.rows = [5, 6, 7, 8, 9, 8, 7, 6, 5]
        self.init_board()

    def init_board(self):

        for coord in self.BOARD_COORD:
            self.circles[coord] = None

    def get_circle(self, row, col):
        """
        Getter for the circle
        :param row: is a character on the board
        :param col: is a number on the board
        :return: is the circle with the given number
        """
        # Return the Circle object at the given row and col
        return self.circles.get((row, col))

    def set_marble(self, coord, color=None):
        self.circles[coord] = color

    @staticmethod
    def is_within_bounds(coord):
        """
        Checks if the given number is within the bounds of the board
        :param row: is a character on the board
        :param col: is a number in the board
        :return: is a Boolean value
        """
        # Check if the row and col are within the hexagonal board bounds
        return coord in Board.BOARD_COORD

    def setup_board(self, setup_type="Default"):
        """
        Sets up the board for a game with a given setup type
        :param setup_type: A string representing the setup type
        """
        self.clear_board()

        if setup_type == "Default":
            self.setup_default()
        elif setup_type == "German Daisy":
            self.setup_german_daisy()
        elif setup_type == "Belgian Daisy":
            self.setup_belgian_daisy()

    def clear_board(self):
        """
        Clears the board of marbles
        """
        self.circles = {}
        self.init_board()

    def setup_default(self):
        """
        Sets up the board for a game with a default setup type
        """
        black_marbles = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                         (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                         (3, 3), (3, 4), (3, 5)]

        white_marbles = [(7, 5), (7, 6), (7, 7),
                         (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9),
                         (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)]

        for coord in black_marbles:
            self.set_marble(coord, "b")

        for coord in white_marbles:
            self.set_marble(coord, "w")

    def setup_german_daisy(self):
        """
        Sets up the marbles on the board for a game with
        in the german daisy setup type
        """
        black_marbles = [
            (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 2), (4, 3),
            (6, 7), (6, 8), (7, 7), (7, 8), (7, 9), (8, 8), (8, 9)
        ]

        white_marbles = [
            (2, 5), (2, 6), (3, 5), (3, 6), (3, 7), (4, 6), (4, 7),
            (6, 3), (6, 4), (7, 3), (7, 4), (7, 5), (8, 4), (8, 5)
        ]

        for coord in black_marbles:
            self.set_marble(coord, "b")

        for coord in white_marbles:
            self.set_marble(coord, "w")

    def setup_belgian_daisy(self):
        """
        Sets up the marbles on the board for a game with
        in the belgian daisy setup type
        """
        black_marbles = [
            (1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3),
            (7, 7), (7, 8), (8, 7), (8, 8), (8, 9), (9, 8), (9, 9)
        ]

        white_marbles = [
            (1, 4), (1, 5), (2, 4), (2, 5), (2, 6), (3, 5), (3, 6),
            (7, 4), (7, 5), (8, 4), (8, 5), (8, 6), (9, 5), (9, 6)
        ]

        for coord in black_marbles:
            self.set_marble(coord, "b")

        for coord in white_marbles:
            self.set_marble(coord, "w")

    def __deepcopy__(self, memo):
        # Create a new Board with deep copies of circles
        new_board = Board()
        new_board.circles = copy.deepcopy(self.circles, memo)
        memo[id(self)] = new_board
        return new_board

    def get_marble(self, coord):
        return self.circles[coord]

    def get_white_marbles(self):
        white_marbles = []
        for coord in self.BOARD_COORD:
            if self.get_marble(coord) == "w":
                white_marbles.append(coord)
        return white_marbles

    def get_black_marbles(self):
        black_marbles = []
        for coord in self.BOARD_COORD:
            if self.get_marble(coord) == "b":
                black_marbles.append(coord)
        return black_marbles

    def get_row_letter(self, index):
        return chr(ord('A') + index - 1)

    def __str__(self):
        board_str = ""

        for marble in self.get_black_marbles() + self.get_white_marbles():
            row_letter = self.get_row_letter(marble[0])
            coord_str = f"{row_letter}{marble[1]}{self.get_marble(marble)}"
            board_str += f"{coord_str}, "

        # Remove the trailing comma and space
        return board_str.rstrip(', ')

    # def get_neighbors(self, row, col):
    #     """ Gets all the surrounding circles of the board for a given row and col"""
    #     directions = [
    #         ('left', (0, -1)),
    #         ('right', (0, 1)),
    #         ('up_left', (1, 0)),
    #         ('up_right', (1, 1)),
    #         ('down_left', (-1, -1)),
    #         ('down_right', (-1, 0)),
    #     ]
    #     neighbors = []
    #     for direction, (dr, dc) in directions:
    #         neighbor_row = chr(ord(row) + dr)
    #         neighbor_col = col + dc
    #         if Board.is_within_bounds(neighbor_row, neighbor_col):
    #             neighbors.append((neighbor_row, neighbor_col))
    #     return neighbors
    #
    # def get_neighbors_with_direction(self, row, col):
    #     """
    #     Gets all the surrounding circles of the board for a given row and col
    #     :param row: is a row of the board as a Character
    #     :param col: is the column of the board as an Int
    #     :return: is a list of tuples of the surrounding circles of the board
    #     with no overlap between the other neighbours of other circles
    #     """
    #     directions = {
    #         'left': (0, -1),
    #         'right': (0, 1),
    #         'up_left': (1, 0),  # Adjusted for hexagonal grid
    #         'up_right': (1, 1),  # Adjusted for hexagonal grid
    #         'down_left': (-1, -1),  # Adjusted for hexagonal grid
    #         'down_right': (-1, 0),  # Adjusted for hexagonal grid
    #     }
    #     neighbors = {}
    #     for direction, (dr, dc) in directions.items():
    #         neighbor_row = chr(ord(row) + dr)
    #         neighbor_col = col + dc
    #         if Board.is_within_bounds(neighbor_row, neighbor_col):
    #             neighbors[direction] = (neighbor_row, neighbor_col)
    #     return neighbors
