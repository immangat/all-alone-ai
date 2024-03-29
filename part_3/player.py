import math
import random
import time
from abc import ABC, abstractmethod
from functools import reduce

from clock import Clock
from board import Board
from state_space_gen import StateSpaceGen


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
        self.clock = Clock()

    @abstractmethod
    def make_move(self, **kwargs):
        self.clock.can_tick = True
        pass
        self.clock.can_tick = False

    def update_score(self, score):
        self.score = score

    def get_aggregate_time(self):
        """
        Gets the aggregate time of the move for the player
        :return: is the aggregate time as an Int
        """
        if len(self.list_of_moves) == 0:
            return 0
        return reduce(lambda x, y: x + y, self.list_of_moves)

    def tick_player_clock(self):
        self.clock.tick_timer()

    def reset_player_clock(self):
        current_move_time = self.clock.current_time
        self.list_of_moves.append(current_move_time)
        print(self)
        self.clock.reset_timer()

    def __str__(self):
        output = ""
        for time in self.list_of_moves:
            output += f"{time} "
        return f"{self.name}  {output}"


class AIPlayer(Player):

    def update_score(self, score):
        super().update_score(score)

    @abstractmethod
    def make_move(self, **kwargs):
        pass

    @abstractmethod
    def _calculate_move(self, **kwargs):
        pass


class HumanPlayer(Player):
    def update_score(self, score):
        super().update_score(score)

    def make_move(self, **kwargs):
        pass


class MangatAI(AIPlayer):

    def __init__(self, name, color):
        super().__init__(name, color)
        self.space_gen = StateSpaceGen()

    def make_move(self, **kwargs):
        pass

    def _calculate_move(self, **kwargs):
        pass

    def game_over(self, position):
        pass

    def count_marbles_in_position(self, position, maximizing_player):
        player_color = 'b' if not maximizing_player else 'w'
        if maximizing_player:
            return len(position.get_marbles_by_color(player_color))
        else:
            return -len(position.get_marbles_by_color(player_color))

    def count_board_score(self, position, maximizing_player):
        return 0

    def count_marble_islands(self, position, maximizing_player):
        return 0

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
        return board_score * marble_islands - marbles_remaining

    def get_positions(self, position, maximizing_player):
        player_color = 'b' if maximizing_player else 'w'
        self.space_gen.boards = []
        self.space_gen.generate_state_space(position, player_color)
        return self.space_gen.boards

    def minimax(self, position, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game_over(position):
            return self.evaluate_position(position, maximizing_player)

        if maximizing_player:
            max_eval = -math.inf
            for child_position in self.get_positions(position, not maximizing_player):
                position_evaluated = self.minimax(child_position, depth - 1, alpha, beta, not maximizing_player)
                max_eval = max(position_evaluated, max_eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for child_position in self.get_positions(position, not maximizing_player):
                position_evaluated = self.minimax(child_position, depth - 1, alpha, beta, not maximizing_player)
                min_eval = min(position_evaluated, min_eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval


player = MangatAI("mangat", "black")
b = Board.create_custom_board(
    "A1b,A2b,B3b,B4b,B5b,C3b,C4b,C5b,D3b,D4b,D5b,E3b,E4b,E5b,B1w,B2w,C1w,C2w,D1w,D2w,E1w,E2w,F3w,F4w,F5w,G3w,G4w,G5w".split(
        ",")
)
time_start = time.time()
print(player.minimax(b, 4, -math.inf, math.inf, False))
time_end = time.time()
print(time_end - time_start)
