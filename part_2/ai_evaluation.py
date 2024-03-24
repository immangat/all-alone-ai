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
        self.player_color = manager.current_player.color
        self.opponent_color = "w" if self.player_color == "b" else "b"

    def evaluate_board_state(self, board, player_color):

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
            neighbors, _ = self.manager.gen.get_neighbors(marble)
            group_bonus = sum(1 for neighbor in neighbors if neighbor in player_marbles)
            score += group_bonus

        # Formation Strength: Bonus for each marble that is part of a larger group
        for marble in opponent_marbles:
            neighbors, _ = self.manager.gen.get_neighbors(marble)
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
        player_marbles_remaining = self.num_marbles_by_color(self.player_color)
        print(f"total player marbles remaining: {self.opponent_color}", player_marbles_remaining)
        for move, resulting_board in zip(self.manager.gen.moves, self.manager.gen.boards):
            resulting_board_length = len(str(resulting_board))
            current_board_length = len(str(self.manager.board))
            if resulting_board_length < current_board_length:
                print("Knockout Move")
                knockout_moves_player.append(move)
                knockout_boards.append(resulting_board)

        return knockout_moves_player, knockout_boards

    def num_marbles_taken(self, color):
        return self.manager.board.num_marbles_left_by_color(color)



    def num_marbles_by_color(self, color):
        return len(self.manager.board.get_marbles_by_color(color))

    def is_marble_near_edge(self, coord):
        if coord in self.EDGE_COORD:
            return True

        neighbors, _ = self.manager.gen.get_neighbors(coord)

        return any(neighbor in self.EDGE_COORD for neighbor in neighbors)
