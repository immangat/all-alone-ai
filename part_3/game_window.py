import math
import pygame
import pygame_gui

from uis.button_ui import ButtonUI
from uis.move_gui import move_gui

from event_handler import EventHandler, CUSTOM_TIMER_EVENT
from uis.player_ui_layout import PlayerUi
from uis.moves_remaining_gui import MovesRemainingGUI

RED = (255, 0, 0)


class GameWindow:
    """
        The game window class responsible for managing the game window and UI elements.

        Attributes:
        - MOVE_GUI_WIDTH (int): Width of the move GUI.
        - MOVE_GUI_HEIGHT (int): Height of the move GUI.
        - MOVE_GUI_MARGIN (int): Margin of the move GUI.
        - BUTTONS_GUI_WIDTH (int): Width of the buttons GUI.
        - BUTTONS_GUI_HEIGHT (int): Height of the buttons GUI.
        - BUTTONS_GUI_MARGIN (int): Margin of the buttons GUI.
        - width (int): Width of the game window.
        - height (int): Height of the game window.
        - display_surface (pygame.Surface): The display surface of the game window.
        - background (pygame.Surface): The background surface of the game window.
        - manager (Manager): The game manager instance.
        - event_handler (EventHandler): The event handler instance.
        - marble_radius (int): Radius of the marbles.
        - highlighted_marbles (list): List of coordinates of highlighted marbles.
        - manager_ui (pygame_gui.UIManager): The UI manager for pygame_gui.
        - type (str): The type of the game window ("game" or "menu").
        - clock (pygame.time.Clock): The game clock instance.
        - player_1_gui (PlayerUi): The player 1 UI instance.
        - player_2_gui (PlayerUi): The player 2 UI instance.
        - COLUM_LINE_1 (int): Column line 1 position for grid layout.
        - ROW_LINE_1 (int): Row line 1 position for grid layout.
        - ROW_LINE_2 (int): Row line 2 position for grid layout.
        - ROW_LINE_3 (int): Row line 3 position for grid layout.
        - ROW_LINE_4 (int): Row line 4 position for grid layout.
        """
    MOVE_GUI_WIDTH = 300
    MOVE_GUI_HEIGHT = 500
    MOVE_GUI_MARGIN = 10
    BUTTONS_GUI_WIDTH = 300
    BUTTONS_GUI_HEIGHT = 100
    BUTTONS_GUI_MARGIN = 10

    def __init__(self, width: int, height: int, manager=None):
        self.moves_left = None
        self.button_gui = None
        self.move_gui = None
        self.width = width
        self.height = height
        self.display_surface = None
        self.background = None
        self.manager = manager
        self.event_handler = EventHandler(self, manager)
        self.marble_radius = 20  # Radius of the marbles
        self.highlighted_marbles = []  # Store the coordinates of the highlighted marble
        self.manager_ui = None
        self.type = "game"
        self.clock = pygame.time.Clock()
        self.player_1_gui = None
        self.player_2_gui = None
        ## added grid
        self.COLUM_LINE_1 = round(width * 0.75)
        self.ROW_LINE_1 = round(height * 0.1)
        self.ROW_LINE_2 = round(height * 0.15)
        self.ROW_LINE_3 = round(height * 0.85)
        self.ROW_LINE_4 = round(height * 0.9)

    def initWindow(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.width, self.height))  # Create the window
        pygame.display.set_caption('Game Window')
        self.background = pygame.Surface((self.width, self.height))  # Create the background surface
        self.background.fill(pygame.Color(200, 200, 200))  # Fill the background with a color
        self.manager_ui = pygame_gui.UIManager((self.width, self.height), "gui_json/theme.json")

        # UI panels defined below
        player_1_gui = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, self.ROW_LINE_4), (self.COLUM_LINE_1, self.ROW_LINE_1)),
            manager=self.manager_ui,
            object_id="player_1")

        player_2_gui = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (self.COLUM_LINE_1, self.ROW_LINE_1)),
            manager=self.manager_ui,
            object_id="player_2")

        turn_remaining_gui = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.COLUM_LINE_1, 0), (self.width - self.COLUM_LINE_1, self.ROW_LINE_2)),
            manager=self.manager_ui,
            object_id="turns_remaining")

        # buttons_gui_window = pygame_gui.elements.UIPanel(
        #     relative_rect=pygame.Rect((self.COLUM_LINE_1, self.ROW_LINE_3), (self.width - self.COLUM_LINE_1, self.height - self.ROW_LINE_3)))

        self.move_gui = move_gui(
            self.width - self.MOVE_GUI_WIDTH - self.MOVE_GUI_MARGIN,
            self.height // 2 - self.MOVE_GUI_HEIGHT // 2,
            self.MOVE_GUI_WIDTH,
            self.MOVE_GUI_HEIGHT,
            self.manager_ui
        )
        self.button_gui = ButtonUI(
            self.width - self.BUTTONS_GUI_WIDTH - self.BUTTONS_GUI_MARGIN,
            self.height - self.BUTTONS_GUI_WIDTH // 3,
            self.BUTTONS_GUI_WIDTH,
            self.BUTTONS_GUI_HEIGHT,
            self.manager_ui
        )
        self.move_gui.create_gui()
        self.button_gui.create_gui()
        # Here, you should also create your UI elements and pass the manager_ui to them

        # Create and add elements to guis
        self.player_1_gui = PlayerUi(1, self.manager.players[0], "player_1", player_1_gui, self.manager_ui)
        self.player_1_gui.create_gui()

        # Create and add player2 elements to player2 container
        self.player_2_gui = PlayerUi(2, self.manager.players[1], "player_2", player_2_gui, self.manager_ui)
        self.player_2_gui.create_gui()

        # Create and add turn indicator elements to moves remaining container
        self.moves_left = MovesRemainingGUI(self.manager_ui, turn_remaining_gui, self.manager)
        self.moves_left.create_gui()

        pygame.time.set_timer(CUSTOM_TIMER_EVENT, 333)

    def update_player_ui(self):
        self.player_2_gui.create_gui()
        self.player_1_gui.create_gui()

    def updateWindow(self):
        # This will update the contents of the entire display
        self.draw_board()
        self.update_player_ui()
        self.manager_ui.draw_ui(self.background)  # Draws any ui using pygame_gui
        pygame.display.flip()  # Update the display
        self.display_surface.blit(self.background, (0, 0))  # Draw the background on the display aka window

    def board_to_pixel(self, coord):
        # Assuming you have a method that converts board coordinates to pixel coordinates
        row, col = coord
        # start_x = self.width // 2  # Center the board on the canvas
        x_spacing = int(self.marble_radius * 2.5)  # Horizontal spacing between marbles
        y_spacing = int(self.marble_radius * math.sqrt(5))  # Vertical spacing between marbles
        max_row = 9  # Maximum row number
        max_col = 9  # Maximum column number
        total_board_width = x_spacing * (max_col - 1) + self.marble_radius * 2
        start_x = total_board_width // 2  # This left aligns a specific x,y coordinate according to the board
        start_y = 50
        x_offset = (row - 1) * x_spacing // 2
        x_pixel = start_x + (col - 3) * x_spacing - x_offset
        y_pixel = start_y + (max_row - row + 2) * y_spacing
        return x_pixel, y_pixel

    def get_board_tuples(self):
        # Assuming you have a method that returns all the board coordinates
        return self.manager.board.BOARD_COORD

    @staticmethod
    def is_within_circle(point, circle_center, radius):
        # Determine if a point is inside a circle
        px, py = point
        cx, cy = circle_center
        return (px - cx) ** 2 + (py - cy) ** 2 <= radius ** 2

    def draw_board(self):
        self.background.fill((200, 200, 200))
        # Iterate through all board coordinates and draw marbles
        for row, col in self.manager.board.BOARD_COORD:
            x_pixel, y_pixel = self.board_to_pixel((row, col))
            color = self.manager.board.get_circle(row, col)
            # Define the color based on the marble color, assuming 'b' for black, 'w' for white
            if color == 'b':
                color = (0, 0, 0)
            elif color == 'w':
                color = (255, 255, 255)
            else:
                color = (181, 154, 126)  # A neutral color for empty spaces

            # Draw the marble on the board
            pygame.draw.circle(self.background, color, (x_pixel, y_pixel), self.marble_radius)
            # print(self.highlighted_marbles)
            for marble in self.highlighted_marbles:
                if marble == (row, col):
                    pygame.draw.circle(self.background, (255, 102, 102), (x_pixel, y_pixel),
                                       self.marble_radius + 3, 3)
            # Draw cordinates now board
            font = pygame.font.SysFont(None, 24)  # Use default font with size 24
            label = font.render(f"{chr(row + 64)}{col}", True, RED)  # Render label text
            label_rect = label.get_rect(center=(x_pixel, y_pixel))  # Position label at center of circle
            self.display_surface.blit(label, label_rect)

    def draw_labels(self):
        pass

    # self.draw_time()

    def draw_time(self):
        font = pygame.font.SysFont(None, 30)
        text = font.render(str("{}:{:.1f} {}:{:.1f} board:{:.1f}".format(self.manager.players[0].name,
                                                                         self.manager.players[
                                                                             0].clock.current_time / 1000,
                                                                         self.manager.players[1].name,
                                                                         self.manager.players[
                                                                             1].clock.current_time / 1000,
                                                                         self.manager.clock.current_time / 1000)), True,
                           (0, 0, 0))
        self.display_surface.blit(text, (0, 0))
        pygame.display.update((0, 0, text.get_width() + 10, text.get_height() + 1))
