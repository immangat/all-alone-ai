import pygame
import pygame_gui


class EventHandler:
    def __init__(self, game_window):
        self.game_window = game_window
        self.test = 0

    def handle_events(self):
        if self.game_window.manager.current_screen == "menu":
            # self.handle_menu_events()
            pass
        elif self.game_window.manager.current_screen == "game":
            # print("game handling events")
            self.handle_game_events()

    # def handle_menu_events(self, event):
    #     self.game_window.manager.menu_screen.handle_events(event)

    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.game_window.move_gui.undo_button:
                        print("Button was clicked!")
                    elif event.ui_element == self.game_window.move_gui.add_button:
                        self.test += 1
                        self.game_window.move_gui.add_move(str(self.test))  # Customize as needed
                        self.game_window.move_gui.moves_gui.rebuild()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                self.on_mouse_click(event.pos)
                self.game_window.manager_ui.process_events(event)

            self.game_window.manager_ui.process_events(event)

    def on_mouse_click(self, mouse_pos):
        # Check if the click is within the radius of any circle
        if self.game_window.manager.current_screen == "game":
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
                    self.game_window.updateWindow()
                break

    def highlight_circle(self, coord, radius):
        # Draw a circle with a different color to highlight it
        x_pixel, y_pixel = self.game_window.board_to_pixel(coord)
        pygame.draw.circle(self.game_window.background, (255, 102, 102), (x_pixel, y_pixel), radius + 3, 3)
        self.game_window.display_surface.blit(self.game_window.background, (0, 0))
        pygame.display.flip()
