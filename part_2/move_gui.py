import pygame
import pygame_gui
from pygame_gui.elements import UIButton

from part_2.event_handler import EventHandler


class move_gui:
    def __init__(self, width: int, height: int, manager=None, ui_window=None):
        self.width = width
        self.height = height
        self.display_surface = pygame.display.set_mode((self.width, self.height))
        self.manager = manager
        self.ui_manager = pygame_gui.UIManager((self.width, self.height))
        self.event_handler = EventHandler(self)
        self.button_layout_rect = pygame.Rect(30, 20, 300, 500)
        self.ui_window = ui_window

    def draw_button(self):

        UIButton(relative_rect=self.button_layout_rect,
                 text='Hello',
                 manager=self.ui_manager,
                 container=self.ui_window)
        # pygame.draw.rect(self.display_surface, (224, 224, 224), self.button_layout_rect)
        # pygame.display.update(self.button_layout_rect)
