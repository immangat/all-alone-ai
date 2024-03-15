import pygame
from pygame_gui.elements import UIButton, UIPanel, UILabel


class PlayerUi:
    def __init__(self, player_num, player, theme_string, container, manager_ui=None):
        self.container = container
        self.manager_ui = manager_ui
        self.container_width = container.relative_rect.width
        self.container_height = container.relative_rect.height
        self.player = player
        self.theme_string = theme_string
        self.player_num = player_num
        self.time_width = round(self.container_width * 0.2)

    def create_gui(self):
        player_1_info = UILabel(relative_rect=pygame.Rect(0, 0, -1, -1),
                                text='Player {}: {}'.format(self.player_num, self.player.name),
                                manager=self.manager_ui,
                                container=self.container,
                                object_id=self.theme_string,
                                anchors={"centery": "centery"})

        player_1_score = UILabel(relative_rect=pygame.Rect((0, 0, -1, -1)),
                                 text=' SCORE: {}'.format(self.player.score),
                                 manager=self.manager_ui,
                                 container=self.container,
                                 object_id=self.theme_string,
                                 anchors={"centery": "centery",
                                          "left": "left", "left_target": player_1_info})

        player_1_time = UILabel(relative_rect=pygame.Rect(-self.time_width, 0, -1, -1),
                                text='TIME: {} '.format(self.player.clock.current_time),
                                manager=self.manager_ui,
                                container=self.container,
                                object_id=self.theme_string,
                                anchors={'left': 'right', 'right': 'right', 'centery': 'centery'})

