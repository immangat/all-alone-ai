import pygame

from part_2.board import Board
from part_2.game_window import GameWindow
from part_2.menu_screen import MenuScreen


class Manager:
    def __init__(self, game_window, board):
        self.game_window = game_window  # This should be an instance of GameWindow class
        self.board_state = ''  # You would set this according to your game logic
        self.is_running = False
        self.board = board  # You would set this according to your game logic
        self.current_screen = "menu"
        self.menu_screen = MenuScreen(game_window.width,
                                      game_window.height,
                                      self)

    def start(self):
        if self.current_screen == "menu":
            self.menu_screen.initWindow()
            self.is_running = True
            self.main_loop()
        elif self.current_screen == "game":
            print("game")
            self.game_window.initWindow()
            self.is_running = True
            self.main_loop()

    def switch_to_screen(self, screen_name):
        """Switches the current screen to the given screen name."""
        self.current_screen = screen_name
        if screen_name == "menu":
            self.menu_screen.initWindow()
        elif screen_name == "game":
            self.game_window.initWindow()

    def main_loop(self):
        clock = pygame.time.Clock()
        while self.is_running:
            time_delta = clock.tick(60) / 1000.0
            self.menu_screen.event_handler.handle_events()
            if self.current_screen == "menu":  # we should probably create an abstact window class
                self.menu_screen.updateWindow()
            elif self.current_screen == "game":
                self.game_window.manager_ui.update(time_delta)
                self.game_window.updateWindow()  # Draw the board state


if __name__ == "__main__":
    board = Board()
    board.setup_belgian_daisy()

    manager = Manager(GameWindow(1280, 720), board)
    game = Manager(GameWindow(1280, 720, manager), board)
    game.start()
