import pygame
from pygame_gui.elements import UIButton, UIPanel, UILabel

from part_3.player import Player


class PlayerUi:
    def __init__(self, player_num, player, theme_string, container, manager_ui=None):
        self.container = container
        self.manager_ui = manager_ui
        self.container_width = container.relative_rect.width
        self.container_height = container.relative_rect.height
        self.player: Player = player
        self.theme_string = theme_string
        self.player_num = player_num
        self.time_width = round(self.container_width * 0.2)

    def create_gui(self):
        player_1_info = UILabel(relative_rect=pygame.Rect(0, 0, -1, -1),
                                text='P {}: {}'.format(self.player_num, self.player.name),
                                manager=self.manager_ui,
                                container=self.container,
                                object_id=self.theme_string,
                                anchors={"centery": "centery"})

        player_1_score = UILabel(relative_rect=pygame.Rect((0, 0, -1, -1)),
                                 text=' S: {}'.format(self.player.score or 0),
                                 manager=self.manager_ui,
                                 container=self.container,
                                 object_id=self.theme_string,
                                 anchors={"centery": "centery",
                                          "left": "left", "left_target": player_1_info})
        player_1_time = UILabel(relative_rect=pygame.Rect(60, 0, -1, -1),
                                text='T R: {:.2f} '.format(self.player.clock.current_time / 1000),
                                manager=self.manager_ui,
                                container=self.container,
                                object_id=self.theme_string,
                                anchors={'left': 'left', 'centery': 'centery', "left_target": player_1_score})

        player_1_total_time = UILabel(relative_rect=pygame.Rect(-10, 0, -1, -1),
                                      text='TOT T: {:.2f} '.format(self.player.get_aggregate_time() / 1000),
                                      manager=self.manager_ui,
                                      container=self.container,
                                      object_id=self.theme_string,
                                      anchors={'left': 'right', 'right': 'right', 'centery': 'centery'})

        player_1_total_time = UILabel(relative_rect=pygame.Rect(-190, 0, -1, -1),
                                      text='LM T: {:.2f} '.format(self.player.get_last_move_time() / 1000),
                                      manager=self.manager_ui,
                                      container=self.container,
                                      object_id=self.theme_string,
                                      anchors={'left': 'right', 'right': 'right', 'centery': 'centery'})
