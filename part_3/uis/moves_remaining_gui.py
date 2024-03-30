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
        self.next_move_tile = None
        self.next_move = None

    def create_gui(self):
        self.ui_title = UILabel(relative_rect=pygame.Rect(-200, 0, -1, -1),
                                text=' Moves Remaining: ',
                                manager=self.manager_ui,
                                container=self.container,
                                anchors={"right": "right", "top": "top"})

        self.ui_text = UILabel(
            relative_rect=pygame.Rect(-40, 0, -1, -1),
            text="{}".format(self.manager.total_move_limit),
            container=self.container,
            manager=self.manager_ui,
            object_id="moves_remaining_text",
            anchors={"right": "right", "left_target": self.ui_title})
        self.next_move_tile = UILabel(relative_rect=pygame.Rect(10, 40, -1, -1),
                                      text='AI Move: ',
                                      manager=self.manager_ui,
                                      container=self.container,
                                      anchors={"left": "left", "top": "top"})
        self.next_move = UILabel(relative_rect=pygame.Rect(10, 40, -1, -1),
                                 text='{}'.format(self.manager.next_move),
                                 manager=self.manager_ui,
                                 container=self.container,
                                 anchors={"left_target": self.next_move_tile})

    def update_gui(self):
        # Fetch the current number of moves remaining
        total_moves_left = self.manager.total_moves_left
        next_move = self.manager.next_move
        self.next_move.set_text('{}'.format(self.manager.next_move))
        # Update the UILabel text with the new number of moves remaining
        self.ui_text.set_text("{}".format(total_moves_left))
