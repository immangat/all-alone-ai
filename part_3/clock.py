import time

class Clock:
    """
    A class used to simulate a simple clock that can tick, increment, decrement,
    and reset based on given time values.
    """

    def __init__(self):
        """
        Initializes a new Clock instance with default settings.
        """
        self.current_time = 0  # Start time of the clock
        self.tick_value = 333  # Time added or subtracted during tick or increment/decrement operations
        self.can_tick = True   # Boolean to control if the clock can tick
        self.reset_value = 0   # Stores the initial set time for full resets

    @property
    def current_timer(self):
        """
        Property that gets the current time of the clock.

        Returns:
            int: The current time of the clock.
        """
        return self.current_time

    def set_clock_time_values(self, timer_value):
        """
        Sets the clock's current time and reset value to the specified timer value.

        Args:
            timer_value (int): The value to set the clock's time and reset value.
        """
        self.current_time = timer_value
        self.reset_value = timer_value

    def tick_timer(self):
        """
        Advances the clock's time by a predefined tick value if ticking is allowed.
        """
        if self.can_tick:
            self.current_time += self.tick_value

    def increment_timer(self):
        """
        Increments the clock's time by a predefined tick value if incrementing is allowed.
        """
        if self.can_tick:
            self.current_time += self.tick_value

    def decrement_timer(self):
        """
        Decrements the clock's time by a predefined tick value if decrementing is allowed.
        If the result is less than or equal to zero, sets the time to zero.
        """
        if self.can_tick:
            if self.current_time - self.tick_value <= 0:
                self.current_time = 0
            else:
                self.current_time -= self.tick_value

    def reset_timer(self):
        """
        Resets the clock's time to zero.
        """
        self.current_time = 0

    def reset_to_full(self):
        """
        Resets the clock's time to the previously set reset value.
        """
        self.current_time = self.reset_value
