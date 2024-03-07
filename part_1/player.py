from functools import reduce

from timer import Timer


class Player:
    """
    Player class for a single player who is playing the game
    """
    def __init__(self, color, player_type):
        self.color = color
        self.current_turn = False  # Initially, not the player's turn
        self.moves = 0
        self.score = 0
        self.timer = Timer()
        self.move_times = []
        self.playerType = player_type
        self.move_list = []

    def get_color(self):
        """Get the color of the player"""
        return self.color

    def get_current_turn(self):
        """Check if it's the player's turn"""
        return self.current_turn

    def flip_turn(self):
        """Flip the player's to the other player"""
        self.current_turn = not self.current_turn
        self.timer.restart_timer()

    def get_score(self):
        """Get the score of the player"""
        return self.score

    def set_score(self, score):
        """Set the score of the player"""
        self.score = score

    def score_up(self):
        """Score the player is incremented by one"""
        self.score += 1

    def reverse_score(self):
        """Score the player is decremented by one"""
        self.score -= 1

    def move_up(self):
        """
        Players total moves are incremented by one
        """
        self.moves += 1

    def reverse_move(self):
        """
        Players total moves are decremented by one
        """
        self.moves -= 1

    def get_moves(self):
        """
        Getter for the number of moves the player has made
        returns: the number of moves the player has made as an Int
        """
        return self.moves

    def get_move_list(self):
        """
        Getter for the list of moves the player has made
        :return: is a list of moves
        """
        return self.move_list

    def increment_time(self):
        """Increments the timer of the player"""
        return self.timer.increment_timer()

    def reset_timer(self):
        """Resets the timer of the player"""
        self.move_times.append(60 - self.timer.get_time())
        self.timer.restart_timer()

    def get_time(self):
        """
        Gets the time of the move for the player
        :return: is the time as an Int
        """
        return self.timer.seconds

    def get_aggregate_time(self):
        """
        Gets the aggregate time of the move for the player
        :return: is the aggregate time as an Int
        """
        if len(self.move_times) == 0:
            return 0
        return reduce(lambda x, y: x + y, self.move_times)

    def get_last_move_time(self):
        """
        Gets the most recent time of the move for the player
        :return: is the most recent time as an Int
        """
        if len(self.move_times) == 0:
            return 0

        return self.move_times[len(self.move_times) - 1]

    def clear_clock(self):
        """Clears the clock of the player"""
        self.move_times = []
        self.reset_timer()

        return self.move_times[len(self.move_times) - 1] 
      
    def remove_last_move(self):
        """Removes the most recent move the player has made"""
        if len(self.move_list) > 0:
            self.move_list.pop()
            return True
        return False

