import math
import pygame
import pygame_gui

from part_2.uis.button_ui import ButtonUI
from part_2.uis.move_gui import move_gui

from part_2.event_handler import EventHandler, CUSTOM_TIMER_EVENT


class GameWindow:
    MOVE_GUI_WIDTH = 300
    MOVE_GUI_HEIGHT = 500
    MOVE_GUI_MARGIN = 10
    BUTTONS_GUI_WIDTH = 300
    BUTTONS_GUI_HEIGHT = 100
    BUTTONS_GUI_MARGIN = 10

    def __init__(self, width: int, height: int, manager=None):
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
        ## added grid
        self.COLUM_LINE_1 = round(width * 0.75)
        self.ROW_LINE_1 = round(height * 0.1)
        self.ROW_LINE_2 = round(height * 0.20)
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
        self.player_1_gui = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0,0), (self.COLUM_LINE_1, self.ROW_LINE_1)),
            manager=self.manager_ui,
            object_id="player_1")

        self.player_2_gui = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0,self.ROW_LINE_4), (self.COLUM_LINE_1, self.ROW_LINE_1)),
            manager=self.manager_ui,
            object_id="player_2")

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
        pygame.time.set_timer(CUSTOM_TIMER_EVENT, 16)

    def updateWindow(self):
        # This will update the contents of the entire display
        self.draw_board()
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
        self.draw_time()


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

    # Not implemented for now due to processing power losses
    # def load_marble_sprites(self):
    #
    #     empty_space_color = (127, 127, 127)  # Color for empty spaces
    #
    #     for row, col in self.manager.board.BOARD_COORD:
    #         color = self.manager.board.get_circle(row, col)
    #
    #         position = self.board_to_pixel((row, col))  # Convert board coords to pixel coords
    #
    #         # if color == 'b':
    #         #     black_marble_sprite = MySprite('assets/black_marble.png', position, (65, 65))
    #         #     self.sprites.add(black_marble_sprite)  # Add to the sprite group
    #         #
    #         # elif color == 'w':
    #         #     white_marble_sprite = MySprite('assets/marble_white.png', position, (50, 50))
    #         #     self.sprites.add(white_marble_sprite)  # Add to the sprite group
    #
    #         else:  # For empty spaces, draw a gray circle directly onto the board
    #             pygame.draw.circle(self.display_surface, empty_space_color, position, self.marble_radius)
    #     self.sprites.draw(self.display_surface)
    #     pygame.display.flip()  # Update the display after drawing the empty spaces
