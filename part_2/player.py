from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self):
        self.color = None
        self.score = None
        self.time = None
        self.current_position = None
        self.marbles_removed = None
        self.turn_number = None

    @abstractmethod
    def make_move(self, **kwargs):
        pass

    @abstractmethod
    def update_score(self, **kwargs):
        pass


class AIPlayer(Player):

    def update_score(self, **kwargs):
        pass

    def make_move(self, **kwargs):
        pass

    def _calculate_move(self, **kwargs):
        pass


class HumanPlayer(Player):
    def update_score(self, **kwargs):
        pass

    def make_move(self, **kwargs):
        pass
