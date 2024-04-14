import re
from state_space_gen import StateSpaceGen
from board import Board
import json


class IOHandler:
    """
    Class responsible for handling input and output operations for the game.

    Attributes:
    - board_string (list): A list representing the board state.
    - player_color (str): The color of the player ('b' for black, 'w' for white).
    - file_number (int): The number extracted from the input filename.
    """

    def __init__(self):
        """
        Initialize the IOHandler instance.
        """
        self.board_string = []
        self.player_color = None
        self.file_number = None

    def create_outcomes_from_board_file(self, filename):
        """
        Create outcome files (board and move) based on the input board file.

        Args:
        - filename (str): The filename of the input board file.
        """
        self.extract_data(filename)
        self.create_outputs()

    def extract_data(self, filename):
        """
        Extract data (player color and board state) from the input board file.

        Args:
        - filename (str): The filename of the input board file.
        """
        match = re.search(r'Test(\d+)\.input', filename)
        if match:
            self.file_number = int(match.group(1))
        else:
            print("Invalid filename format. Couldn't extract the file number.")
            return

        with open(filename, 'r') as file:
            self.player_color = file.readline().strip()
            self.board_string = file.readline().strip().split(',')

    @staticmethod
    def read_transposition_table_from_file(player_color):
        """
        Read the transposition table from a file.

        Args:
        - player_color (str): The color of the player ('b' for black, 'w' for white).

        Returns:
        - dict: The transposition table loaded from the file.
        """
        table_name = f"TranspositionTable{player_color}.json"
        try:
            with open(table_name, 'r') as file:
                transposition_table = json.load(file)
                transposition_table = {int(key): value for key, value in transposition_table.items()}
                print(f"Transposition table for player {player_color} loaded successfully.")
                return transposition_table
        except FileNotFoundError:
            print(f"No transposition table found for player {player_color}.")
            return None

    @staticmethod
    def save_transposition_table(transposition_table_data, player_color):
        """
        Save the transposition table to a file.

        Args:
        - transposition_table_data (dict): The transposition table data to be saved.
        - player_color (str): The color of the player ('b' for black, 'w' for white).
        """
        table_name = f"TranspositionTable{player_color}.json"
        with open(table_name, 'w') as file:
            json.dump(transposition_table_data, file, indent=None)
            print(f"Transposition table for player {player_color} saved successfully.")

    def get_board_string(self):
        """
        Get the board state as a list of strings.

        Returns:
        - list: The board state.
        """
        return self.board_string

    def get_player_color(self):
        """
        Get the player's color.

        Returns:
        - str: The player's color ('b' for black, 'w' for white).
        """
        return self.player_color

    def create_outputs(self):
        """
        Create output files (board and move) based on the extracted data.
        """
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
