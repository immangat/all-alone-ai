import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIPanel

from part_2.event_handler import EventHandler


class move_gui:
    MARGIN = 20

    def __init__(self, x_pixel: int, y_pixel: int, width: int, height: int, manager_ui=None, container=None):
        self.width = width
        self.height = height
        self.x_pixel = x_pixel
        self.y_pixel = y_pixel
        self.manager_ui = manager_ui
        self.move_gui_rect = pygame.Rect(x_pixel, y_pixel, width, height)
        # Use division to keep relative sizes
        self.top_rect = pygame.Rect(
            width//2 - width//4,  # x pixel
            height//30,          # y pixel
            width//2,             # width
            height//10            # height
        )
        self.button_rect = pygame.Rect(
            width//2 - width//4,
            height - height//8,
            width//2,
            height//10)
        self.container = container

    def create_gui(self):
        panel = UIPanel(relative_rect=self.move_gui_rect,
                        starting_height=1,
                        manager=self.manager_ui,
                        object_id="panel1")

        panel_top = UIPanel(relative_rect=self.top_rect,
                            starting_height=1,
                            margins={'left': 20, 'right': 20, 'top': 20, 'bottom': 20}, # this is like padding inside the panel
                            manager=self.manager_ui,
                            container=panel)

        UIButton(relative_rect=self.button_rect,
                 starting_height=2,
                 text='Hello',
                 manager=self.manager_ui,
                 container=panel)
