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
        self.current_screen = "game"
        self.menu_screen = MenuScreen(game_window.width,
                                      game_window.height,
                                      game_window.manager_ui)

    # def start(self):
    #     self.is_running = True
    #     self.game_window.initWindow()
    #     self.main_loop()

    def start(self):
        if self.current_screen == "menu":
            self.menu_screen.create_menu()
            self.is_running = True
            self.main_loop()
        elif self.current_screen == "game":
            print("game")
            self.game_window.initWindow()
            self.is_running = True
            self.main_loop()

    def main_loop(self):
        clock = pygame.time.Clock()
        while self.is_running:
            time_delta = clock.tick(60) / 1000.0
            self.game_window.event_handler.handle_events()
            if self.current_screen == "menu":
                # self.menu_screen.handle_events()
                print("drawing menu")
            elif self.current_screen == "game":
                self.game_window.manager_ui.update(time_delta)
                self.game_window.updateWindow()  # Draw the board state

if __name__ == "__main__":
    board = Board()
    board.setup_belgian_daisy()

    manager = Manager(GameWindow(1280, 720), board)
    game = Manager(GameWindow(1280, 720, manager), board)
    game.start()
