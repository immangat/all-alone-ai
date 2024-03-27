from state_space_gen import StateSpaceGen
from board import Board


class AIAgent:
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

    def __init__(self):
        self.weights = self.get_weights()
        self.transposition_table = {}

    def get_best_move(self, board, current_player, depth):
        best_move = None
        best_board = None
        best_score = -self.INFINITY if current_player == 'b' else self.INFINITY
        gen = StateSpaceGen()
        gen.generate_state_space(board, current_player)

        evaluated_moves =[]

        for gen_board in gen.get_boards():
            score = self.board_evaluation(gen_board)
            evaluated_moves.append((gen_board, score))

        if current_player == 'b':
            evaluated_moves.sort(key=lambda x: x[1], reverse=True)  # Higher scores first
        else:
            evaluated_moves.sort(key=lambda x: x[1])  # Lower scores first

        alpha = -self.INFINITY if current_player == 'b' else self.INFINITY
        beta = self.INFINITY if current_player == 'b' else -self.INFINITY

        for gen_board, score in evaluated_moves:
            if current_player == 'b':
                score = self.alpha_beta(gen_board, depth - 1, alpha, beta, 'w')
            else:
                score = self.alpha_beta(gen_board, depth - 1, alpha, beta, 'b')

            if (current_player == 'b' and score > best_score) or (current_player == 'w' and score < best_score):
                best_score = score
                best_move = gen.get_moves()[gen.get_index_from_board(gen_board)]
                best_board = gen_board

            # Update alpha or beta for pruning
            if current_player == 'b':
                alpha = max(alpha, best_score)
            else:
                beta = min(beta, best_score)

            # Pruning when scores do not improve for the player
            if beta <= alpha:
                break

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

        # Points for mobility (number of legal moves) <- removed due to poor efficiency
        # genb = StateSpaceGen()
        # genw = StateSpaceGen()
        # genb.generate_state_space(board, "b")
        # genw.generate_state_space(board, "w")
        # b_moves = genb.get_moves()
        # w_moves = genw.get_moves()
        #
        # black_mobility = len(b_moves)
        # white_mobility = len(w_moves)
        # black_score += black_mobility * self.weights["b_mobility"]
        # white_score += white_mobility * self.weights["w_mobility"]

        # points for coherence
        black_score += self.calculate_group_score("b", board) * self.weights["b_coherence"]
        white_score += self.calculate_group_score("w", board) * self.weights["w_coherence"]

        return black_score + white_score

    def calculate_distance(self, player, board):
        marbles = board.get_marbles_by_color(player)
        gen = StateSpaceGen()
        count = 0
        for marble in marbles:
            neighbors = gen.get_neighbors(marble)
            for neighbor in neighbors[0]:
                if board.get_marble(neighbor) == player:
                    count += 1
        return count


    def calculate_group_score(self, player, board):
        marbles = board.get_marbles_by_color(player)
        visited = set()
        group_score = 0

        for marble in marbles:
            if marble not in visited:
                group_size = self.dfs_group_size(marble, player, board, visited)
                group_score += group_size
        return group_score

    def dfs_group_size(self, marble, player, board, visited):
        stack = [marble]
        group_size = 0

        while stack:
            current_marble = stack.pop()
            if current_marble not in visited:
                visited.add(current_marble)
                group_size += 1
                neighbors = StateSpaceGen().get_neighbors(current_marble)[0]
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
        if hash_key in self.transposition_table:
            return self.transposition_table[hash_key]

        if depth == 0:
            return self.board_evaluation(board)

        gen = StateSpaceGen()
        gen.generate_state_space(board, current_player)
        if current_player == "b":
            value = -self.INFINITY
            for gen_board in gen.get_boards():
                value = max(value, self.alpha_beta(gen_board, depth - 1, alpha, beta, "w"))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cut-off
            self.transposition_table[hash_key] = value
            return value
        else:
            value = self.INFINITY
            for gen_board in gen.get_boards():
                value = min(value, self.alpha_beta(gen_board, depth - 1, alpha, beta, "b"))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cut-off
            self.transposition_table[hash_key] = value
            return value

    def state_ordering(self):
        pass

    def actions(self):
        pass

    def values(self):
        pass

    def policies(self):
        pass
