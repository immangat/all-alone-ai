import re
from state_space_gen import StateSpaceGen
from board import Board
class IOHandler:

    def __init__(self):
        self.board_string =[]
        self.player_color = None
        self.file_number = None

    def create_outcomes_from_board_file(self, filename):
        self.extract_data(filename)
        self.create_outputs()

    def extract_data(self, filename):
        match = re.search(r'Test(\d+)\.input', filename)
        if match:
            self.file_number = int(match.group(1))
        else:
            print("Invalid filename format. Couldn't extract the file number.")
            return


        with open(filename, 'r') as file:
            # Read the first line and set self.player_color
            self.player_color = file.readline().strip()

            # Read the second line and set self.board_string
            self.board_string = file.readline().strip().split(',')

    def get_board_string(self):
        return self.board_string

    def get_player_color(self):
        return self.player_color

    def create_outputs(self):
        if self.player_color is None:
            print("No input file provided.")
            return

        board = Board.create_custom_board(self.board_string)
        if board is not None:
            gen = StateSpaceGen()
            gen.generate_state_space(board, self.player_color)

            moves = gen.get_moves()
            boards = gen.get_boards()

            board_output_file = f'Test{self.file_number}.board'
            move_output_file = f'Test{self.file_number}.move'

            # boards
            with open(board_output_file, 'w') as board_file:
                board_file.write('\n'.join(map(str, boards)))

            # moves
            with open(move_output_file, 'w') as move_file:
                move_file.write('\n'.join(map(str, moves)))
