import time


class Clock:

    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0
        self.time_limit = 0

    def start_timer(self):
        self.start_time = time.time_ns()

    def pause_timer(self):
        pass

    def reset_timer(self):
        pass
