from circle import Circle
from marble import Marble
import copy


class Board:
    def __init__(self):
        self.circles = {}  # This will map board coordinates to Circle objects
        self.starting_numbers = [5, 4, 3, 2, 1, 1, 1, 1, 1]
        self.rows = [5, 6, 7, 8, 9, 8, 7, 6, 5]
        self.initBoard()

    def initBoard(self):
        row_labels = "IHGFEDCBA"

        for i, num in enumerate(self.rows):
            for j in range(num):
                letter = row_labels[i]
                number = j + self.starting_numbers[i]
                circle = Circle(letter, number)
                self.circles[(letter, number)] = circle


    def getCircle(self, row, col):
        # Return the Circle object at the given row and col
        return self.circles.get((row, col))

    def printCircleStatus(self):
        for circle in self.circles.values():
            print((circle.getPosition()))
            hasMarble = "False" if circle.isEmpty() else "True"
            print(hasMarble)

    def isWithinBounds(self, row, col):
        # Check if the row and col are within the hexagonal board bounds
        if row in 'ABCDEFG' and 1 <= col <= 9:
            index = 'ABCDEFG'.index(row)
            if index < 3:  # Rows A, B, C
                return col <= 5 + index
            elif index < 5:  # Rows D, E
                return True
            else:  # Rows F, G
                return col >= index - 4
        return False

    def setupBoard(self, setup_type="default"):
        self.clearBoard()

        if setup_type == "default":
            self.setupDefault()
        elif setup_type == "german_daisy":
            self.setupGermanDaisy()
        elif setup_type == "belgian_daisy":
            self.setupBelgianDaisy()
        elif setup_type == "notation":
            self.setupForNotation()

    def checkPath(self, from_row, from_col, to_row, to_col):
        # Implement logic to check the path for a move
        pass

    def clearBoard(self):
        for position, circle in self.circles.items():
            circle.setMarble(None)

    def setupDefault(self):
        for i, row_label in enumerate("IHGFEDCBA"):
            for j in range(self.rows[i]):
                if i < 2 or (
                        i == 2 and 2 <= j <= 4):  # Place black marbles in the bottom two rows and the center positions
                    self.placeMarble(row_label, j + self.starting_numbers[i], Marble("Black"))
                elif i > 6 or (
                        i == 6 and 2 <= j <= 4):  # Place white marbles in the top two rows and the center positions
                    self.placeMarble(row_label, j + self.starting_numbers[i], Marble("White"))

        for position, circle in self.circles.items():
            print(f"tile {position}{circle.getMarble()}")

    def setupForNotation(self):
        self.placeMarble("E", 5 + 1, Marble("Black"))
        self.placeMarble("E", 6 + 1, Marble("Black"))
        self.placeMarble("E", 7 + 1, Marble("Black"))
        # self.placeMarble("E", 5 + 1, Marble("Black"))
        # self.placeMarble("D", 5 + 1, Marble("Black"))
        for position, circle in self.circles.items():
            print(f"tile {position}{circle.getMarble()}")

    def setupGermanDaisy(self):
        black_initial = [('C', 2), ('G', 8)]
        black_positions = Board.flower_positions(black_initial)

        white_initial = [('G', 4), ('C', 6)]
        white_positions = Board.flower_positions(white_initial)

        for position in black_positions:
            self.placeMarble(position[0], position[1], Marble("Black"))

        for position in white_positions:
            self.placeMarble(position[0], position[1], Marble("White"))

    def setupBelgianDaisy(self):
        black_initial = [('B', 2), ('H', 8)]
        black_positions = Board.flower_positions(black_initial)

        white_initial = [('H', 5), ('B', 5)]
        white_positions = Board.flower_positions(white_initial)

        for position in black_positions:
            self.placeMarble(position[0], position[1], Marble("Black"))

        for position in white_positions:
            self.placeMarble(position[0], position[1], Marble("White"))

    def __deepcopy__(self, memo):
        # Create a new Board with deep copies of circles
        new_board = Board()
        new_board.circles = {pos: copy.deepcopy(circle, memo) for pos, circle in self.circles.items()}
        memo[id(self)] = new_board
        return new_board

    @staticmethod
    def flower_positions(lst):
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

    def placeMarble(self, row, col, marble):
        # Helper method to place a marble on the board at the specified position
        position = (row, col)
        self.circles[position].setMarble(marble)

    def get_neighbors(self, row, col):
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
            if self.isWithinBounds(neighbor_row, neighbor_col):
                neighbors.append((neighbor_row, neighbor_col))
        return neighbors
