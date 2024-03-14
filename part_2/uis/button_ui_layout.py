import pygame
from pygame_gui.elements import UIButton, UIPanel


class ButtonUI:

    def __init__(self, container, manager_ui=None):
        self.manager_ui = manager_ui
        self.container = container
        self.container_width = container.relative_rect.width
        self.container_height = container.relative_rect.height
        self.pause = None
        self.button_height = round(self.container_height * 0.5)
        self.button_width = round(self.container_width * 0.5)



    def create_gui(self):
        # panel = UIPanel(relative_rect=self.button_gui_rect,
        #                 starting_height=1,
        #                 manager=self.manager_ui,
        #                 object_id="buttons_panel")

        self.pause = UIButton(relative_rect=pygame.Rect(0, 0, self.button_width, self.button_height),
                              starting_height=2,
                              text='Pause',
                              manager=self.manager_ui,
                              container=self.container,
                              object_id="pause_button"

                              )
        # self.reset = UIButton(relative_rect=self.reset_button_rect,
        #                       starting_height=2,
        #                       text='Reset',
        #                       manager=self.manager_ui,
        #                       container=panel,
        #                       object_id="reset_button"
        #                       )
        # self.stop = UIButton(relative_rect=self.stop_button_rect,
        #                      starting_height=2,
        #                      text='Stop',
        #                      manager=self.manager_ui,
        #                      container=panel,
        #                      object_id="stop_button"
        #                      )
