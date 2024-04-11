import math
import time
from abc import ABC, abstractmethod
from functools import reduce
# from multiprocessing import Queue
# from multiprocess import Process, Queue
from queue import Empty, Queue
import random
from board import Board
from clock import Clock
from IO_handler import IOHandler
from state_space_gen import StateSpaceGen
from threading import Thread
from IO_handler import IOHandler

SEARCH_DEPTH = 20
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

hash_map_for_positions = {
    ('I', 5): {'b': 496, 'w': 269},
    ('I', 6): {'b': 89, 'w': 762},
    ('I', 7): {'b': 313, 'w': 805},
    ('I', 8): {'b': 545, 'w': 452},
    ('I', 9): {'b': 683, 'w': 786},
    ('H', 4): {'b': 269, 'w': 89},
    ('H', 5): {'b': 762, 'w': 496},
    ('H', 6): {'b': 805, 'w': 313},
    ('H', 7): {'b': 452, 'w': 545},
    ('H', 8): {'b': 786, 'w': 683},
    ('H', 9): {'b': 564, 'w': 534},
    ('G', 3): {'b': 431, 'w': 412},
    ('G', 4): {'b': 598, 'w': 613},
    ('G', 5): {'b': 987, 'w': 872},
    ('G', 6): {'b': 315, 'w': 163},
    ('G', 7): {'b': 894, 'w': 230},
    ('G', 8): {'b': 862, 'w': 893},
    ('G', 9): {'b': 109, 'w': 712},
    ('F', 2): {'b': 963, 'w': 915},
    ('F', 3): {'b': 104, 'w': 740},
    ('F', 4): {'b': 792, 'w': 292},
    ('F', 5): {'b': 268, 'w': 772},
    ('F', 6): {'b': 453, 'w': 56},
    ('F', 7): {'b': 466, 'w': 761},
    ('F', 8): {'b': 856, 'w': 73},
    ('F', 9): {'b': 891, 'w': 358},
    ('E', 1): {'b': 783, 'w': 51},
    ('E', 2): {'b': 916, 'w': 744},
    ('E', 3): {'b': 886, 'w': 923},
    ('E', 4): {'b': 497, 'w': 937},
    ('E', 5): {'b': 853, 'w': 988},
    ('E', 6): {'b': 881, 'w': 102},
    ('E', 7): {'b': 75, 'w': 485},
    ('E', 8): {'b': 332, 'w': 57},
    ('E', 9): {'b': 699, 'w': 204},
    ('D', 1): {'b': 302, 'w': 835},
    ('D', 2): {'b': 977, 'w': 485},
    ('D', 3): {'b': 815, 'w': 876},
    ('D', 4): {'b': 511, 'w': 328},
    ('D', 5): {'b': 749, 'w': 999},
    ('D', 6): {'b': 155, 'w': 127},
    ('D', 7): {'b': 863, 'w': 650},
    ('D', 8): {'b': 230, 'w': 103},
    ('C', 1): {'b': 523, 'w': 327},
    ('C', 2): {'b': 209, 'w': 812},
    ('C', 3): {'b': 890, 'w': 250},
    ('C', 4): {'b': 939, 'w': 873},
    ('C', 5): {'b': 579, 'w': 233},
    ('C', 6): {'b': 840, 'w': 405},
    ('C', 7): {'b': 557, 'w': 326},
    ('B', 1): {'b': 587, 'w': 914},
    ('B', 2): {'b': 127, 'w': 262},
    ('B', 3): {'b': 74, 'w': 408},
    ('B', 4): {'b': 814, 'w': 180},
    ('B', 5): {'b': 705, 'w': 120},
    ('B', 6): {'b': 746, 'w': 569},
    ('A', 1): {'b': 951, 'w': 316},
    ('A', 2): {'b': 123, 'w': 444},
    ('A', 3): {'b': 549, 'w': 820},
    ('A', 4): {'b': 266, 'w': 132},
    ('A', 5): {'b': 127, 'w': 931}
}


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


def get_hash(position: Board):
    output = 1
    circles = position.get_circles()
    circles = {key: value for key, value in circles.items() if value is not None}
    for key, value in circles.items():
        hash_value = hash_map_for_positions[(chr(int(key[0]) + 64), key[1])][value]
        output = output ^ hash_value
    return output


class AIPlayer(Player):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.in_search = False
        self.space_gen = StateSpaceGen()
        self.best_move = None
        self.queue = Queue()
        self.ai_search_process = None
        self.trans_table = None

    def update_score(self, score):
        super().update_score(score)

    def make_move(self, board, **kwargs):
        print(self.color, "being asked to make a move")

        def search_and_apply_move(queue, board):
            time_start = time.time_ns()
            best_move = self._calculate_move(board, queue=self.queue, start_time=time_start)
            return best_move

        # Start the process
        best_move = self.ai_search_process = Thread(target=search_and_apply_move, args=(self.queue, board))
        self.ai_search_process.start()
        print("Thread started")
        # self.ai_search_process.join()
        print("Thread done")


    @abstractmethod
    def _calculate_move(self, board, queue, start_time, **kwargs):
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


class MangatAI(AIPlayer):

    def minimax(self, position: Board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game_over(position):
            return self.evaluate_position(position, maximizing_player)

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

    def get_first_random_move(self, board, start_time):
        player_color = self.color == 'b'
        positions, moves = self.get_positions(board, player_color)
        make_move = random.choice(moves)
        time_for_this_move = (time.time_ns() - start_time) / 1_000_000
        return (make_move, time_for_this_move)

    def _calculate_move(self, board, queue, start_time, **kwargs):
        self.trans_table = IOHandler.read_transposition_table_from_file("mangat_table.json")
        if self.trans_table is None:
            self.trans_table = {}
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
                hash = get_hash(new_board)
                if self.trans_table.get(hash):
                    eval = self.trans_table.get(hash)
                else:
                    eval = self.minimax(new_board, SEARCH_DEPTH, math.inf, -math.inf, player_color)
                    self.trans_table[hash] = eval
                if eval > max_eval:
                    max_eval = eval
                    make_move = moves[i]
                    time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                    queue.put((make_move, time_for_this_move))
            IOHandler.save_transposition_table(self.trans_table, "mangat_table.json")
            print("done searching")
            return make_move
        else:
            positions, moves = self.get_positions(board, player_color)
            for i, position in enumerate(positions):
                new_board = Board()
                new_board.set_circles(position)
                hash = get_hash(new_board)
                if self.trans_table.get(hash):
                    eval = self.trans_table.get(hash)
                else:
                    eval = self.minimax(new_board, SEARCH_DEPTH, math.inf, -math.inf, player_color)
                    self.trans_table[hash] = eval
                if eval < min_eval:
                    min_eval = eval
                    make_move = moves[i]
                    time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                    print("found move", make_move, time_for_this_move)
                    queue.put((make_move, time_for_this_move))
            IOHandler.save_transposition_table(self.trans_table, "mangat_table.json")
            print("done searching")
            return make_move

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
        self.depth = 4

    def _calculate_move(self, board, queue, start_time, **kwargs):
        return self.get_best_move(board, start_time, queue)

    def get_color(self):
        return self.color

    def load_transposition_table(self):
        transposition_table_data = IOHandler.read_transposition_table_from_file(self.color)
        if transposition_table_data is not None:
            self.transposition_table = transposition_table_data

    def get_best_move(self, board, start_time, queue):
        self.load_transposition_table()
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

        IOHandler.save_transposition_table(self.transposition_table, self.color)

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
                black_score += self.POINT_VALUES[index] * self.weights["b_pos"] * \
                (self.weights["empower_self"] if self.color == "w" else 1)
            elif board.get_marble(coord) == "w":
                white_score += self.POINT_VALUES[index] * self.weights["w_pos"] * \
                (self.weights["empower_self"] if self.color == "b" else 1)

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
        weights["b_off"] = -50
        weights["w_off"] = 50
        weights["b_pos"] = 4
        weights["w_pos"] = -4
        weights["b_coherence"] = 1
        weights["w_coherence"] = -1
        weights["empower_self"] = 2
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

    def get_first_random_move(self, board, start_time):
        player_color = self.color == 'b'
        positions, moves = self.get_positions(board, player_color)
        make_move = random.choice(moves)
        time_for_this_move = (time.time_ns() - start_time) / 1_000_000
        return (make_move, time_for_this_move)


class AIAgent2(AIPlayer):
    """
    AI agent for testing purposes.
    """
    POINT_VALUES = [
        -2, -1, -1, -1, -2,
        -1, 0, 0, 0, 0, -1,
        -1, 0, 1, 1, 1, 0, -1,
        -1, 0, 1, 3, 3, 1, 0, -1,
        -2, 0, 1, 3, 5, 3, 1, 0, -2,
        -1, 0, 1, 3, 3, 1, 0, -1,
        -1, 0, 1, 1, 1, 0, -1,
        -1, 0, 0, 0, 0, -1,
        -2, -1, -1, -1, -2
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
        print(f"time for {count}", time_end - time_start)
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
        print(f"time for {count}", time_end - time_start)
        count += 1
    end_of_pattern = time.time()
    print("third pattern: ", end_of_pattern - time_start_of_pattern)
