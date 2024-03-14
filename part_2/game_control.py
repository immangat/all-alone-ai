import pygame

from part_2.board import Board
from part_2.clock import Clock
from part_2.game_window import GameWindow
from part_2.player import Player, HumanPlayer
from part_2.menu_screen import MenuScreen


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
            self.game_paused = False
            self.board = board  # You would set this according to your game logic
            self.clock = Clock()
            self.players = [HumanPlayer("White", "w"), HumanPlayer("Black", "b")]
            self.current_player: Player = self.players[0]
            self.current_screen = "game"
            self.menu_screen = MenuScreen(1280,
                                          720,
                                          self)

    @staticmethod
    def get_instance(game_window=None, board=None):
        if Manager.__instance is None:
            Manager(game_window, board)
        return Manager.__instance

    def start(self):
        if self.current_screen == "menu":
            self.menu_screen.initWindow()
            self.is_running = True
            self.main_loop()
        elif self.current_screen == "game":
            # print("game")
            self.game_window.initWindow()
            self.is_running = True
            self.main_loop()

    def end_game(self):
        pass

    def pause_game(self):
        print("Game pasued")
        self.game_paused = not self.game_paused

    def switch_turns(self):
        self.current_player.reset_player_clock()
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def tick_timer(self):
        self.clock.tick_timer()
        if not self.game_paused:
            self.current_player.tick_player_clock()

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
            if self.current_screen == "menu":  # we should probably create an abstact window class
                # print("menu loop")
                self.menu_screen.event_handler.handle_events()
                self.menu_screen.updateWindow()
            elif self.current_screen == "game":
                # print("game loop")
                self.game_window.event_handler.handle_events()
                self.game_window.manager_ui.update(time_delta)
                self.game_window.updateWindow()  # Draw the board state


if __name__ == "__main__":
    board = Board()
    board.setup_belgian_daisy()
    game = Manager(board)
    game.start()
