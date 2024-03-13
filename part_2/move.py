from directions import Direction
class Move():

    def __init__(self, move_type, direction, marbles):
        self.move_type = move_type
        self.direction = direction
        self.marbles = marbles

    def get_move_type(self):
        return self.move_type

    def get_direction(self):
        return self.direction

    def get_marbles(self):
        return self.marbles

    def get_row_letter(self, index):
        return chr(ord('A') + index - 1)

    def __str__(self):
        if self.move_type == 'i':
            return f"{self.move_type}-{self.get_row_letter(self.marbles[0][0])}{self.marbles[0][1]}-{self.direction.value}"
        else:
            return f"{self.move_type}-{self.get_row_letter(self.marbles[0][0])}{self.marbles[0][1]}-{self.get_row_letter(self.marbles[-1][0])}{self.marbles[-1][1]}-{self.direction.value}"
