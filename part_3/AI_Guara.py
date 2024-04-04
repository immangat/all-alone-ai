from state_space_gen import StateSpaceGen
from board import Board
from player import AIPlayer
from IO_handler import IOHandler
import time
import random


class AIAgentTester():
    POINT_VALUES = [
        -2, -2, -2, -2, -2,
        -2, 0, 0, 0, 0, -2,
        -2, 0, 1, 1, 1, 0, -2,
        -2, 0, 1, 3, 3, 1, 0, -2,
        -2, 0, 1, 3, 5, 3, 1, 0, -2,
        -2, 0, 1, 3, 3, 1, 0, -2,
        -2, 0, 1, 1, 1, 0, -2,
        -2, 0, 0, 0, 0, -2,
        -2, -2, -2, -2, -2
    ]

    INFINITY = float('inf')

    def __init__(self, color, depth):
        self.depth = depth
        self.color = color
        self.weights = self.get_weights()
        self.transposition_table = {}
        self.inner_transposition_table = {}

    # def _calculate_move(self, board, queue, start_time, **kwargs):
    #     return self.get_best_move(board, start_time, queue)

    def get_color(self):
        return self.color

    def load_transposition_table(self):
        transposition_table_data = IOHandler.read_transposition_table_from_file(self.color)
        if transposition_table_data is not None:
            self.transposition_table = transposition_table_data

    def get_best_move(self, board):
        self.load_transposition_table()
        print(f"transposition_table: {len(self.transposition_table)}")
        best_move = None
        best_board = None
        best_score = -self.INFINITY if self.color == 'b' else self.INFINITY
        gen = StateSpaceGen()
        gen.generate_state_space(board, self.color)

        alpha = -self.INFINITY
        beta = self.INFINITY

        ordered_boards = self.state_ordering(gen.get_boards())

        for gen_board in ordered_boards:

            hash_key = gen_board.hash_board()

            if hash_key in self.transposition_table:
                score = self.transposition_table[hash_key]
            else:
                if self.color == 'b':
                    score = self.alpha_beta(gen_board, self.depth - 1, alpha, beta, 'w')
                    self.transposition_table[hash_key] = score
                else:
                    score = self.alpha_beta(gen_board, self.depth - 1, alpha, beta, 'b')
                    self.transposition_table[hash_key] = score

            if (self.color == 'b' and score > best_score) or (self.color == 'w' and score < best_score):
                best_score = score
                best_move = gen.get_moves()[gen.get_index_from_board_string(gen_board)]
                best_board = gen_board

            # Update alpha or beta for pruning
            if self.color == 'b':
                alpha = max(alpha, best_score)
            else:
                beta = min(beta, best_score)

            # Perform pruning
            if beta <= alpha:
                break

        IOHandler.save_transposition_table(self.transposition_table, self.color)

        print(f"Best move: {best_move}")
        return best_move, best_board

    def evaluate_position(self, board, max_player):
        # number_off_grid
        black_score = board.num_marbles_left_by_color("b") * self.weights["b_off"]
        white_score = board.num_marbles_left_by_color("w") * self.weights["w_off"]

        # points for position (the closer to the center, the better)

        for coord in Board.BOARD_COORD:
            index = Board.BOARD_COORD.index(coord)
            if board.get_marble(coord) == "b":
                black_score += self.POINT_VALUES[index] * self.weights["b_pos"]
            elif board.get_marble(coord) == "w":
                white_score += self.POINT_VALUES[index] * self.weights["w_pos"]

        # points for coherence
        black_score += self.calculate_group_score("b", board) * self.weights["b_coherence"]
        white_score += self.calculate_group_score("w", board) * self.weights["w_coherence"]

        return black_score + white_score

    def calculate_group_score(self, player, board):
        marbles = board.get_marbles_by_color(player)
        visited = set()
        group_score = 0

        for marble in marbles:
            if marble not in visited:
                group_size = self.dfs_group_size(marble, player, board, visited)
                group_score += group_size
        return group_score

    @staticmethod
    def dfs_group_size(marble, player, board, visited):
        stack = [marble]
        group_size = 0
        group_bonus = 0

        while stack:
            current_marble = stack.pop()
            if current_marble not in visited:
                visited.add(current_marble)
                group_size += 1
                neighbors = board.get_neighbors_only(current_marble)
                for neighbor in neighbors:
                    if board.get_marble(neighbor) == player:
                        group_bonus += 1
                        stack.append(neighbor)
        return group_size + group_bonus

    @staticmethod
    def get_weights():
        """
        Using an adapted AI_abalone weight system
        """
        weights = {}
        weights["b_off"] = 50
        weights["w_off"] = -50
        weights["b_pos"] = 4
        weights["w_pos"] = -4
        weights["b_coherence"] = 1
        weights["w_coherence"] = -1
        return weights

    def alpha_beta(self, board, depth, alpha, beta, current_player):

        hash_key = board.hash_board()
        if hash_key in self.inner_transposition_table:
            return self.inner_transposition_table[hash_key]
        if depth == 0:
            return self.evaluate_position(board, current_player)

        gen = StateSpaceGen()
        gen.generate_state_space(board, current_player)
        if current_player == "b":
            value = -self.INFINITY
            for gen_board in gen.get_boards():
                new_board = Board()
                new_board.set_circles(gen_board)
                value = max(value, self.alpha_beta(new_board, depth - 1, alpha, beta, "w"))
                alpha = max(alpha, value)
                if beta >= alpha:
                    break  # Beta cut-off
            self.inner_transposition_table[hash_key] = value
            return value
        else:
            value = self.INFINITY
            for gen_board in gen.get_boards():
                new_board = Board()
                new_board.set_circles(gen_board)
                value = min(value, self.alpha_beta(new_board, depth - 1, alpha, beta, "b"))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cut-off
            self.inner_transposition_table[hash_key] = value
            return value

    def state_ordering(self, boards):
        ordered_boards = []
        for board in boards:
            new_board = Board()
            new_board.set_circles(board)
            evaluation = self.transposition_table.get(new_board.hash_board(), 0)
            ordered_boards.append((new_board, evaluation))

        ordered_boards.sort(key=lambda x: x[1], reverse=self.color == 'b')  # Higher evaluations first for Black

        ordered_boards = [board for board, _ in ordered_boards]
        return ordered_boards

    # def get_first_random_move(self, board, start_time):
    #     player_color = self.color == 'b'
    #     positions, moves = self.get_positions(board, player_color)
    #     make_move = random.choice(moves)
    #     time_for_this_move = (time.time_ns() - start_time) / 1_000_000
    #     return (make_move, time_for_this_move)

    @staticmethod
    def get_random_move(board, color):
        gen = StateSpaceGen()
        gen.generate_state_space(board, color)

        return random.choice(gen.get_boards())

