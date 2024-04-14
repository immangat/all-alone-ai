import pygame
import pygame_gui

CUSTOM_TIMER_EVENT = pygame.USEREVENT + 1


class EventHandler:
    """
    A class to handle different types of events within a game application, managing
    interactions with the GUI and the game state based on the current screen.
    """

    def __init__(self, window=None, manager=None):
        """
        Initialize the EventHandler with references to the game window and game manager.

        Args:
            window: The game window instance which provides UI and game display functions.
            manager: The game manager instance which handles game logic and state management.
        """
        self.window = window
        self.manager = manager
        self.selected_marble = []

    def handle_events(self):
        """
        Directs event handling to the appropriate method based on the current window type.
        """
        if self.window.type == "menu":
            self.handle_menu_events()
        elif self.window.type == "game":
            self.handle_game_events()

    def handle_menu_events(self):
        """
        Handles events specific to the menu screen, such as button clicks and UI updates.
        """
        self.window.menu.update(pygame.event.get())

    def handle_game_events(self):
        """
        Handles events specific to the game screen, including user interactions like button
        clicks, mouse clicks, key presses, and custom timer events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.USEREVENT:
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
                    elif event.ui_element == self.window.button_gui.stop:
                        print("Stopping game")
                        self.manager.stop_game()
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
        """
        Handles mouse click events, detecting interactions with the game board,
        such as selecting marbles or potential moves.

        Args:
            mouse_pos (tuple): The x and y coordinates of the mouse click.
        """
        if self.window.manager.current_screen == "game" and not self.manager.is_game_over():
            self._marbles_clicked(mouse_pos)

    def _marbles_clicked(self, mouse_pos):
        """
        Detects if a marble was clicked based on its position on the screen and initiates
        appropriate actions if it matches conditions for a move or selection.

        Args:
            mouse_pos (tuple): The x and y coordinates where the mouse was clicked.
        """
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
        """
        Attempts to make a move in the game based on the selected marble and its neighboring positions.

        Args:
            coord (tuple): Coordinates of the clicked position on the board.
        """
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
        """
        Highlights a circle on the game board, indicating that it has been selected.

        Args:
            coord (tuple): Coordinates of the circle to highlight.
            radius (int): Radius of the circle to be highlighted.
        """
        self.selected_marble.append(coord)
        print(self.selected_marble)
        x_pixel, y_pixel = self.window.board_to_pixel(coord)
        pygame.draw.circle(self.window.background, (255, 102, 102), (x_pixel, y_pixel), radius + 3, 3)
        self.window.display_surface.blit(self.window.background, (0, 0))
        pygame.display.flip()
