import math

import pygame

from part_2.event_handler import EventHandler
from part_2.sprite import MySprite


class GameWindow:
    def __init__(self, width: int, height: int, manager=None):
        self.width = width
        self.height = height
        self.display_surface = None
        self.sprites = pygame.sprite.Group()  # Group to hold all sprite objects
        self.manager = manager
        self.event_handler = EventHandler(self)
        self.marble_radius = 20  # Radius of the marbles
        self.highlighted_marbles = []  # Store the coordinates of the highlighted marble

    def initWindow(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Game Window')
        # self.loadSprites()

    def updateWindow(self):
        # This will update the contents of the entire display
        self.draw_board()
        # self.sprites.update()  # Update all the sprites in the group
        # self.sprites.draw(self.display_surface)  # Draw all the sprites in the group
        # pygame.draw.circle(self.display_surface, (0, 0, 0), (100, 100), 20)
        # pygame.display.flip()

    # def loadSprites(self):
    #     # Load the images as sprites
    #     black_marble_sprite = MySprite('assets/black_marble.png', (100, 100), (65, 65))
    #     white_marble_sprite = MySprite('assets/marble_white.png', (150, 150), (50, 50))
    #     self.sprites.add(black_marble_sprite, white_marble_sprite)  # Add them to the group

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
        self.display_surface.fill((200, 200, 200))
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
            pygame.draw.circle(self.display_surface, color, (x_pixel, y_pixel), self.marble_radius)
            print(self.highlighted_marbles)
            for marble in self.highlighted_marbles:
                if marble == (row, col):
                    pygame.draw.circle(self.display_surface, (255, 102, 102), (x_pixel, y_pixel),
                                       self.marble_radius + 2, 3)
        pygame.display.flip()

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
