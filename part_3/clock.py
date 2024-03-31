import time


class Clock:

    def __init__(self):
        self.current_time = 0
        self.tick_value = 333
        self.can_tick = True
        self.reset_value = 0

    @property
    def current_timer(self):
        return self.current_time

    def set_clock_time_values(self, timer_value):
        self.current_time = timer_value
        self.reset_value = timer_value

    def tick_timer(self):
        if self.can_tick:
            self.current_time += self.tick_value

    def increment_timer(self):
        if self.can_tick:
            self.current_time += self.tick_value

    def decrement_timer(self):
        if self.can_tick:
            if self.current_time - self.tick_value <= 0:
                self.current_time = 0
            else:
                self.current_time -= self.tick_value

    def reset_timer(self):
        self.current_time = 0

    def reset_to_full(self):
        self.current_time = self.reset_value
