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


class TestAI(AIPlayer):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.move_already_picked = set()

    def _calculate_move(self, board, start_time, **kwargs):

        player_color = self.color == 'b'
        max_eval = -math.inf
        min_eval = math.inf
        make_move = None
        self.space_gen.boards = []
        if player_color:
            positions, moves = self.get_positions(board, player_color)
            for i, position in enumerate(positions):
                eval = self.minimax(position, SEARCH_DEPTH, math.inf, -math.inf, player_color)
                if eval > max_eval:
                    if len(self.move_already_picked) < 8:
                        max_eval = eval
                        make_move = position
                        self.move_already_picked.add(str(position))
                        time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                    else:
                        if str(position) not in self.move_already_picked:
                            max_eval = eval
                            make_move = position
                            self.move_already_picked.add(str(position))
                    # queue.put((make_move, time_for_this_move))

            return make_move
        else:
            positions, moves = self.get_positions(board, player_color)
            for i, position in enumerate(positions):
                eval = self.minimax(position, SEARCH_DEPTH, math.inf, -math.inf, player_color)
                if eval < min_eval:
                    if len(self.move_already_picked) < 8:
                        max_eval = eval
                        make_move = position
                        self.move_already_picked.add(str(position))
                        time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                    else:
                        if str(position) not in self.move_already_picked:
                            max_eval = eval
                            make_move = position
                            self.move_already_picked.pop()
                            self.move_already_picked.add(str(position))
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
    console_writing()
