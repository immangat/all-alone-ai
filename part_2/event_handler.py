import pygame

CUSTOM_TIMER_EVENT = pygame.USEREVENT + 1


class EventHandler:
    def __init__(self, game_window):
        self.game_window = game_window

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                self.game_window.draw_board()
                self.game_window.updateWindow()
                self.on_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game_window.manager.switch_turns()
            elif event.type == CUSTOM_TIMER_EVENT:
                self.game_window.manager.tick_timer()
                self.game_window.draw_time()

    def on_mouse_click(self, mouse_pos):
        # Check if the click is within the radius of any circle
        self._marbles_clicked(mouse_pos)

    def _marbles_clicked(self, mouse_pos):
        for coord in self.game_window.get_board_tuples():
            marble_pos = self.game_window.board_to_pixel(coord)
            if self.game_window.is_within_circle(mouse_pos, marble_pos, self.game_window.marble_radius):
                if coord not in self.game_window.highlighted_marbles:
                    print(f"Marble at {coord} was added.")
                    self.highlight_circle(coord, self.game_window.marble_radius)
                    self.game_window.highlighted_marbles.append(coord)
                elif coord in self.game_window.highlighted_marbles:
                    print(f"Marble at {coord} was removed.")
                    self.game_window.highlighted_marbles.remove(coord)
                    self.game_window.draw_board()
                break

    def highlight_circle(self, coord, radius):
        # Draw a circle with a different color to highlight it
        x_pixel, y_pixel = self.game_window.board_to_pixel(coord)
        pygame.draw.circle(self.game_window.display_surface, (255, 102, 102), (x_pixel, y_pixel), radius + 3, 3)
        pygame.display.flip()
