from part_3.board import Board
from part_3.player import AIPlayer
from multiprocess import Process, Queue
from queue import Empty


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
