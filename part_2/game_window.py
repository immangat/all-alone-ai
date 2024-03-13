import math
import pygame
import pygame_gui
from part_2.event_handler import EventHandler
from part_2.move_gui import move_gui


class GameWindow:
    MOVE_GUI_WIDTH = 300
    MOVE_GUI_HEIGHT = 500
    MOVE_GUI_MARGIN = 10

    def __init__(self, width: int, height: int, manager=None):
        self.width = width
        self.height = height
        self.display_surface = None
        self.background = None
        self.manager = manager
        self.event_handler = EventHandler(self)
        self.marble_radius = 20  # Radius of the marbles
        self.highlighted_marbles = []  # Store the coordinates of the highlighted marble
        self.manager_ui = None
        self.type = "game"
        self.move_gui = move_gui(
            width - self.MOVE_GUI_WIDTH - self.MOVE_GUI_MARGIN,
            height // 2 - self.MOVE_GUI_HEIGHT // 2,
            self.MOVE_GUI_WIDTH,
            self.MOVE_GUI_HEIGHT,
            self.manager_ui,
            self.manager_ui
        )

    def initWindow(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.width, self.height))  # Create the window
        pygame.display.set_caption('Game Window')
        self.background = pygame.Surface((self.width, self.height))  # Create the background surface
        self.background.fill(pygame.Color(200, 200, 200))  # Fill the background with a color
        self.manager_ui = pygame_gui.UIManager((self.width, self.height), "gui_json/theme.json")
        self.move_gui.create_gui()

        # Here, you should also create your UI elements and pass the manager_ui to them

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

