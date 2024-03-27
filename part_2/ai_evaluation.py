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
        self.transposition_table = {}  # Key: (board_hash, depth, maximizingPlayer), Value: score

    def choose_best_move(self, time_limit=0):
        print("Board:", self.manager.board)
        start_time = time.time()
        depth = 1
        best_move = None
        best_score = -float('inf')
        best_board = None

        if self.manager.current_player.color != self.player_color:
            self.switch_players()

        # Continue deepening until the time limit is reached.
        # while True:
        #     score, move, board = self.minimax(self.manager.board, depth, -float('inf'), float('inf'), True, start_time, time_limit)
        #     if move is None:  # Time's up, no move found
        #         break
        #     if score > best_score:
        #         best_score, best_move, best_board = score, move, board
        #     depth += 1
        #     if time.time() - start_time >= time_limit:
        #         break
        score, move, board = self.minimax(self.manager.board, 1, -float('inf'), float('inf'), True, start_time,
                                          time_limit)
        best_score, best_move, best_board = score, move, board

        print(f"Best move at depth {depth - 1}: {best_move}, score: {best_score}")
        return best_move, best_board

    def hash_board(self, depth, board, maximizingPlayer):
        """
        Computes a unique hash value for the current board state, considering the board's state,
        the depth in the game tree, and the current player (maximizing or minimizing).

        :param depth: Current depth in the game tree.
        :param maximizingPlayer: Boolean indicating if it's the maximizing player's turn.
        """
        hash_value = 0
        base = 3
        # Incrementally factor in the state of each position on the board
        for coord in board.BOARD_COORD:
            marble = board.get_marble(coord)
            state = 0  # Assume empty by default
            if marble == "b":
                state = 1
            elif marble == "w":
                state = 2
            hash_value = hash_value * base + state

        # Factor in the depth and the current player
        # Use large primes to minimize collisions and ensure uniqueness
        depth_hash = depth * 7919
        player_hash = 1 if maximizingPlayer else 2
        combined_hash = hash_value * 100003 + depth_hash + player_hash * 1000003

        return combined_hash

    def minimax(self, board, depth, alpha, beta, maximizingPlayer, start_time, time_limit):
        # Time check to stop the search
        # if time.time() - start_time > time_limit:
        #     return -float('inf') if maximizingPlayer else float('inf'), None, None

        # Check if the board state is in the transposition table
        board_hash = self.hash_board(depth, board, maximizingPlayer)
        if board_hash in self.transposition_table:
            print("Transposition table hit!")
            return self.transposition_table[board_hash]  # This now includes the board as well

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
        best_board = None

        # Example of sorting moves based on a simple heuristic evaluation
        sorted_moves = sorted(zip(self.gen.moves, self.gen.boards),
                              key=lambda mb: self.nico_heuristic(mb[1], self.player_color), reverse=maximizingPlayer)
        for move, resulting_board in sorted_moves:
            # Recursive minimax call
            evaluation, _, _ = self.minimax(resulting_board, depth - 1, alpha, beta, not maximizingPlayer, start_time,
                                            time_limit)
            if maximizingPlayer:
                if evaluation > best_score:
                    best_score, best_move, best_board = evaluation, move, resulting_board
                    print(f"best score: {best_score}")
                alpha = max(alpha, evaluation)
            else:
                # print("minimizing player")
                if evaluation < best_score:
                    best_score, best_move, best_board = evaluation, move, resulting_board

                beta = min(beta, evaluation)

            if beta <= alpha:
                break

        # Restore the original player context
        self.player_color, self.opponent_color = original_player_color, original_opponent_color
        self.transposition_table[board_hash] = (best_score, best_move, best_board if best_move else board)
        return best_score, best_move, best_board if best_move else board

    # def nico_heuristic(self, board, player_color):
    #
    #     score = 0
    #
    #
    #
    #     num_marbles_taken = self.num_marbles_taken(self.player_color)
    #     num_marbles_lost = self.num_marbles_taken(self.opponent_color)
    #     player_marbles = board.get_marbles_by_color(player_color)
    #     # print("color playert: ",player_color)
    #     opponent_color = "w" if player_color == "b" else "b"
    #     opponent_marbles = board.get_marbles_by_color(opponent_color)
    #
    #     # Safety: Decrease score for marbles close to the edge
    #     for marble in player_marbles:
    #         if self.is_marble_near_edge(marble):
    #             score += 10
    #
    #     # Aggression: Increase score for opponent marbles near the edge
    #     for marble in opponent_marbles:
    #         if self.is_marble_near_edge(marble):
    #             score -= 1
    #
    #     # Formation Strength: Bonus for each marble that is part of a larger group
    #     for marble in player_marbles:
    #         neighbors, _ = self.gen.get_neighbors(marble)
    #         group_bonus = sum(1 for neighbor in neighbors if neighbor in player_marbles)
    #         score += group_bonus * 1
    #
    #     # Formation Strength: Bonus for each marble that is part of a larger group
    #     # for marble in opponent_marbles:
    #     #     neighbors, _ = self.gen.get_neighbors(marble)
    #     #     group_bonus = sum(1 for neighbor in neighbors if neighbor in opponent_marbles)
    #     #     score += group_bonus
    #
    #     # Direct Knockout Bonus
    #     # print(self.find_knockout_moves())
    #     knockout_moves = self.find_knockout_moves()[0]
    #     # Assuming each knockout move is highly valuable, add a significant score for each.
    #     if num_marbles_taken == 4:
    #         score += len(knockout_moves) * 10000  # Modify the multiplier as needed to balance gameplay.
    #     else:
    #         score += len(knockout_moves) * 10  # Modify the multiplier as needed to balance gameplay.
    #
    #     # Center Control: Additional points for controlling the center of the board
    #     # center_control_bonus = sum(1 for marble in player_marbles if marble in self.CENTER_COORD)
    #     # score += center_control_bonus * 2  # Weight center control more heavily
    #     #
    #     # center_control_bonus = sum(1 for marble in opponent_marbles if marble in self.CENTER_COORD)
    #     # score -= center_control_bonus * 2  # Weight center control more heavily
    #     #
    #     # # Number of marbles taken: Increase score for each marble taken
    #     # score += num_marbles_taken * 10  # Modify the multiplier as needed to balance gameplay.
    #     #
    #     # # Number of marbles lost: Decrease score for each marble lost
    #     # score -= num_marbles_lost * 10
    #
    #     return score

    def nico_heuristic(self, board, player_color):
        score = 0
        total_marbles = len(board.get_marbles_by_color(player_color)) * 2  # Assuming get_all_marbles returns all marbles on the board

        # Identify the game stage based on the number of marbles left
        if total_marbles > 24:  # Early game
            edge_weight = -10
            group_bonus_weight = 1
            knockout_bonus_weight = 10
        elif 16 < total_marbles <= 24:  # Mid game
            edge_weight = -5
            group_bonus_weight = 2
            knockout_bonus_weight = 20
        else:  # Late game
            edge_weight = -1
            group_bonus_weight = 3
            knockout_bonus_weight = 50

        num_marbles_taken = self.num_marbles_taken(self.player_color)
        num_marbles_lost = self.num_marbles_taken(self.opponent_color)
        player_marbles = board.get_marbles_by_color(player_color)
        opponent_color = "w" if player_color == "b" else "b"
        opponent_marbles = board.get_marbles_by_color(opponent_color)

        # Safety: Adjust score for marbles close to the edge based on game stage
        for marble in player_marbles:
            if self.is_marble_near_edge(marble):
                score -= edge_weight

        # Aggression: Adjust score for opponent marbles near the edge based on game stage
        for marble in opponent_marbles:
            if self.is_marble_near_edge(marble):
                score += edge_weight / 10  # Make it less impactful than player marble safety

        # Formation Strength: Bonus for each marble that is part of a larger group, adjusted by game stage
        for marble in player_marbles:
            neighbors, _ = self.gen.get_neighbors(marble)
            group_bonus = sum(1 for neighbor in neighbors if neighbor in player_marbles)
            score += group_bonus * group_bonus_weight

        # Direct Knockout Bonus: Adjust the significance of knockout moves based on game stage
        knockout_moves = self.find_knockout_moves()[0]
        if num_marbles_taken == 4:
            score += len(knockout_moves) * 10000  # Modify the multiplier as needed to balance gameplay.
        else:
            score += len(knockout_moves) * knockout_bonus_weight

        # Number of marbles taken: Increase score for each marble taken
        score -= num_marbles_taken * 10  # Modify the multiplier as needed to balance gameplay.

        # Number of marbles lost: Decrease score for each marble lost
        score += num_marbles_lost * 10

        # Add or adjust other game metrics as needed to fine-tune the heuristic for different stages

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
