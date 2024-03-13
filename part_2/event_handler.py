import pygame
import pygame_gui



class EventHandler:
    def __init__(self, window=None):
        self.window = window
        self.test = 0

    def handle_events(self):
        if self.window.type == "menu":
            self.handle_menu_events()
        elif self.window.type == "game":
            # print("game handling events")
            self.handle_game_events()

    def handle_menu_events(self):
        self.window.menu.update(pygame.event.get())

    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.USEREVENT:
                print(self.window)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.window.move_gui.undo_button:
                        print("Button was clicked!")
                    elif event.ui_element == self.window.move_gui.add_button:
                        self.test += 1
                        self.window.move_gui.add_move(str(self.test))  # Customize as needed
                        self.window.move_gui.moves_gui.rebuild()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                self.on_mouse_click(event.pos)
                self.window.manager_ui.process_events(event)

            self.window.manager_ui.process_events(event)

    def on_mouse_click(self, mouse_pos):
        # Check if the click is within the radius of any circle
        if self.window.manager.current_screen == "game":
            self._marbles_clicked(mouse_pos)

    def _marbles_clicked(self, mouse_pos):
        for coord in self.window.get_board_tuples():
            marble_pos = self.window.board_to_pixel(coord)
            if self.window.is_within_circle(mouse_pos, marble_pos, self.window.marble_radius):
                if coord not in self.window.highlighted_marbles:
                    print(f"Marble at {coord} was added.")
                    self.highlight_circle(coord, self.window.marble_radius)
                    self.window.highlighted_marbles.append(coord)
                elif coord in self.window.highlighted_marbles:
                    print(f"Marble at {coord} was removed.")
                    self.window.highlighted_marbles.remove(coord)
                    self.window.updateWindow()
                break

    def highlight_circle(self, coord, radius):
        # Draw a circle with a different color to highlight it
        x_pixel, y_pixel = self.window.board_to_pixel(coord)
        pygame.draw.circle(self.window.background, (255, 102, 102), (x_pixel, y_pixel), radius + 3, 3)
        self.window.display_surface.blit(self.window.background, (0, 0))
        pygame.display.flip()
