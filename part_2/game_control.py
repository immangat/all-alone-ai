import pygame

from part_2.board import Board
from part_2.clock import Clock
from part_2.game_window import GameWindow
from part_2.player import Player, HumanPlayer


class Manager:
    __instance = None

    def __init__(self, board):
        if Manager.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            Manager.__instance = self
            self.game_window = GameWindow(1280, 720, self)  # This should be an instance of GameWindow class
            self.board_state = ''  # You would set this according to your game logic
            self.is_running = False
            self.board = board  # You would set this according to your game logic
            self.clock = Clock()
            self.players = [HumanPlayer("White"), HumanPlayer("Black")]
            self.current_player: Player = self.players[0]

    @staticmethod
    def get_instance(game_window=None, board=None):
        if Manager.__instance is None:
            Manager(game_window, board)
        return Manager.__instance

    def start(self):
        self.is_running = True
        self.game_window.initWindow()
        self.main_loop()

    def end_game(self):
        pass

    def pause_game(self):
        pass

    def switch_turns(self):
        self.current_player.reset_player_clock()
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def tick_timer(self):
        self.clock.tick_timer()
        self.current_player.tick_player_clock()

    def main_loop(self):
        # done outside the loop the first time to optimize performance
        # self.game_window.draw_board()
        # self.game_window.updateWindow()
        self.game_window.draw_time()
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
    game = Manager(board)
    game.start()
