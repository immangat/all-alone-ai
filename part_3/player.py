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
from part_3.IO_handler import IOHandler
from state_space_gen import StateSpaceGen
from threading import Thread

SEARCH_DEPTH = 10


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


class TestAI(AIPlayer):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.move_already_picked = set()

    def _calculate_move(self, board, start_time, **kwargs):
        self.trans_table = IOHandler.read_transposition_table_from_file("mangat_table.json")
        if self.trans_table is None:
            self.trans_table = {}
        player_color = self.color == 'b'
        max_eval = -math.inf
        min_eval = math.inf
        make_move = None
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
                    if len(self.move_already_picked) < 8:
                        max_eval = eval
                        make_move = new_board
                        self.move_already_picked.add(str(position))
                        time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                    else:
                        if str(position) not in self.move_already_picked:
                            max_eval = eval
                            make_move = new_board
                            self.move_already_picked.add(str(position))
                    # queue.put((make_move, time_for_this_move))
            IOHandler.save_transposition_table(self.trans_table, "mangat_table.json")
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
                    if len(self.move_already_picked) < 8:
                        min_eval = eval
                        make_move = new_board
                        self.move_already_picked.add(str(position))
                        time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                    else:
                        if str(position) not in self.move_already_picked:
                            min_eval = eval
                            make_move = new_board
                            self.move_already_picked.pop()
                            self.move_already_picked.add(str(position))
            IOHandler.save_transposition_table(self.trans_table, "mangat_table.json")
            return make_move


class MangatAITest(TestAI):
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


def file_writing():
    def playing_game():
        whitePlayer = MangatAITest("white", "w")
        blackPlayer = MangatAITest("black", "b")
        b = Board()
        b.setup_board("Belgian Daisy")

        # Use a more precise filename based on the start time
        time_start = time.time()
        filename = f"D:\\OneDrive - BCIT\\BCIT\\Term 3\\COMP 3981\\project\\mangat_state_space\\inputs\\{time_start}.txt"

        with open(filename, 'w') as file:
            for _ in range(35):
                black_move = blackPlayer._calculate_move(b, time.time_ns())
                file.write(str(black_move) + "\n")  # Use str() for conversion and add newline for readability
                white_move = whitePlayer._calculate_move(black_move, time.time_ns())
                file.write(str(white_move) + "\n")
                b = white_move
        time_end = time.time()
        print(time_end - time_start)

    threads = []
    for _ in range(10):
        new_thread = Thread(target=playing_game)
        threads.append(new_thread)
        new_thread.start()
    for thread in threads:
        thread.join()


def console_writing():
    time_start = time.time()
    whitePlayer = MangatAITest("white", "w")
    blackPlayer = MangatAITest("black", "b")
    b = Board()
    b.setup_board("Belgian Daisy")
    for _ in range(35):
        black_move = blackPlayer._calculate_move(b, time.time_ns())
        print(black_move)  # Use str() for conversion and add newline for readability
        white_move = whitePlayer._calculate_move(black_move, time.time_ns())
        print(white_move)
        b = white_move

    time_end = time.time()
    print(time_end - time_start)


if __name__ == '__main__':
    # b = Board()
    # b.setup_board("Belgian Daisy")
    # get_hash(b)
    console_writing()
