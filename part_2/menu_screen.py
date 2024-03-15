import pygame
import pygame_gui
import pygame_menu
from pygame_gui.elements import UIButton
from functools import partial

from part_2.board import Board
from part_2.event_handler import EventHandler
from part_2.player import HumanPlayer


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
        self.human_player = HumanPlayer("Black", "b")

    def initWindow(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.width, self.height))  # Create the window
        pygame.display.set_caption('Menu Screen')
        self.background = pygame.Surface((self.width, self.height))  # Create the background surface
        self.background.fill(pygame.Color(200, 200, 200))  # Fill the background with a color
        # self.manager_ui = pygame_gui.UIManager((self.width, self.height), "gui_json/theme.json")
        self.menu = pygame_menu.Menu('All-Alone', self.width, self.height,
                                     theme=pygame_menu.themes.THEME_DEFAULT)

        title = self.menu.add.label("Game Settings:", padding=(0, 0, 15, 0))  # top, right, bottom, left
        selector_game_type = self.menu.add.dropselect(
            title='Game Type:',
            items=[('Human vs Human', 0),
                   ('Human vs AI', 1),
                   ('AI vs Human', 2)],
            font_size=20,
            selection_option_font_size=20,
            onchange=self.select_game_type,
            default=0,
            selection_box_height=5,
            selection_box_width=212,
            selection_color=(76, 0, 153)
        )

        # board_type_frame = self.menu.add.frame_h(width=600, height=200, padding=(0, 50, 0, 0))
        board_selector = self.menu.add.selector('Select Board Type:',
                                                [('Default', 1), ('German Daisy', 2), ('Belgian Daisy', 3)],
                                                onchange=self.select_board_type,
                                                font_size=20,
                                                style=pygame_menu.widgets.SELECTOR_STYLE_FANCY,
                                                selection_color=(76, 0, 153))
        # board_type_frame.pack(title_board, align=pygame_menu.locals.ALIGN_LEFT)
        # board_type_frame.pack(board_selector, align=pygame_menu.locals.ALIGN_RIGHT)
        # self.menu.add.label("Select Board Type:", padding=(15, 0, 15, 0))
        # self.menu.add.selector('',
        #                        [('Default', 1), ('German Daisy', 2), ('Belgian Daisy', 3)],
        #                        onchange=self.select_board_type)
        self.menu.add.label("Time Settings:", padding=(15, 0, 15, 0))
        self.menu.add.button('Select Total Move Limit', self.select_total_move_limit)
        self.menu.add.text_input('Select P1 Time Per Move ',
                                 default='60',
                                 maxchar=3,
                                 maxwidth=3,
                                 input_type=pygame_menu.locals.INPUT_INT,
                                 cursor_selection_enable=False,
                                 textinput_id='timer_p1',
                                 onchange=self.select_p1_time_per_move,
                                 selection_color=(76, 0, 153))
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
        self.menu.add.button('Quit', self.quit_game, background_color=(205, 92, 92))

        self.manager.board.setup_board("Default")

    def select_game_type(self, *args):
        print(f"select game type {args[1]}")
        if args[1] == 0:
            self.human_vs_human()
        elif args[1] == 1:
            self.human_vs_ai()
        elif args[1] == 2:
            self.ai_vs_human()

    def human_vs_human(self):
        print("human vs human")

    def human_vs_ai(self):
        # self.add_marble_options()
        print("human vs ai")

    def ai_vs_human(self):
        print("ai vs human")

    def select_board_type(self, selected: tuple, value: any):
        print("Board type selected")
        if selected[0][0] == "Default":
            print("Default board selected")
            self.manager.board.clear_board()
            self.manager.board.setup_default()
        elif selected[0][0] == "German Daisy":
            print("German Daisy board selected")
            self.manager.board.clear_board()
            self.manager.board.setup_german_daisy()
        elif selected[0][0] == "Belgian Daisy":
            print("Belgian Daisy board selected")
            self.manager.board.clear_board()
            self.manager.board.setup_belgian_daisy()
        # print(f"selected: {selected[0][0]} value: {value}")

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
