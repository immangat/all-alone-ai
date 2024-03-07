from circle import Circle
from marble import Marble
import copy


class Board:
    """
    This class is the representation of an abalone board
    """
    def __init__(self):
        """
        Initialise the board with the empty board
        """
        self.circles = {}  # This will map board coordinates to Circle objects
        self.starting_numbers = [5, 4, 3, 2, 1, 1, 1, 1, 1]
        self.rows = [5, 6, 7, 8, 9, 8, 7, 6, 5]
        self.init_board()

    def init_board(self):
        row_labels = "IHGFEDCBA"

        for i, num in enumerate(self.rows):
            for j in range(num):
                letter = row_labels[i]
                number = j + self.starting_numbers[i]
                circle = Circle(letter, number)
                self.circles[(letter, number)] = circle

    def get_circle(self, row, col):
        """
        Getter for the circle
        :param row: is a character on the board
        :param col: is a number on the board
        :return: is the circle with the given number
        """
        # Return the Circle object at the given row and col
        return self.circles.get((row, col))

    @staticmethod
    def is_within_bounds(row, col):
        """
        Checks if the given number is within the bounds of the board
        :param row: is a character on the board
        :param col: is a number in the board
        :return: is a Boolean value
        """
        # Check if the row and col are within the hexagonal board bounds
        if row in 'ABCDEFGHI' and 1 <= col <= 9:
            index = 'ABCDEFGHI'.index(row)
            if index < 3:  # Rows A, B, C
                return col <= 5 + index
            elif index < 5:  # Rows D, E
                return True
            else:  # Rows F, G, I, H
                return col >= index - 4
        return False

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

    def check_path(self, from_row, from_col, to_row, to_col):
        # Implement logic to check the path for a move
        pass

    def clear_board(self):
        """
        Clears the board of marbles
        """
        for position, circle in self.circles.items():
            circle.set_marble(None)

    def setup_default(self):
        """
        Sets up the board for a game with a default setup type
        """
        for i, row_label in enumerate("IHGFEDCBA"):
            for j in range(self.rows[i]):
                if i < 2 or (
                        i == 2 and j >= 2 and j <= 4):  # Place black marbles in the bottom two rows and the center pos
                    self.place_marble(row_label, j + self.starting_numbers[i], Marble("Black"))
                elif i > 6 or (
                        i == 6 and j >= 2 and j <= 4):  # Place white marbles in the top two rows and the center pos
                    self.place_marble(row_label, j + self.starting_numbers[i], Marble("White"))

        for position, circle in self.circles.items():
            print(f"tile {position}{circle.get_marble()}")

    def setup_german_daisy(self):
        """
        Sets up the marbles on the board for a game with
        in the german daisy setup type
        """
        black_initial = [('C', 2), ('G', 8)]
        black_positions = Board.flower_positions(black_initial)

        white_initial = [('G', 4), ('C', 6)]
        white_positions = Board.flower_positions(white_initial)

        for position in black_positions:
            self.place_marble(position[0], position[1], Marble("Black"))

        for position in white_positions:
            self.place_marble(position[0], position[1], Marble("White"))

    def setup_belgian_daisy(self):
        """
        Sets up the marbles on the board for a game with
        in the belgian daisy setup type
        """
        black_initial = [('B', 2), ('H', 8)]
        black_positions = Board.flower_positions(black_initial)

        white_initial = [('H', 5), ('B', 5)]
        white_positions = Board.flower_positions(white_initial)

        for position in black_positions:
            self.place_marble(position[0], position[1], Marble("Black"))

        for position in white_positions:
            self.place_marble(position[0], position[1], Marble("White"))

    def __deepcopy__(self, memo):
        # Create a new Board with deep copies of circles
        new_board = Board()
        new_board.circles = {pos: copy.deepcopy(circle, memo) for pos, circle in self.circles.items()}
        memo[id(self)] = new_board
        return new_board

    @staticmethod
    def flower_positions(lst):
        """
        Given a list of lists, return a list of tuples of the surrounding tuples
        :param lst: is a list of tuples
        :return: is a list of tuples of (position)
        """
        new_list = []
        for row, col in lst:
            new_list.append((row, col))
            rows_labels = "ABCDEFGHI"
            index = rows_labels.index(row)
            new_list.append((row, col + 1))
            new_list.append((row, col - 1))
            bottom = rows_labels[index - 1]
            top = rows_labels[index + 1]
            new_list.append((top, col))
            new_list.append((top, col + 1))
            new_list.append((bottom, col))
            new_list.append((bottom, col - 1))

        return new_list

    def place_marble(self, row, col, marble):
        """
        Places a marble on the board
        :param row: is the row of the board as Character
        :param col: is the col of the board as an Int
        :param marble: is the marble
        """
        position = (row, col)
        self.circles[position].set_marble(marble)

    def get_neighbors(self, row, col):
        """ Gets all the surrounding circles of the board for a given row and col"""
        directions = [
            ('left', (0, -1)),
            ('right', (0, 1)),
            ('up_left', (1, 0)),
            ('up_right', (1, 1)),
            ('down_left', (-1, -1)),
            ('down_right', (-1, 0)),
        ]
        neighbors = []
        for direction, (dr, dc) in directions:
            neighbor_row = chr(ord(row) + dr)
            neighbor_col = col + dc
            if Board.is_within_bounds(neighbor_row, neighbor_col):
                neighbors.append((neighbor_row, neighbor_col))
        return neighbors

    def get_neighbors_with_direction(self, row, col):
        """
        Gets all the surrounding circles of the board for a given row and col
        :param row: is a row of the board as a Character
        :param col: is the column of the board as an Int
        :return: is a list of tuples of the surrounding circles of the board
        with no overlap between the other neighbours of other circles
        """
        directions = {
            'left': (0, -1),
            'right': (0, 1),
            'up_left': (1, 0),  # Adjusted for hexagonal grid
            'up_right': (1, 1),  # Adjusted for hexagonal grid
            'down_left': (-1, -1),  # Adjusted for hexagonal grid
            'down_right': (-1, 0),  # Adjusted for hexagonal grid
        }
        neighbors = {}
        for direction, (dr, dc) in directions.items():
            neighbor_row = chr(ord(row) + dr)
            neighbor_col = col + dc
            if Board.is_within_bounds(neighbor_row, neighbor_col):
                neighbors[direction] = (neighbor_row, neighbor_col)
        return neighbors

    def get_coordinates(self, circle):
        """
        Gets the coordinates of the given circle
        :param circle: Is a circle on the board
        :return: the circle if it is on the board or None otherwise
        """
        for coord, circ in self.circles.items():
            if circ == circle:
                return coord
        return None

