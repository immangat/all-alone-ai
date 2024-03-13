import pygame

from part_2.board import Board
from part_2.game_window import GameWindow


class Manager:
    def __init__(self, game_window, board):
        self.game_window = game_window  # This should be an instance of GameWindow class
        self.board_state = ''  # You would set this according to your game logic
        self.is_running = False
        self.board = board  # You would set this according to your game logic

    def start(self):
        self.is_running = True
        self.game_window.initWindow()
        self.main_loop()

    def main_loop(self):
        clock = pygame.time.Clock()
        # originally planned to only update on mouse click, but for simplicity will update everything for now
        # self.game_window.draw_board()
        # self.game_window.updateWindow()
        # self.game_window.manager_ui.draw_ui(self.game_window.display_surface)
        # This would be the main loop where you keep the game running and handle events
        while self.is_running:
            time_delta = clock.tick(60) / 1000.0
            self.game_window.event_handler.handle_events()
            self.game_window.manager_ui.update(time_delta)
            self.game_window.updateWindow()  # Draw the board state


if __name__ == "__main__":
    board = Board()
    board.setup_belgian_daisy()

    manager = Manager(GameWindow(1280, 720), board)
    game = Manager(GameWindow(1280, 720, manager), board)
    game.start()
