from abc import ABC, abstractmethod
from functools import reduce

from clock import Clock


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
    def make_move(self, **kwargs):
        pass

    def _calculate_move(self, **kwargs):
        pass


def game_over(position):
    pass


def minimax(position, depth, maximizing_player):
    if depth == 0 or game_over(position):
        return 1
