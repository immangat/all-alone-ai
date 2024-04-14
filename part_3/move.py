class Move:
    """
       Class representing a move in the game.

       Attributes:
       - move_type (str): The type of move ('i' for insertion, 's' for sliding).
       - direction (str): The direction of the move ('R', 'L', 'U', 'D', 'UR', 'UL', 'DR', 'DL').
       - marbles (list): A list of tuples representing the marbles involved in the move.
       - sumito (bool): Indicates if the move is a sumito move (default is False).
       """

    def __init__(self, move_type, direction, marbles, sumito=False):
        self.move_type = move_type
        self.direction = direction
        self.marbles = marbles
        self.sumito = sumito

    def get_move_type(self):
        return self.move_type

    def get_direction(self):
        return self.direction

    def get_marbles(self):
        return self.marbles

    def get_row_letter(self, index):
        return chr(ord('A') + index - 1)

    def get_sumito(self):
        return self.sumito

    @classmethod
    def string_to_move(cls, move_str):
        """
        Parse the given string and return a Move object.
        :param move_str: The string representation of the move.
        :return: A Move object.
        """
        move_parts = move_str.split('-')
        move_type = move_parts[0]
        direction = move_parts[-1]

        if move_type == 'i':
            row_letter, col = move_parts[1][0], int(move_parts[1][1:])
            marbles = [(ord(row_letter) - ord('A') + 1, col)]
        elif move_type == 's':
            start_row_letter, start_col = move_parts[1][0], int(move_parts[1][1:])
            end_row_letter, end_col = move_parts[2][0], int(move_parts[2][1:])
            marbles = [(ord(row_letter) - ord('A') + 1, start_col) for row_letter in
                       range(start_row_letter, end_row_letter + 1)]
        else:
            raise ValueError("Invalid move type")

        return cls(move_type, direction, marbles)

    def __str__(self):
        if self.move_type == 'i':
            return f"{self.move_type}-{self.get_row_letter(self.marbles[0][0])}{self.marbles[0][1]}-{self.direction.value}"
        else:
            return f"{self.move_type}-{self.get_row_letter(self.marbles[0][0])}{self.marbles[0][1]}-{self.get_row_letter(self.marbles[-1][0])}{self.marbles[-1][1]}-{self.direction.value}"
