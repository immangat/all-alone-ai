import pygame
import pygame_gui
from pygame_gui.elements import UIButton

from part_2.event_handler import EventHandler


class move_gui:
    def __init__(self, x_pixel: int, y_pixel: int, width: int, height: int, manager_ui=None, container=None):
        self.width = width
        self.height = height
        self.x_pixel = x_pixel
        self.y_pixel = y_pixel
        self.manager_ui = manager_ui
        self.button_layout_rect = pygame.Rect(x_pixel, y_pixel, width, height)
        self.container = container

    def create_gui(self):
        UIButton(relative_rect=self.button_layout_rect,
                 text='Hello',
                 manager=self.manager_ui,
                 container=self.container)
