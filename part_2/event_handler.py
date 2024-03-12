import pygame


class EventHandler:
    def __init__(self, game_window):
        self.game_window = game_window

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                self.on_mouse_click(event.pos)

    def on_mouse_click(self, mouse_pos):
        # Check if the click is within the radius of any circle
        self._marbles_clicked(mouse_pos)

    def _marbles_clicked(self, mouse_pos):
        for coord in self.game_window.get_board_tuples():
            marble_pos = self.game_window.board_to_pixel(coord)
            if self.game_window.is_within_circle(mouse_pos, marble_pos, self.game_window.marble_radius):
                print(f"Marble at {coord} was clicked.")
