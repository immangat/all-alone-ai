import time

import pygame

from board import Board
from clock import Clock
from game_window import GameWindow
from player import Player, HumanPlayer, AIPlayer, MangatAI, AIAgent
# from ais.mangat_ai import MangatAI
from menu_screen import MenuScreen
from states import States
from state_space_gen import StateSpaceGen
import copy


class Manager:
    """
    The central management class for the game.

    Attributes:
    - game_window (GameWindow): The game window instance.
    - board_state (str): The current state of the game board.
    - is_running (bool): Flag indicating if the game is running.
    - board (Board): The game board instance.
    - game_paused (bool): Flag indicating if the game is paused.
    - clock (Clock): The game clock instance.
    - players (list): List of Player instances (HumanPlayer or AIPlayer).
    - current_player (Player): The current player.
    - current_screen (str): The current screen of the game ("menu" or "game").
    - menu_screen (MenuScreen): The menu screen instance.
    - states (States): The game states instance.
    - gen (StateSpaceGen): The state space generator instance.
    - board_type (str): The type of game board.
    - total_move_limit (int): The total move limit for the game.
    - total_moves_left (int): The total moves left in the game.
    - time_limit_per_move_p1 (int): Time limit per move for player 1.
    - time_limit_per_move_p2 (int): Time limit per move for player 2.
    - next_move (str): The next move to be executed.
    - ai_move_start_time (int): The start time of the AI move.
    - ai_found_move (bool): Flag indicating if AI found a move.
    - first_move_done (bool): Flag indicating if the first move has been made.
    """
    __instance = None

    def __init__(self):
        if Manager.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            Manager.__instance = self
            pygame.init()
            self.game_window = GameWindow(1280, 720, self)  # This should be an instance of GameWindow class
            self.board_state = ''  # You would set this according to your game logic
            self.is_running = False
            self.board = None  # You would set this according to your game logic
            self.game_paused = False
            self.board = None  # You would set this according to your game logic
            self.clock = Clock()
            self.players = [HumanPlayer("Black", "b"), HumanPlayer("White", "w")]
            self.current_player: Player = self.players[0]
            self.current_screen = "menu"
            self.menu_screen = MenuScreen(1280,
                                          720,
                                          self)
            self.states = None
            self.gen = StateSpaceGen()
            self.board_type = "German Daisy"  # set to a value for testing purposes without menu
            # added here because no game class
            self.total_move_limit = None
            self.total_moves_left = None
            self.time_limit_per_move_p1 = None
            self.time_limit_per_move_p2 = None
            self.next_move = None
            self.ai_move_start_time = None
            self.ai_found_move = None
            self.first_move_done = False

    @staticmethod
    def get_instance():
        if Manager.__instance is None:
            Manager()
        return Manager.__instance

    def start(self):
        self.board = Board()
        self.board.setup_board("German Daisy")  # This is only a placeholder for testing without the menu
        self.states = States()
        self.states.create_initial_state(self.board)
        if self.current_screen == "menu":
            print("menu")
            self.menu_screen.initWindow()
            self.is_running = True
            self.main_loop()
        elif self.current_screen == "game":
            self.game_window.initWindow()
            self.is_running = True
            self.main_loop()

    def is_game_over(self):
        return True if self.players[0].score == 6 or self.players[1].score == 6 or self.total_moves_left == 0 else False

    def end_game(self):
        pass

    def pause_game(self):
        print("Game paused")
        self.game_paused = not self.game_paused
        pass

    def reset_game(self):
        print("Game reset")
        self.clock.reset_timer()
        self.players[0].reset_player_clock()
        self.players[1].reset_player_clock()
        self.players[0].reset_player()
        self.players[1].reset_player()
        self.next_move = None
        self.ai_found_move = None
        self.current_player = self.players[0]
        self.states.clear_states()
        self.board.clear_board()
        self.board.setup_board(self.board_type)
        self.states.create_initial_state(self.board)
        self.game_window.initWindow()

    def stop_game(self):
        print("Game stop")
        self.clock.reset_timer()
        self.players[0].reset_player()
        self.players[1].reset_player()
        self.current_player = self.players[0]
        self.states.clear_states()
        self.board.clear_board()
        self.states.create_initial_state(self.board)
        self.switch_to_screen("menu")

    def store_move_history(self):
        last_move = self.states.get_states()[-1].get_move()
        self.game_window.move_gui.add_move(last_move)
        self.game_window.move_gui.moves_gui.rebuild()

    def validate_and_make_move(self, marbles, direction):
        self.gen = StateSpaceGen()
        move_board = self.gen.validate_move(self.board, marbles, direction)
        new_board = Board()
        new_board.set_circles(move_board[1])
        if move_board[1] is not None:
            self.board = new_board
            self.states.add_state(move_board[0], new_board)
            print(self.states.get_states()[-1].get_move())
            self.store_move_history()
            self.switch_turns()
            self.decrement_moves_remaining()
            self.game_window.moves_left.update_gui()
            self.game_window.move_gui.moves_gui.rebuild()
            self.board.get_marbles_by_color(self.current_player.color)

        else:
            pass
            # TODO: Feedback for invalid move????

    def switch_turns(self):
        self.current_player.reset_player_clock()
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]
        self.ask_for_move()
        self.update_score()

    def switch_turns_for_undo(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]
        self.ask_for_move()
        self.update_score()

    def undo_move(self):
        """
        Undoes the last move made in the game
        """
        current_state = self.states.get_last_state()
        self.states.remove_last_state()
        last_state = self.states.get_last_state()
        if current_state != last_state:
            self.current_player.reset_player_clock(undo=True)
            self.game_window.move_gui.remove_last_move()
            self.increment_moves_remaining()
            self.game_window.moves_left.update_gui()
            self.board = copy.deepcopy(last_state.get_board())
            self.switch_turns_for_undo()
            self.current_player.undo_move()

    def ask_for_move(self):
        current_player = self.current_player.__str__()
        print("current", current_player)

        if isinstance(self.current_player, AIPlayer):
            print("Current Player", self.current_player)
            self.next_move = "Searching"
            self.ai_found_move = False
            self.ai_move_start_time = time.time_ns()
            self.game_window.moves_left.update_gui()
        self.current_player.make_move(board=self.board)

    def update_score(self):
        white_score = self.board.num_marbles_left_by_color("b")
        black_score = self.board.num_marbles_left_by_color("w")
        self.players[0].update_score(black_score)
        self.players[1].update_score(white_score)

    def tick_timer(self):
        self.clock.tick_timer()
        if not self.game_paused:
            self.current_player.tick_player_clock()

    def switch_to_screen(self, screen_name):
        """Switches the current screen to the given screen name."""
        self.current_screen = screen_name
        # self.start()
        if screen_name == "menu":
            self.menu_screen.initWindow()
            self.main_loop()
        elif screen_name == "game":
            self.players[0].set_time_limit_per_move(self.time_limit_per_move_p1 * 1000)
            self.players[1].set_time_limit_per_move(self.time_limit_per_move_p2 * 1000)
            self.is_running = True
            self.game_window.initWindow()
            self.ask_for_move()
            self.main_loop()

    def configure_player(self, player_color, player_type):
        if player_color == 'b':
            if player_type == 'h':
                self.players[0] = HumanPlayer("Black", "b")
            if player_type == 'a':
                self.players[0] = AIAgent("Black", "b")
        if player_color == 'w':
            if player_type == 'h':
                self.players[1] = HumanPlayer("White", "w")
            if player_type == 'a':
                self.players[1] = AIAgent("White", "w")
        self.current_player = self.players[0]

    def increment_moves_remaining(self):
        self.total_moves_left = self.total_moves_left + 1

    def decrement_moves_remaining(self):
        self.total_moves_left = self.total_moves_left - 1

    def check_for_ai_player_move(self):
        if not self.first_move_done and self.current_player.color != "w":
            move, time_for_ai_move = self.current_player.get_first_random_move(self.board, self.ai_move_start_time)
            self.current_player.add_ai_time(time_for_ai_move)
            self.ai_found_move = True
            self.next_move = move
            self.game_window.moves_left.update_gui()
            self.first_move_done = True
        else:
            self.first_move_done = True
        if self.ai_found_move:
            return
        print("thread alive>>>", self.current_player.ai_search_process.is_alive())
        if ((((time.time_ns() - self.ai_move_start_time) / 1_000_000 >= self.current_player.time_per_move) or
             not self.current_player.ai_search_process.is_alive())):
            # self.current_player.ai_search_process.terminate()
            if self.current_player.queue.empty() and not self.ai_found_move:
                self.next_move = "AI couldn't find a move"
                self.game_window.moves_left.update_gui()
                return
            move, time_for_ai_move = self.current_player.get_last_item_and_empty()
            self.current_player.add_ai_time(time_for_ai_move)
            self.ai_found_move = True
            self.next_move = move
            self.game_window.moves_left.update_gui()
            self.current_player.ai_search_process.join(timeout=1)

    def main_loop(self):

        clock = pygame.time.Clock()
        while self.is_running:
            time_delta = clock.tick(60) / 1000.0
            if self.current_screen == "menu":  # we should probably create an abstact window class
                # print("menu loop")
                self.menu_screen.event_handler.handle_events()
                self.menu_screen.updateWindow()
            elif self.current_screen == "game":
                if isinstance(self.current_player, AIPlayer):
                    self.check_for_ai_player_move()
                self.game_window.event_handler.handle_events()
                self.game_window.manager_ui.update(time_delta)
                self.game_window.updateWindow()  # Draw the board state


if __name__ == "__main__":
    game = Manager()
    game.start()
