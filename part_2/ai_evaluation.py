class move_evaluation:
    def __init__(self, manager):
        self.manager = manager

    def evaluate_board_state(self, board, player_color):
        score = 0
        # Safety: Decrease score for marbles close to the edge
        for marble in board.get_marbles_by_color(player_color):
            if self.is_marble_near_edge(marble):
                print(f"Marble {marble} is near the edge")
                score -= 1
        #TODO for now I will assume the ai is always white. I will change this later once we implement the ai selection

        # Aggression: Increase score for opponent marbles near the edge
        opponent_color = "w" if player_color == "b" else "b"
        for marble in board.get_marbles_by_color(opponent_color):
            if self.is_marble_near_edge(marble):
                score += 1

        # Control: Modify score based on control of center or strategic areas (implementation dependent on your game logic)

        return score

    def is_marble_near_edge(self, coord):
        if coord in self.manager.board.EDGE_COORD:
            return True

        neighbors, _ = self.manager.gen.get_neighbors(coord)

        return any(neighbor in self.manager.board.EDGE_COORD for neighbor in neighbors)

