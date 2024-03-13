import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIPanel, UILabel

from part_2.event_handler import EventHandler


class move_gui:

    def __init__(self, x_pixel: int, y_pixel: int, width: int, height: int, manager_ui=None, container=None):
        self.width = width
        self.height = height
        self.x_pixel = x_pixel
        self.y_pixel = y_pixel
        self.manager_ui = manager_ui
        self.container = container
        self.move_gui_rect = pygame.Rect(x_pixel, y_pixel, width, height)
        # Use division to keep relative sizes
        self.top_rect = self.calc_relative_rect(x_proportion=0.49, y_proportion=0.1, width_proportion=0.75,
                                                height_proportion=0.1, parent=self.move_gui_rect)
        self.button_rect = self.calc_relative_rect(x_proportion=0.49, y_proportion=0.875, width_proportion=0.5,
                                                   height_proportion=0.1, parent=self.move_gui_rect)
        self.moves_container = self.calc_relative_rect(x_proportion=0.49, y_proportion=0.5, width_proportion=0.9,
                                                       height_proportion=0.6, parent=self.move_gui_rect)
        self.top_label = self.calc_relative_rect(x_proportion=0.49, y_proportion=0.5, width_proportion=1,
                                                 height_proportion=1, parent=self.top_rect)

    # Calculate the relative rect based on the parent rect and the proportions
    def calc_relative_rect(self, x_proportion, y_proportion, width_proportion, height_proportion, parent):
        # pixels are based on the center of the object
        x_pixel = parent.width * x_proportion - (parent.width * width_proportion / 2)
        y_pixel = parent.height * y_proportion - (parent.height * height_proportion / 2)
        width = parent.width * width_proportion
        height = parent.height * height_proportion
        return pygame.Rect(x_pixel, y_pixel, width, height)


    def create_gui(self):
        panel = UIPanel(relative_rect=self.move_gui_rect,
                        starting_height=1,
                        manager=self.manager_ui,
                        object_id="panel1")

        panel_top = UIPanel(relative_rect=self.top_rect,
                            starting_height=1,
                            # this is like padding inside the panel
                            manager=self.manager_ui,
                            container=panel)

        panel_moves = UIPanel(relative_rect=self.moves_container,
                              starting_height=1,
                              # this is like padding inside the panel
                              manager=self.manager_ui,
                              container=panel)

        ulabel = UILabel(relative_rect=self.top_label,
                         text='Moves made in game:',
                         manager=self.manager_ui,
                         container=panel_top)

        UIButton(relative_rect=self.button_rect,
                 starting_height=2,
                 text='Undo',
                 manager=self.manager_ui,
                 container=panel)
