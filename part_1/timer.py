class Timer:
    """
    Timer class used to represent time for a move in the game
    """
    def __init__(self):
        self.minutes = 0
        self.seconds = 60

    def restart_timer(self):
        """
        Restarts the timer
        """
        self.seconds = 60

    def increment_timer(self):
        """
        Increments the towards zero
        :return: the new time with one less second as an Int
        """
        self.seconds -= 1
        return self.seconds

    def get_time(self):
        """
        Getter for the current time
        :return:  an Int
        """
        return self.seconds
