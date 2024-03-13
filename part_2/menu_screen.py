import pygame
import pygame_gui


class MenuScreen:
    def __init__(self, width: int, height: int, manager_ui=None):
        self.width = width
        self.height = height
        self.manager_ui = manager_ui
        self.start_game_button = None
        self.time_select_input = None
        self.display_surface = None
        self.background = None

    def create_menu(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.width, self.height))  # Create the window
        pygame.display.set_caption('Menu Screen')
        self.background = pygame.Surface((self.width, self.height))  # Create the background surface
        self.background.fill(pygame.Color(200, 200, 200))  # Fill the background with a color
        self.manager_ui = pygame_gui.UIManager((self.width, self.height), "gui_json/theme.json")

        # Create the Start Game button
        self.start_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width / 2 - 100, self.height / 2 - 25), (200, 50)),
            text='Start Game',
            manager=self.manager_ui)

        # Create an input form for selecting time or other settings
        self.time_select_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.width / 2 - 100, self.height / 2 + 50), (200, 50)),
            manager=self.manager_ui)

    def handle_events(self, event):
        # Handle events like button clicks or text entry here
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_game_button:
                    print("Start Game button clicked!")
                    # Transition to the game screen here
