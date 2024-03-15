import pygame
import pygame_gui

CUSTOM_TIMER_EVENT = pygame.USEREVENT + 1


class EventHandler:
    def __init__(self, window=None, manager=None):
        self.window = window
        self.manager = manager
        self.test = 0
        self.selected_marble = []

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
                # print(self.window)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.window.move_gui.undo_button:
                        print("Undo?")
                        self.manager.undo_move()
                    elif event.ui_element == self.window.button_gui.pause:
                        print("jkaghfjhajhfajf")
                        self.manager.pause_game()
                    elif event.ui_element == self.window.button_gui.reset:
                        print("Resetting game")
                        self.manager.reset_game()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                self.on_mouse_click(event.pos)
                self.window.manager_ui.process_events(event)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.manager.switch_turns()
                self.window.highlighted_marbles = []
            elif event.type == CUSTOM_TIMER_EVENT:
                self.manager.tick_timer()
            self.window.manager_ui.process_events(event)

    def on_mouse_click(self, mouse_pos):
        # Check if the click is within the radius of any circle
        if self.window.manager.current_screen == "game":
            self._marbles_clicked(mouse_pos)

    def _marbles_clicked(self, mouse_pos):
        for coord in self.window.get_board_tuples():
            marble_pos = self.window.board_to_pixel(coord)
            if self.window.is_within_circle(mouse_pos, marble_pos, self.window.marble_radius):
                color_of_marble = self.manager.board.get_circle(coord[0], coord[1])
                if color_of_marble is None or color_of_marble != self.manager.current_player.color:
                    print(len(self.selected_marble))
                    if len(self.selected_marble) > 0:
                        self.make_move(coord)
                    self.window.highlighted_marbles = []
                    self.selected_marble = []
                    break
                if coord not in self.window.highlighted_marbles:
                    self.highlight_circle(coord, self.window.marble_radius)
                    self.window.highlighted_marbles.append(coord)
                elif coord in self.window.highlighted_marbles:
                    self.window.highlighted_marbles.remove(coord)
                    self.selected_marble.pop()
                    self.window.updateWindow()
                break

    def make_move(self, coord):
        neighbors = self.manager.gen.get_neighbors(self.selected_marble[-1])
        index = None
        for neighbor in neighbors[0]:
            if coord == neighbor:
                print("Im a neighbour")
                index = neighbors[0].index(neighbor)
                break
        if index is not None:
            print(f" index {neighbors[1][index]}")
            direction = neighbors[1][index]
            if self.selected_marble is not None:
                print("move?")
                self.manager.validate_and_make_move(self.selected_marble, direction)

    def highlight_circle(self, coord, radius):
        # Draw a circle with a different color to highlight it
        self.selected_marble.append(coord)
        print(self.selected_marble)
        x_pixel, y_pixel = self.window.board_to_pixel(coord)
        pygame.draw.circle(self.window.background, (255, 102, 102), (x_pixel, y_pixel), radius + 3, 3)
        self.window.display_surface.blit(self.window.background, (0, 0))
        pygame.display.flip()
