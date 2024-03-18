import math

import pygame
import pygame_gui
from pygame_gui.elements import UILabel, UIImage, UIPanel, UIButton
from part_2 import player
from part_2.player import AIPlayer, HumanPlayer
from part_2.uis.button_ui_layout import ButtonUI
from part_2.game_control import Manager
from part_2.board import Board
from part_2.uis.player_ui_layout import PlayerUi
from part_2.uis.move_gui_layout import MoveGui


# class BoardUi:
#     def __init__(self, container, manager):
#         self.board = Board()
#         self.board.setup_default()
#         self.container = container
#         self.container_width = container.relative_rect.width
#         self.container_height = container.relative_rect.height
#         self.marble_radius = self.container_width / 20
#         self.background = None
#         self.manager = manager
#         self.highlighted_marbles = []  # Store the coordinates of the highlighted marble
#         self.background = pygame.Surface((self.container_width, self.container_height))
#
#     def draw_board(self):
#         self.background.fill((200, 200, 200))
#         # Iterate through all board coordinates and draw marbles
#         for row, col in self.board.BOARD_COORD:
#             x_pixel, y_pixel = self.board_to_pixel((row, col))
#             color = self.board.get_circle(row, col)
#             # Define the color based on the marble color, assuming 'b' for black, 'w' for white
#             if color == 'b':
#                 color = (0, 0, 0)
#             elif color == 'w':
#                 color = (255, 255, 255)
#             else:
#                 color = (181, 154, 126)  # A neutral color for empty spaces
#
#             # Draw the marble on the board
#             pygame.draw.circle(self.background, color, (x_pixel, y_pixel), self.marble_radius)
#             # print(self.highlighted_marbles)
#             for marble in self.highlighted_marbles:
#                 if marble == (row, col):
#                     pygame.draw.circle(self.background, (255, 102, 102), (x_pixel, y_pixel),
#                                        self.marble_radius + 3, 3)
#         # see if blit works
#         self.container.blit(self.background, (0, 0))
#     def board_to_pixel(self, coord):
#         # Assuming you have a method that converts board coordinates to pixel coordinates
#         row, col = coord
#         # start_x = self.width // 2  # Center the board on the canvas
#         x_spacing = int(self.marble_radius * 2.5)  # Horizontal spacing between marbles
#         y_spacing = int(self.marble_radius * math.sqrt(5))  # Vertical spacing between marbles
#         max_row = 9  # Maximum row number
#         max_col = 9  # Maximum column number
#         total_board_width = x_spacing * (max_col - 1) + self.marble_radius * 2
#         start_x = total_board_width // 2  # This left aligns a specific x,y coordinate according to the board
#         start_y = 50
#         x_offset = (row - 1) * x_spacing // 2
#         x_pixel = start_x + (col - 3) * x_spacing - x_offset
#         y_pixel = start_y + (max_row - row + 2) * y_spacing
#         return x_pixel, y_pixel
#
#     def get_board_tuples(self):
#         # Assuming you have a method that returns all the board coordinates
#         return self.board.BOARD_COORD



## making players for testing
ai_player = AIPlayer(name="AI Nico", color="Red")
human_player = HumanPlayer(name="Human Manhgott", color="Blue")


pygame.init()

#constants
display_info = pygame.display.Info()
WINDOW_WIDTH = display_info.current_w
WINDOW_HEIGHT = display_info.current_h
COLUM_LINE_1 = round(WINDOW_WIDTH * 0.75)
ROW_LINE_1 = round(WINDOW_HEIGHT * 0.1)
ROW_LINE_2 = round(WINDOW_HEIGHT * 0.20)
ROW_LINE_3 = round(WINDOW_HEIGHT * 0.85)
ROW_LINE_4 = round(WINDOW_HEIGHT * 0.9)
# Set the size of the pygame window
window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Dynamic Layout Example")

# Clock to control the frame rate
clock = pygame.time.Clock()

# UIManager to manage UI elements
manager = pygame_gui.UIManager(window_size, "gui_json/theme.json")

# Define a UI containers
# commented out, abalone game might not function well as a gui element, trying to keep Nico draw logic,
# Attempting to restructure . blit surface transfer to selected grid area
# abalone_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, ROW_LINE_1), (COLUM_LINE_1, ROW_LINE_4 - ROW_LINE_1)),
#                                              manager=manager)

abalone_surface = pygame.Surface((0,0),0)

player_1_hud_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), (COLUM_LINE_1, ROW_LINE_1)),
                                                  manager=manager,
                                                  object_id="player_1")

player_2_hud_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,ROW_LINE_4), (COLUM_LINE_1, ROW_LINE_1)),
                                                  manager=manager,
                                                  object_id="player_2")

clock_image_1 = pygame.image.load('assets/clock1.png')


turn_remaining_window = pygame_gui.elements.UIPanel(relative_rect= pygame.Rect((COLUM_LINE_1, 0), (WINDOW_WIDTH - COLUM_LINE_1, ROW_LINE_2)))

moves_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((COLUM_LINE_1, ROW_LINE_2), (WINDOW_WIDTH - COLUM_LINE_1, ROW_LINE_3 - ROW_LINE_2)),
                                           manager=manager,
                                           object_id="panel1")

buttons_gui_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((COLUM_LINE_1, ROW_LINE_3), (WINDOW_WIDTH - COLUM_LINE_1, WINDOW_HEIGHT- ROW_LINE_3)))

# Create and add player elements to player1 gui
player1 = PlayerUi(1, human_player, "player_1", player_1_hud_window, manager)
player1.create_gui()

# Create and add player2 elements to player2 container
player2 = PlayerUi(2, ai_player, "player_2", player_2_hud_window, manager)
player2.create_gui()

# create and add buttons to  buttons gui
buttons_gui = ButtonUI(buttons_gui_window, manager)
buttons_gui.create_gui()

# create and add elements to move gui
move_gui = MoveGui(moves_window, manager)
move_gui.create_gui()


# player_1_clock = UIImage(relative_rect=pygame.Rect(0, 0, 25, 25),
#                          manager=manager,
#                          container=player_1_hud_window,
#                          image_surface=clock_image_1)


# player_1_clock_label = UILabel(relative_rect=pygame.)

# make board
# board_ui = BoardUi(abalone_surface, manager)

running = True
while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pass the event to the UIManager
        manager.process_events(event)

    # Update UIManager
    manager.update(time_delta)

    # Clear the screen to black (or any other color)
    screen.fill((0, 0, 0))

    # Draw UI elements
    manager.draw_ui(screen)

    # print players times to console as a test
    print(human_player.clock.current_time)
    human_player.clock.tick_timer()
    ai_player.clock.tick_timer()

    #updates the clockuilabel with current time
    # player_1_time.set_text(' TIME: {:.2f}'.format(human_player.clock.current_time))
    # above logic needs to be moved else where, as human ui is in seperate class now
    # board_ui.draw_board()

    # Update the display
    pygame.display.flip()

pygame.quit()







