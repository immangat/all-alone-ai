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
        # done outside the loop the first time to optimize performance
        self.game_window.draw_board()
        self.game_window.updateWindow()
        # This would be the main loop where you keep the game running and handle events
        while self.is_running:
            self.game_window.event_handler.handle_events()


if __name__ == "__main__":
    board = Board()
    board.setup_belgian_daisy()
    manager = Manager(GameWindow(1280, 720), board)
    game = Manager(GameWindow(1280, 720, manager), board)
    game.start()
