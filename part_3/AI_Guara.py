from state_space_gen import StateSpaceGen
from board import Board
from player import AIPlayer
from IO_handler import IOHandler
import time


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
        self.load_transposition_table()
        self.inner_transposition_table = {}

    def _calculate_move(self, board, queue, start_time, **kwargs):
        depth = kwargs.get('depth')
        return self.get_best_move(board, depth, start_time, queue)

    def get_color(self):
        return self.color

    def load_transposition_table(self):
        transposition_table_data = IOHandler.read_transposition_table_from_file(self.color)
        if transposition_table_data is not None:
            self.transposition_table = transposition_table_data

    def get_best_move(self, board, depth):
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
                    score = self.alpha_beta(gen_board, depth - 1, alpha, beta, 'w')
                    self.transposition_table[hash_key] = score
                else:
                    score = self.alpha_beta(gen_board, depth - 1, alpha, beta, 'b')
                    self.transposition_table[hash_key] = score

            if (self.color == 'b' and score > best_score) or (self.color == 'w' and score < best_score):
                best_score = score
                best_move = gen.get_moves()[gen.get_index_from_board_string(gen_board)]
                # time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                # queue.put((best_move, time_for_this_move))
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

        return best_move, best_board

    def board_evaluation(self, board):
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

    # def calculate_distance(self, player, board):
    #     marbles = board.get_marbles_by_color(player)
    #     gen = StateSpaceGen()
    #     count = 0
    #     for marble in marbles:
    #         neighbors = gen.get_neighbors(marble)
    #         for neighbor in neighbors[0]:
    #             if board.get_marble(neighbor) == player:
    #                 count += 1
    #     return count

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

    def get_weights(self):
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
            return self.board_evaluation(board)

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


class AIAgentTester():
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

    def __init__(self, color):
        self.color = color
        self.weights = self.get_weights()
        self.transposition_table = {}
        self.inner_transposition_table = {}
        self.depth = (4 if self.color == "b" else 2)

    # def _calculate_move(self, board, queue, start_time, **kwargs):
    #     return self.get_best_move(board, start_time, queue)

    def get_color(self):
        return self.color

    def load_transposition_table(self):
        transposition_table_data = IOHandler.read_transposition_table_from_file(self.color)
        if transposition_table_data is not None:
            self.transposition_table = transposition_table_data

    def get_best_move(self, board):
        self.load_transposition_table()
        best_move = None
        best_board = None
        best_score = -self.INFINITY if self.color == 'b' else self.INFINITY
        gen = StateSpaceGen()
        gen.generate_state_space(board, self.color)

        alpha = -self.INFINITY
        beta = self.INFINITY

        ordered_boards = self.state_ordering(gen.get_boards())
        # queue.put((gen.get_moves()[0], 0))
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
                # time_for_this_move = (time.time_ns() - start_time) / 1_000_000
                # if time_for_this_move >= self.time_per_move * 1000:
                #     break
                # queue.put((best_move, time_for_this_move))
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

        print(f"Best score: {best_score}")
        print(f"Best move: {best_move}")
        return best_move, best_board

    def nico_heuristic(self, board):
        score = 0
        total_marbles = board.count_marbles() # Assuming get_all_marbles returns all marbles on the board
        inverter = (1 if self.color == 'b' else -1)

        # Identify the game stage based on the number of marbles left
        if total_marbles > 24:  # Early game
            edge_weight = 10
            group_bonus_weight = 1
            knockout_bonus_weight = 10
        elif 21 < total_marbles <= 24:  # Mid game
            edge_weight = -5
            group_bonus_weight = 2
            knockout_bonus_weight = 20
        else:  # Late game
            edge_weight = -1
            group_bonus_weight = 3
            knockout_bonus_weight = 50

        num_marbles_black = board.num_marbles_left_by_color("b")
        num_marbles_white = board.num_marbles_left_by_color("w")
        black_marbles = board.get_marbles_by_color("b")
        # opponent_color = "w" if player_color == "b" else "b"
        white_marbles = board.get_marbles_by_color("w")

        # Safety: Adjust score for marbles close to the edge based on game stage
        for marble in black_marbles:
            if marble in board.EDGE_COORD:
                score -= edge_weight / (10 if self.color == "w" else 1)

        # Aggression: Adjust score for opponent marbles near the edge based on game stage
        for marble in white_marbles:
            if marble in board.EDGE_COORD:
                score += edge_weight / (10 if self.color == "b" else 1)  # Make it less impactful than player marble safety

        # Formation Strength: Bonus for each marble that is part of a larger group, adjusted by game stage
        player_marbles = board.get_marbles_by_color(self.color)
        for marble in player_marbles:
            neighbors = Board.get_neighbors_only(marble)
            group_bonus = sum(1 for neighbor in neighbors if neighbor in player_marbles)
            score += group_bonus * group_bonus_weight * inverter #positive for black, negative for white

        # Direct Knockout Bonus: Adjust the significance of knockout moves based on game stage
        knockout_moves = self.find_knockout_moves(board, (num_marbles_white if self.color == "b" else num_marbles_black))
        if (14 - (num_marbles_white if self.color == "b" else num_marbles_black)) == 4:
            score += knockout_moves * 10000 * inverter # Modify the multiplier as needed to balance gameplay.
        else:
            score += knockout_moves * knockout_bonus_weight * inverter

        # Number of marbles taken: Increase score for each marble taken
        # Adjusted black: the more lost marbles black has the lower the score (black is maximizing player)
        score -= (14 - num_marbles_black) * 10 # Modify the multiplier as needed to balance gameplay.

        # Number of marbles lost: Decrease score for each marble lost
        # Adjusted white: the more lost marbles white has the higher the score (white is minimizing player)
        score += (14 - num_marbles_white) * 10

        # Add or adjust other game metrics as needed to fine-tune the heuristic for different stages

        return score

    def find_knockout_moves(self, board, num_opponent_marbles):
        count = 0
        gen = StateSpaceGen()
        gen.generate_state_space(board, self.color)
        for new_circles in gen.get_boards():
            new_board = Board()
            new_board.set_circles(new_circles)
            if len(new_board.get_marbles_by_color("w" if self.color== "b" else "b")) < num_opponent_marbles:
                count += 1

        return count

    def evaluate_position(self, board, max_player):
        # number_off_grid
        black_total = board.num_marbles_left_by_color("b") * self.weights["b_off"]
        white_total = board.num_marbles_left_by_color("w") * self.weights["w_off"] * self.weights["empower_self"]
        black_score = board.num_marbles_left_by_color("b") * self.weights["b_off"]
        white_score = board.num_marbles_left_by_color("w") * self.weights["w_off"] * self.weights["empower_self"]

        # points for position (the closer to the center, the better)

        for coord in Board.BOARD_COORD:
            index = Board.BOARD_COORD.index(coord)
            if board.get_marble(coord) == "b":
                black_score += self.POINT_VALUES[index] * self.weights["b_pos"]
            elif board.get_marble(coord) == "w":
                white_score += self.POINT_VALUES[index] * self.weights["w_pos"] * \
                               (self.weights["empower_self"] if self.POINT_VALUES[index] < 0 else 1)

        # points for coherence
        black_score += self.calculate_group_score("b", board) * self.weights["b_coherence"]
        white_score += self.calculate_group_score("w", board) * self.weights["w_coherence"]

        if white_total != -black_total:
            print(board)
            print(f"white {white_total}, black {black_total}")
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
        weights["b_off"] = -150
        weights["w_off"] = 150
        weights["b_pos"] = 4
        weights["w_pos"] = -4
        weights["b_coherence"] = 1
        weights["w_coherence"] = -1
        weights["empower_self"] = 10
        return weights

    def alpha_beta(self, board, depth, alpha, beta, current_player):

        hash_key = board.hash_board()
        if hash_key in self.inner_transposition_table:
            return self.inner_transposition_table[hash_key]
        if depth == 0:
            if self.color == "b":
                return self.evaluate_position(board, current_player)
            elif self.color == "w":
                return self.nico_heuristic(board)

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
