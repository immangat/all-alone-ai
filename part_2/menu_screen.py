import pygame
import pygame_gui
import pygame_menu
from pygame_gui.elements import UIButton

from part_2.event_handler import EventHandler


class MenuScreen:
    def __init__(self, width: int, height: int, manager):
        self.width = width
        self.height = height
        # self.manager_ui = None
        self.start_game_button = None
        self.time_select_input = None
        self.display_surface = None
        self.background = None
        self.menu = None
        self.manager = manager
        self.event_handler = EventHandler(self, manager)
        self.type = "menu"

    def initWindow(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.width, self.height))  # Create the window
        pygame.display.set_caption('Menu Screen')
        self.background = pygame.Surface((self.width, self.height))  # Create the background surface
        self.background.fill(pygame.Color(200, 200, 200))  # Fill the background with a color
        # self.manager_ui = pygame_gui.UIManager((self.width, self.height), "gui_json/theme.json")
        self.menu = pygame_menu.Menu('All-Alone', self.width, self.height,
                                     theme=pygame_menu.themes.THEME_DEFAULT)

        self.menu.add.label("Game Settings:", padding=(0, 0, 15, 0)) # top, right, bottom, left
        self.menu.add.button('Play against Human', self.play_against_human)
        self.menu.add.button('Play against AI', self.play_against_ai)
        self.menu.add.label("Marble Settings:")
        self.menu.add.button('White Marble', self.select_white_marble)
        self.menu.add.button('Black Marble', self.select_black_marble)
        self.menu.add.button('Random Marble', self.select_random_marble)
        self.menu.add.label("Select Board Type:", padding=(15, 0, 15, 0))
        self.menu.add.selector('',
                               [('Default', 1), ('German Daisy', 2), ('Belgian Daisy', 3)],
                               onchange= self.select_board_type)
        self.menu.add.label("Time Settings:", padding=(15, 0, 15, 0))
        self.menu.add.button('Select Total Move Limit', self.select_total_move_limit)
        self.menu.add.text_input('Select P1 Time Per Move ',
                                 default='60',
                                 maxchar=3,
                                 maxwidth=3,
                                 input_type=pygame_menu.locals.INPUT_INT,
                                 cursor_selection_enable=False,
                                 textinput_id='timer_p1',
                                 onchange=self.select_p1_time_per_move)
        self.menu.add.text_input('Select P2 Time Per Move ',
                                 default='60',
                                 maxchar=3,
                                 maxwidth=3,
                                 input_type=pygame_menu.locals.INPUT_INT,
                                 cursor_selection_enable=False,
                                 textinput_id='timer_p2',
                                 onchange=self.select_p2_time_per_move)
        self.menu.add.button('Board Testing', self.select_total_move_limit)

        self.menu.add.button('Start', self.start_game)
        self.menu.add.button('Quit', self.quit_game)





    def play_against_human(self):
        print("Play against human")

    def play_against_ai(self):
        print("Play against AI")

    def select_white_marble(self):
        print("White marble selected")

    def select_black_marble(self):
        print("Black marble selected")

    def select_random_marble(self):
        print("Random marble selected")

    def select_board_type(self, selected: tuple, value: any):
        print("Board type selected")
        print(f"selected: {selected[0]} value: {value}")

    def select_total_move_limit(self):
        print("Total move limit selected")

    def select_p1_time_per_move(self, *args):
        print(f"P1 time per move selected {args[0]}")

    def select_p2_time_per_move(self, *args):
        print(f"P2 time per move selected {args[0]}")

    def start_game(self):
        print("Game started")
        self.manager.switch_to_screen("game")

    def quit_game(self):
        # Exit the program
        pygame.quit()


    def updateWindow(self):
        # self.manager_ui.draw_ui(self.background)
        self.menu.draw(self.background)
        pygame.display.flip()
        self.display_surface.blit(self.background, (0, 0))
