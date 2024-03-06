class Timer:
    def __init__(self):
        self.minutes = 0
        self.seconds = 60

    def restart_timer(self):
        self.seconds = 60

    def increment_timer(self):
        self.seconds -= 1
        return self.seconds

    def get_time(self):
        return self.seconds
