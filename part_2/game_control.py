import pygame

from part_2.board import Board
from part_2.clock import Clock
from part_2.game_window import GameWindow
from part_2.player import Player, HumanPlayer
from part_2.states import States
from part_2.state_space_gen import StateSpaceGen
import copy


class Manager:
    __instance = None

    def __init__(self):
        if Manager.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            Manager.__instance = self
            self.game_window = GameWindow(1280, 720, self)  # This should be an instance of GameWindow class
            self.board_state = ''  # You would set this according to your game logic
            self.is_running = False
            self.board = None  # You would set this according to your game logic
            self.clock = Clock()
            self.players = [HumanPlayer("Black"), HumanPlayer("White")]
            self.current_player: Player = self.players[0]
            self.states = None

    @staticmethod
    def get_instance():
        if Manager.__instance is None:
            Manager()
        return Manager.__instance

    def start(self):
        self.is_running = True
        self.board = Board()
        # TODO: add a function to return setup config from UI
        self.board.setup_board("Belgian Daisy")
        self.states = States()
        self.states.create_initial_state(self.board)
        self.game_window.initWindow()
        self.main_loop()

    def is_game_over(self):
        return True if self.players[0].score == 6 or self.players[1].score == 6 else False


    def end_game(self):
        pass

    def pause_game(self):
        pass

    def validate_and_make_move(self, marbles, direction):
        gen = StateSpaceGen()
        board_move = gen.validate_move(self.board, marbles, direction)
        if board_move[1] is not None:
            self.board = board_move[1]
            self.states.add_state(board_move[1], board_move[0])
            self.switch_turns()
        else:
            pass
            #TODO: Feedback for invalid move????

    def switch_turns(self):
        self.current_player.reset_player_clock()
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]
        self.update_score()

    def undo_move(self):
        """
        Undoes the last move made in the game
        """

        deleted_state = self.states.remove_last_state()
        if deleted_state:
            last_state = self.states.get_last_state()
            self.board = copy.deepcopy(last_state.get_board())
            self.switch_turns()

    def update_score(self):
        white_score = self.board.num_marbles_left_by_color("b")
        black_score = self.board.num_marbles_right_by_color("w")
        self.players[0].update_score(black_score)
        self.players[1].update_score(white_score)

    def tick_timer(self):
        self.clock.tick_timer()
        self.current_player.tick_player_clock()

    def main_loop(self):
        clock = pygame.time.Clock()
        while self.is_running:
            time_delta = clock.tick(60) / 1000.0
            self.game_window.event_handler.handle_events()
            self.game_window.manager_ui.update(time_delta)
            self.game_window.updateWindow()  # Draw the board state


if __name__ == "__main__":
    game = Manager()
    game.start()
