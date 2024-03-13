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
        self.event_handler = EventHandler(self)
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
        self.menu.add.button('Start', self.start_game)
        self.menu.add.button('Quit', self.quit_game)

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
