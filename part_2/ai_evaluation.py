import time

from state_space_gen import StateSpaceGen

class move_evaluation:

    EDGE_COORD = [

        (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
        (2, 1), (2, 6),
        (3, 1), (3, 7),
        (4, 1), (4, 8),
        (5, 1), (5, 9),
        (6, 2), (6, 9),
        (7, 3), (7, 9),
        (8, 4), (8, 9),
        (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)

    ]

    CENTER_COORD = [
        (4, 4), (4, 5), (4, 6), (5, 4), (5, 5), (5, 6), (6, 4), (6, 5), (6, 6)
    ]

    def __init__(self, manager):
        self.manager = manager
        self.gen = StateSpaceGen()
        self.player_color = manager.current_player.color
        print(f"player color: {self.player_color}")
        self.opponent_color = "w" if self.player_color == "b" else "b"
        self.best_board = None

    # def choose_best_move(self):
    #     best_score = -float('inf')  # Initialize with the lowest possible score
    #     best_move = None
    #     best_board = None
    #
    #     # Loop through all possible moves and their resulting boards
    #     for move, resulting_board in zip(self.manager.gen.moves, self.manager.gen.boards):
    #         # Evaluate the board state resulting from making the current move
    #
    #         score = self.nico_heuristic(resulting_board, self.player_color)
    #
    #         # If the current move's score is better than the best found so far, update best_move and best_score
    #         if score > best_score:
    #             best_score = score
    #             best_move = move
    #             best_board = resulting_board
    #
    #     # Optionally, print or log the best move and its score for debugging
    #     print(f"Best move: {best_move}, Score: {best_score}")
    #
    #     return best_move, best_board, best_score

    def choose_best_move(self, time_limit=20):
        start_time = time.time()
        depth = 1
        best_move = None
        best_score = -float('inf')
        best_board = None

        if self.manager.current_player.color != self.player_color:
            self.switch_players()

        # Continue deepening until the time limit is reached.
        while True:
            score, move, board = self.minimax(self.manager.board, depth, -float('inf'), float('inf'), True, start_time, time_limit)
            if move is None:  # Time's up, no move found
                break
            if score > best_score:
                best_score, best_move, best_board = score, move, board
            depth += 1
            if time.time() - start_time >= time_limit:
                break

        print(f"Best move at depth {depth-1}: {best_move}, score: {best_score}")
        return best_move, best_board

    def minimax(self, board, depth, alpha, beta, maximizingPlayer, start_time, time_limit):
        # Time check to stop the search
        if time.time() - start_time > time_limit:
            return -float('inf') if maximizingPlayer else float('inf'), None, None

        original_player_color = self.player_color
        original_opponent_color = self.opponent_color

        # Switch context for minimizing player
        if not maximizingPlayer:
            self.player_color, self.opponent_color = self.opponent_color, self.player_color

        self.gen = StateSpaceGen()
        self.gen.generate_state_space(board, self.player_color)

        if depth == 0:
            score = self.nico_heuristic(board, self.player_color)
            self.player_color, self.opponent_color = original_player_color, original_opponent_color
            return score, None, board

        best_move = None
        best_score = -float('inf') if maximizingPlayer else float('inf')

        for move, resulting_board in zip(self.gen.moves, self.gen.boards):
            # Recursive minimax call
            evaluation, _, _ = self.minimax(resulting_board, depth - 1, alpha, beta, not maximizingPlayer, start_time,
                                            time_limit)

            if maximizingPlayer:
                if evaluation > best_score:
                    best_score, best_move = evaluation, move
                alpha = max(alpha, evaluation)
            else:
                if evaluation < best_score:
                    best_score, best_move = evaluation, move
                beta = min(beta, evaluation)

            if beta <= alpha:
                break

        # Restore the original player context
        self.player_color, self.opponent_color = original_player_color, original_opponent_color

        return best_score, best_move, resulting_board if best_move else board

    # def minimax(self, board, depth, alpha, beta, maximizingPlayer):
    #     count = 0
    #     original_player_color = self.player_color
    #     original_opponent_color = self.opponent_color
    #
    #     if maximizingPlayer:
    #         self.player_color = original_player_color
    #         self.opponent_color = original_opponent_color
    #     else:
    #         # Switch context for minimizing player
    #         self.player_color = original_opponent_color
    #         self.opponent_color = original_player_color
    #
    #     self.gen = StateSpaceGen()
    #     print("color: ",self.player_color)
    #     # self.switch_players()
    #     self.gen.generate_state_space(board, self.player_color)
    #     for move, resulting_board in zip(self.gen.moves, self.gen.boards):
    #         count+= 1
    #         print(f"Move: {move}")
    #         print(resulting_board)
    #     print(count)
    #     # if depth == 0 or board.is_game_over():
    #     if depth == 0:
    #         score = self.nico_heuristic(board, self.player_color)
    #         # Restore original player context
    #         self.player_color = original_player_color
    #         self.opponent_color = original_opponent_color
    #         return score, None, board
    #
    #     best_move = None
    #     best_board = None
    #
    #     if maximizingPlayer:
    #         maxEval = -float('inf')
    #         for move, resulting_board in zip(self.gen.moves, self.gen.boards):
    #             evaluation, _, _ = self.minimax(resulting_board, depth - 1, alpha, beta, False)
    #             if evaluation > maxEval:
    #                 maxEval = evaluation
    #                 best_move = move
    #                 best_board = resulting_board
    #             alpha = max(alpha, evaluation)
    #             if beta <= alpha:
    #                 break
    #         return maxEval, best_move, best_board
    #     else:
    #         minEval = float('inf')
    #         for move, resulting_board in zip(self.gen.moves, self.gen.boards):
    #             evaluation, _, _ = self.minimax(resulting_board, depth - 1, alpha, beta, True)
    #             if evaluation < minEval:
    #                 minEval = evaluation
    #                 # best_move = move
    #                 # best_board = resulting_board
    #             beta = min(beta, evaluation)
    #             if beta <= alpha:
    #                 break
    #         return minEval, best_move, best_board

    def nico_heuristic(self, board, player_color):

        score = 0

        num_marbles_taken = self.num_marbles_taken(self.player_color)
        num_marbles_lost = self.num_marbles_taken(self.opponent_color)
        player_marbles = board.get_marbles_by_color(player_color)
        opponent_color = "w" if player_color == "b" else "b"
        opponent_marbles = board.get_marbles_by_color(opponent_color)

        # Safety: Decrease score for marbles close to the edge
        for marble in player_marbles:
            if self.is_marble_near_edge(marble):
                score -= 1

        # Aggression: Increase score for opponent marbles near the edge
        for marble in opponent_marbles:
            if self.is_marble_near_edge(marble):
                score += 1

        # Formation Strength: Bonus for each marble that is part of a larger group
        for marble in player_marbles:
            neighbors, _ = self.gen.get_neighbors(marble)
            group_bonus = sum(1 for neighbor in neighbors if neighbor in player_marbles)
            score += group_bonus

        # Formation Strength: Bonus for each marble that is part of a larger group
        for marble in opponent_marbles:
            neighbors, _ = self.gen.get_neighbors(marble)
            group_bonus = sum(1 for neighbor in neighbors if neighbor in opponent_marbles)
            score -= group_bonus

        # Direct Knockout Bonus
        # print(self.find_knockout_moves())
        knockout_moves = self.find_knockout_moves()[0]
        # Assuming each knockout move is highly valuable, add a significant score for each.
        if num_marbles_taken == 4:
            score += len(knockout_moves) * 10000  # Modify the multiplier as needed to balance gameplay.
        else:
            score += len(knockout_moves) * 10  # Modify the multiplier as needed to balance gameplay.

        # Center Control: Additional points for controlling the center of the board
        center_control_bonus = sum(1 for marble in player_marbles if marble in self.CENTER_COORD)
        score += center_control_bonus * 5  # Weight center control more heavily

        center_control_bonus = sum(1 for marble in opponent_marbles if marble in self.CENTER_COORD)
        score -= center_control_bonus * 5  # Weight center control more heavily

        # Number of marbles taken: Increase score for each marble taken
        score += num_marbles_taken * 10  # Modify the multiplier as needed to balance gameplay.

        # Number of marbles lost: Decrease score for each marble lost
        score -= num_marbles_lost * 10

        return score

    def find_knockout_moves(self):
        knockout_moves_player = []
        knockout_boards = []
        player_marbles_remaining = self._num_marbles_by_color(self.player_color)
        # print(f"total player marbles remaining: {self.opponent_color}", player_marbles_remaining)
        for move, resulting_board in zip(self.gen.moves, self.gen.boards):
            resulting_board_length = len(str(resulting_board))
            current_board_length = len(str(self.manager.board))
            if resulting_board_length < current_board_length:
                # print("Knockout Move")
                knockout_moves_player.append(move)
                knockout_boards.append(resulting_board)

        return knockout_moves_player, knockout_boards

    def num_marbles_taken(self, color):
        return self.manager.board.num_marbles_left_by_color(color)

    def _num_marbles_by_color(self, color):
        return len(self.manager.board.get_marbles_by_color(color))

    def is_marble_near_edge(self, coord):
        if coord in self.EDGE_COORD:
            return True

        neighbors, _ = self.gen.get_neighbors(coord)

        return any(neighbor in self.EDGE_COORD for neighbor in neighbors)

    def switch_players(self):
        self.player_color = "w" if self.player_color == "b" else "b"
        self.opponent_color = "w" if self.player_color == "b" else "b"
