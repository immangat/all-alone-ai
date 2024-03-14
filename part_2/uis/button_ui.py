import pygame
from pygame_gui.elements import UIButton, UIPanel


class ButtonUI:

    def __init__(self, x_pixel: int, y_pixel: int, width: int, height: int, manager_ui=None, container=None):
        self.width = width
        self.height = height
        self.x_pixel = x_pixel
        self.y_pixel = y_pixel
        self.manager_ui = manager_ui
        self.container = container
        self.pause = None
        self.reset = None
        self.stop = None
        self.button_gui_rect = pygame.Rect(x_pixel, y_pixel, width, height)
        self.stop_button_rect = self.calc_relative_rect(x_proportion=0.24, y_proportion=0.7, width_proportion=0.3,
                                                        height_proportion=0.4, parent=self.button_gui_rect)
        self.reset_button_rect = self.calc_relative_rect(x_proportion=0.74, y_proportion=0.7, width_proportion=0.3,
                                                         height_proportion=0.4, parent=self.button_gui_rect)
        self.pause_button_rect = self.calc_relative_rect(x_proportion=0.49, y_proportion=0.2, width_proportion=0.3,
                                                         height_proportion=0.4, parent=self.button_gui_rect
                                                         )

    def calc_relative_rect(self, x_proportion, y_proportion, width_proportion, height_proportion, parent):
        # pixels are based on the center of the object
        x_pixel = parent.width * x_proportion - (parent.width * width_proportion / 2)
        y_pixel = parent.height * y_proportion - (parent.height * height_proportion / 2)
        width = parent.width * width_proportion
        height = parent.height * height_proportion
        return pygame.Rect(x_pixel, y_pixel, width, height)

    def create_gui(self):
        panel = UIPanel(relative_rect=self.button_gui_rect,
                        starting_height=1,
                        manager=self.manager_ui,
                        object_id="buttons_panel")

        self.pause = UIButton(relative_rect=self.pause_button_rect,
                              starting_height=2,
                              text='Pause',
                              manager=self.manager_ui,
                              container=panel,
                              object_id="pause_button"

                              )
        self.reset = UIButton(relative_rect=self.reset_button_rect,
                              starting_height=2,
                              text='Reset',
                              manager=self.manager_ui,
                              container=panel,
                              object_id="reset_button"
                              )
        self.stop = UIButton(relative_rect=self.stop_button_rect,
                             starting_height=2,
                             text='Stop',
                             manager=self.manager_ui,
                             container=panel,
                             object_id="stop_button"
                             )
