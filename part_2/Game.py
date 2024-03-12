class Game:
    def __init__(self, player_one, player_two, board, max_turns, max_time):
        self.player_one = player_one
        self.player_two = player_two
        self.board = board
        self.max_turns = max_turns
        self.max_time = max_time
        self.current_player = self.player_one
        self.current_turn = 1
        self.timer = "implement this logic"