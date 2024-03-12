import time


class Clock:

    def __init__(self):
        self.current_time = 0
        self.tick_value = 1
        self.can_tick = True

    @property
    def current_timer(self):
        return self.current_time

    def tick_timer(self):
        if self.can_tick:
            self.current_time += self.tick_value

    def reset_timer(self):
        self.current_time = 0
