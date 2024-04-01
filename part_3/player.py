import math
import time
from abc import ABC, abstractmethod
from functools import reduce
# from multiprocessing import Queue
from multiprocess import Process, Queue
from queue import Empty
import random
from board import Board
from clock import Clock
from state_space_gen import StateSpaceGen
from threading import Thread
from IO_handler import IOHandler

SEARCH_DEPTH = 20


class Player(ABC):
    def __init__(self, name, color):
        self.color = color
        self.score = None
        self.time = None
        self.current_position = None
        self.marbles_removed = None
        self.turn_number = None
        self.list_of_moves = []
        self.current_move_time = 0
        self.name = name
        self.time_per_move = 0
        self.clock = Clock()

    @abstractmethod
    def make_move(self, **kwargs):
        print("making move kajfkajfkjaf")

    def update_score(self, score):
        self.score = score

    def set_time_limit_per_move(self, time_limit_per_move):
        self.time_per_move = time_limit_per_move
        self.clock.set_clock_time_values(time_limit_per_move)

    def get_aggregate_time(self):
        """
        Gets the aggregate time of the move for the player
        :return: is the aggregate time as an Int
        """
        if len(self.list_of_moves) == 0:
            return 0
        return reduce(lambda x, y: x + y, self.list_of_moves)

    def tick_player_clock(self):
        self.clock.decrement_timer()

    def reset_player_clock(self, undo=False):
        if not undo:
            current_move_time = self.time_per_move - self.clock.current_time
            self.list_of_moves.append(current_move_time)
        self.clock.reset_to_full()

    def reset_player(self):
        self.list_of_moves = []
        self.clock.reset_to_full()

    def get_last_move_time(self):
        if len(self.list_of_moves) == 0:
            return 0
        return self.list_of_moves[len(self.list_of_moves) - 1]

    def undo_move(self):
        if len(self.list_of_moves) != 0:
            self.list_of_moves.pop()
        self.clock.reset_to_full()

    def get_name(self):
        return self.name

    def __str__(self):
        output = ""
        for time in self.list_of_moves:
            output += f"{time} "
        return f"{self.name}  {output}"


class AIPlayer(Player):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.in_search = False
        self.space_gen = StateSpaceGen()
        self.best_move = None
        self.queue = Queue()
        self.ai_search_process = None

    def update_score(self, score):
        super().update_score(score)

    def make_move(self, board, **kwargs):
        print(self.color, "being asked to make a move")

        def search_and_apply_move(queue, board):
            time_start = time.time_ns()
            best_move = self._calculate_move(board, queue=self.queue, start_time=time_start)

        # Start the process
        self.ai_search_process = Process(target=search_and_apply_move, args=(self.queue, board))
        self.ai_search_process.start()

    def get_first_random_move(self, board, start_time):
        player_color = self.color == 'b'
        positions, moves = self.get_positions(board, player_color)
        make_move = random.choice(moves)
        time_for_this_move = (time.time_ns() - start_time) / 1_000_000
        return (make_move, time_for_this_move)

    def _calculate_move(self, board, queue, start_time, **kwargs):
        player_color = self.color == 'b'
        max_eval = -math.inf
        min_eval = math.inf
        make_move = None
        print("inside searching")
        self.space_gen.boards = []
        if player_color:
            positions, moves = self.get_positions(board, player_color)
            for i, position in enumerate(positions):
                new_board = Board()
                new_board.set_circles(position)
                eval = self.minimax(new_board, SEARCH_DEPTH, math.inf, -math.inf, player_color)
                if eval > max_eval:
                    max_eval = eval
                    make_move = moves[i]
                    time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                    queue.put((make_move, time_for_this_move))

            print("done searching")
            return make_move
        else:
            positions, moves = self.get_positions(board, player_color)
            for i, position in enumerate(positions):
                new_board = Board()
                new_board.set_circles(position)
                eval = self.minimax(new_board, SEARCH_DEPTH, math.inf, -math.inf, player_color)
                if eval < min_eval:
                    min_eval = eval
                    make_move = moves[i]
                    time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                    print("found move", make_move, time_for_this_move)
                    queue.put((make_move, time_for_this_move))
            print("done searching")
            return make_move

    @abstractmethod
    def evaluate_position(self, position, maximizing_player):
        pass

    def add_ai_time(self, time_of_ai_move):
        self.list_of_moves.append(time_of_ai_move)

    def reset_player_clock(self, undo=False):
        self.clock.reset_to_full()

    def empty_queue(self):
        try:
            while True:  # Continue until the queue is empty
                item = self.queue.get_nowait()  # Attempt to get an item without blocking
        except Exception as e:
            print("queue is empty")

    def get_last_item_and_empty(self):
        last_item = None
        try:
            while True:  # Keep dequeuing until the queue is empty
                last_item = self.queue.get_nowait()
        except Empty:
            pass  # The queue is empty
        return last_item

    def minimax(self, position: Board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game_over(position):
            score = self.evaluate_position(position, maximizing_player)
            # print_abalone_board(position.circles)
            return score

        if maximizing_player:
            max_eval = -math.inf
            positions, moves = self.get_positions(position, not maximizing_player)
            for i, child_position in enumerate(positions):
                new_board = Board()
                new_board.set_circles(child_position)
                position_evaluated = self.minimax(new_board, depth - 1, alpha, beta,
                                                  not maximizing_player)
                if position_evaluated > max_eval:
                    max_eval = position_evaluated

                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            positions, moves = self.get_positions(position, not maximizing_player)
            for i, child_position in enumerate(positions):
                new_board = Board()
                new_board.set_circles(child_position)
                position_evaluated = self.minimax(new_board, depth - 1, alpha, beta,
                                                  not maximizing_player)
                if position_evaluated < min_eval:
                    min_eval = position_evaluated

                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval

    def apply_move(self, best_move):
        self.best_move = best_move

    def game_over(self, position):
        pass

    def get_positions(self, position, maximizing_player):
        player_color = 'b' if maximizing_player else 'w'
        self.space_gen.boards = []
        self.space_gen.moves = []
        self.space_gen.generate_state_space(position, player_color)
        return self.space_gen.boards, self.space_gen.moves


class HumanPlayer(Player):
    def update_score(self, score):
        super().update_score(score)

    def make_move(self, board, **kwargs):
        print(self.color, "being asked to make a move")


FIRST_CIRCLE = 0.5
SECOND_CIRCLE = 1
THIRD_CIRCLE = 3
FOURTH_CIRCLE = 5
FIFTH_CIRCLE = 10

board_scores = {('I', 5): FIRST_CIRCLE,
                ('I', 6): FIRST_CIRCLE,
                ('I', 7): FIRST_CIRCLE,
                ('I', 8): FIRST_CIRCLE,
                ('I', 9): FIRST_CIRCLE,
                ('H', 4): FIRST_CIRCLE,
                ('H', 5): SECOND_CIRCLE,
                ('H', 6): SECOND_CIRCLE,
                ('H', 7): SECOND_CIRCLE,
                ('H', 8): SECOND_CIRCLE,
                ('H', 9): FIRST_CIRCLE,
                ('G', 3): FIRST_CIRCLE,
                ('G', 4): SECOND_CIRCLE,
                ('G', 5): THIRD_CIRCLE,
                ('G', 6): THIRD_CIRCLE,
                ('G', 7): THIRD_CIRCLE,
                ('G', 8): SECOND_CIRCLE,
                ('G', 9): FIRST_CIRCLE,
                ('F', 2): FIRST_CIRCLE,
                ('F', 3): SECOND_CIRCLE,
                ('F', 4): THIRD_CIRCLE,
                ('F', 5): FOURTH_CIRCLE,
                ('F', 6): FOURTH_CIRCLE,
                ('F', 7): THIRD_CIRCLE,
                ('F', 8): SECOND_CIRCLE,
                ('F', 9): FIRST_CIRCLE,
                ('E', 1): FIRST_CIRCLE,
                ('E', 2): SECOND_CIRCLE,
                ('E', 3): THIRD_CIRCLE,
                ('E', 4): FOURTH_CIRCLE,
                ('E', 5): FIFTH_CIRCLE,
                ('E', 6): FOURTH_CIRCLE,
                ('E', 7): THIRD_CIRCLE,
                ('E', 8): SECOND_CIRCLE,
                ('E', 9): FIRST_CIRCLE,
                ('D', 1): FIRST_CIRCLE,
                ('D', 2): SECOND_CIRCLE,
                ('D', 3): THIRD_CIRCLE,
                ('D', 4): FOURTH_CIRCLE,
                ('D', 5): FOURTH_CIRCLE,
                ('D', 6): THIRD_CIRCLE,
                ('D', 7): SECOND_CIRCLE,
                ('D', 8): FIRST_CIRCLE,
                ('C', 1): FIRST_CIRCLE,
                ('C', 2): SECOND_CIRCLE,
                ('C', 3): THIRD_CIRCLE,
                ('C', 4): THIRD_CIRCLE,
                ('C', 5): THIRD_CIRCLE,
                ('C', 6): SECOND_CIRCLE,
                ('C', 7): FIRST_CIRCLE,
                ('B', 1): FIRST_CIRCLE,
                ('B', 2): SECOND_CIRCLE,
                ('B', 3): SECOND_CIRCLE,
                ('B', 4): SECOND_CIRCLE,
                ('B', 5): SECOND_CIRCLE,
                ('B', 6): FIRST_CIRCLE,
                ('A', 1): FIRST_CIRCLE,
                ('A', 2): FIRST_CIRCLE,
                ('A', 3): FIRST_CIRCLE,
                ('A', 4): FIRST_CIRCLE,
                ('A', 5): FIRST_CIRCLE
                }

center_positions = [('E', 5), ('E', 6), ('F', 5), ('F', 6)]


class MangatAI(AIPlayer):

    def count_marbles_in_position(self, position, maximizing_player):
        black_count = len(position.get_marbles_by_color('b'))
        white_count = len(position.get_marbles_by_color('w'))
        if maximizing_player:
            return black_count - white_count
        else:
            return white_count - black_count

    def _calculate_zone(self, circle):
        # Basic manhattan distance approximation for zones on a hex grid
        # Outermost Circle
        return board_scores[(chr(circle[0] + 64), circle[1])]

    def count_board_score(self, position: Board, maximizing_player):

        marbles = position.get_marbles_by_color(self.color)
        board_score = 0
        for marble in marbles:
            board_score += self._calculate_zone(marble)
        if maximizing_player:
            return board_score
        else:
            return -board_score

    def count_marble_islands(self, position, maximizing_player):
        return 1

    def evaluate_position(self, position, maximizing_player):
        """
        1. How many marbles (count the opposite number of marbles)
        2. How close to center (count all the marbles scores based upon where they are)
        3. How many islands (count the number of islands)
        1 * 2 * 3
        """
        marbles_remaining = self.count_marbles_in_position(position, maximizing_player)
        board_score = self.count_board_score(position, maximizing_player)
        marble_islands = self.count_marble_islands(position, maximizing_player)
        return (board_score * marble_islands) + (marbles_remaining * 15)


class AIAgent(AIPlayer):
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

    def __init__(self, name, color):
        super().__init__(name, color)
        self.weights = self.get_weights()
        self.transposition_table = {}
        self.inner_transposition_table = {}
        self.depth = 6

    def _calculate_move(self, board, queue, start_time, **kwargs):
        return self.get_best_move(board, start_time, queue)

    def get_color(self):
        return self.color

    def load_transposition_table(self):
        transposition_table_data = IOHandler.read_transposition_table_from_file()
        if transposition_table_data is not None:
            self.transposition_table = transposition_table_data

    def get_best_move(self, board, start_time, queue):
        self.load_transposition_table()
        print(f"TP length: {len(self.transposition_table)}")
        best_move = None
        best_board = None
        best_score = -self.INFINITY if self.color == 'b' else self.INFINITY
        gen = StateSpaceGen()
        gen.generate_state_space(board, self.color)

        alpha = -self.INFINITY
        beta = self.INFINITY

        ordered_boards = self.state_ordering(gen.get_boards())

        for gen_board in ordered_boards:
            # newboard = Board()
            # newboard.set_circles(gen_board)
            # score = self.board_evaluation(newboard)

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
                time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                queue.put((best_move, time_for_this_move))
                best_board = gen_board

            # Update alpha or beta for pruning
            if self.color == 'b':
                alpha = max(alpha, best_score)
            else:
                beta = min(beta, best_score)

            # Perform pruning
            if beta <= alpha:
                break

        IOHandler.save_transposition_table(self.transposition_table)

        print(f"Best move: {best_move}")
        return best_move

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

        # print(f"black score {black_score}")
        # print(f"white score {white_score}")

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

        while stack:
            current_marble = stack.pop()
            if current_marble not in visited:
                visited.add(current_marble)
                group_size += 1
                neighbors = board.get_neighbors_only(current_marble)
                for neighbor in neighbors:
                    if board.get_marble(neighbor) == player:
                        stack.append(neighbor)
        return group_size

    @staticmethod
    def get_weights():
        """
        Using an adapted AI_abalone weight system
        """
        weights = {}
        weights["b_off"] = -15
        weights["w_off"] = 15
        weights["b_pos"] = 3
        weights["w_pos"] = -3
        weights["b_coherence"] = 10
        weights["w_coherence"] = -10
        # weights["b_mobility"] = 2
        # weights["w_mobility"] = -2
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


class AIAgent2(AIPlayer):
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

    def __init__(self, name, color):
        super().__init__(name, color)
        self.weights = self.get_weights()
        self.transposition_table = {}
        self.inner_transposition_table = {}
        self.depth = 6

    def _calculate_move(self, board, **kwargs):
        return self.get_best_move(board)

    def get_color(self):
        return self.color

    def load_transposition_table(self):
        transposition_table_data = IOHandler.read_transposition_table_from_file()
        if transposition_table_data is not None:
            self.transposition_table = transposition_table_data

    def get_best_move(self, board):
        self.load_transposition_table()
        print(f"TP length: {len(self.transposition_table)}")
        best_move = None
        best_board = None
        best_score = -self.INFINITY if self.color == 'b' else self.INFINITY
        gen = StateSpaceGen()
        gen.generate_state_space(board, self.color)

        alpha = -self.INFINITY
        beta = self.INFINITY

        ordered_boards = self.state_ordering(gen.get_boards())

        for gen_board in ordered_boards:
            # newboard = Board()
            # newboard.set_circles(gen_board)
            # score = self.board_evaluation(newboard)

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

        IOHandler.save_transposition_table(self.transposition_table)

        print(f"Best move: {best_move}")
        return best_board

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

        # print(f"black score {black_score}")
        # print(f"white score {white_score}")

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

        while stack:
            current_marble = stack.pop()
            if current_marble not in visited:
                visited.add(current_marble)
                group_size += 1
                neighbors = board.get_neighbors_only(current_marble)
                for neighbor in neighbors:
                    if board.get_marble(neighbor) == player:
                        stack.append(neighbor)
        return group_size

    @staticmethod
    def get_weights():
        """
        Using an adapted AI_abalone weight system
        """
        weights = {}
        weights["b_off"] = -15
        weights["w_off"] = 15
        weights["b_pos"] = 3
        weights["w_pos"] = -3
        weights["b_coherence"] = 10
        weights["w_coherence"] = -10
        # weights["b_mobility"] = 2
        # weights["w_mobility"] = -2
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


if __name__ == '__main__':
    black = AIAgent2("black", "b")
    white = AIAgent2("black", "w")
    # b.setup_board(setup_type="Belgian Daisy")
    count = 3
    time_start_of_pattern = time.time()
    while count <= 40:
        b = Board()
        b.setup_board()
        time_start = time.time()
        for _ in range(count):
            black_move = black._calculate_move(b)
            white_move = white._calculate_move(black_move)
            b = white_move
        time_end = time.time()
        print(f"time for {count}", time_end - time_start)
        count += 1
    end_of_pattern = time.time()
    print("first pattern: ", end_of_pattern - time_start_of_pattern)
    time_start_of_pattern = time.time()
    count = 3
    while count <= 40:
        b = Board()
        b.setup_board(setup_type="Belgian Daisy")
        time_start = time.time()
        for _ in range(count):
            black_move = black._calculate_move(b)
            white_move = white._calculate_move(black_move)
            b = white_move
        time_end = time.time()
        print(f"time for {count}",time_end - time_start)
        count += 1
    end_of_pattern = time.time()
    print("second pattern: ", end_of_pattern - time_start_of_pattern)
    time_start_of_pattern = time.time()
    count = 3
    while count <= 40:
        b = Board()
        b.setup_board(setup_type="German Daisy")
        time_start = time.time()
        for _ in range(count):
            black_move = black._calculate_move(b)
            white_move = white._calculate_move(black_move)
            b = white_move
        time_end = time.time()
        print(f"time for {count}",time_end - time_start)
        count += 1
    end_of_pattern = time.time()
    print("third pattern: ", end_of_pattern - time_start_of_pattern)
