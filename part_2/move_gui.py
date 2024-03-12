import pygame
import pygame_gui
from pygame_gui.elements import UIButton

from part_2.event_handler import EventHandler


class move_gui:
    def __init__(self, width: int, height: int, manager_ui=None, container=None):
        self.width = width
        self.height = height
        self.display_surface = pygame.display.set_mode((self.width, self.height))
        self.manager_ui = manager_ui
        self.event_handler = EventHandler(self)
        self.button_layout_rect = pygame.Rect(30, 20, 300, 500)
        self.container = container

    def draw_button(self):

        UIButton(relative_rect=self.button_layout_rect,
                 text='Hello',
                 manager=self.manager_ui,
                 container=self.container)
        # pygame.draw.rect(self.display_surface, (224, 224, 224), self.button_layout_rect)
        # pygame.display.update(self.button_layout_rect)
