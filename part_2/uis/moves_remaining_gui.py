import pygame
from pygame_gui.elements import UILabel


class MovesRemainingGUI:
    def __init__(self, manager_ui, container, manager):
        self.container = container
        self.container_width = container.relative_rect.width
        self.container_height = container.relative_rect.height
        self.manager_ui = manager_ui
        self.manager = manager
        self.ui_title = None
        self.ui_text = None

    def create_gui(self):
        self.ui_title = UILabel(relative_rect=pygame.Rect(0, 0, -1, -1),
                         text=' Moves Remaining: ',
                         manager=self.manager_ui,
                         container=self.container,
                         anchors={"centerx": "centerx", "top": "top"})

        self.ui_text = UILabel(
            relative_rect=pygame.Rect(0,-15,-1,-1),
            text="{}" .format(self.manager.total_move_limit),
            container=self.container,
            manager=self.manager_ui,
            object_id="moves_remaining_text",
            anchors={"centerx": "centerx", "top_target": self.ui_title})

    def update_gui(self):
        # Fetch the current number of moves remaining
        total_moves_left = self.manager.total_moves_left

        # Update the UILabel text with the new number of moves remaining
        self.ui_text.set_text("{}".format(total_moves_left))
