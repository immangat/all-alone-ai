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

    def evaluate_board_state(self, board, player_color):
        score = 0
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
        for marble in player_marbles:
            if self.can_knockout(marble, board, player_color):
                score += 10  # Assign a high score for potential knockouts

        # Positional Advantage for Future Knockouts
        for marble in player_marbles:
            if self.is_position_advantageous_for_knockout(marble, board, player_color):
                score += 5  # Reward positions that could lead to knockouts

        # Center Control: Additional points for controlling the center of the board
        center_control_bonus = sum(1 for marble in player_marbles if marble in self.CENTER_COORD)
        score += center_control_bonus * 5  # Weight center control more heavily

        center_control_bonus = sum(1 for marble in opponent_marbles if marble in self.CENTER_COORD)
        score -= center_control_bonus * 5  # Weight center control more heavily

        return score

    def is_marble_near_edge(self, coord):
        if coord in self.EDGE_COORD:
            return True

        neighbors, _ = self.manager.gen.get_neighbors(coord)

        return any(neighbor in self.EDGE_COORD for neighbor in neighbors)
