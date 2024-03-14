import pygame
from pygame_gui.elements import UIButton, UIPanel, UILabel, UITextBox


class move_gui:

    def __init__(self, x_pixel: int, y_pixel: int, width: int, height: int, manager_ui=None):
        self.move_buffer = None
        self.moves_made = ""
        self.move_count = 0
        self.width = width
        self.height = height
        self.x_pixel = x_pixel
        self.y_pixel = y_pixel
        self.manager_ui = manager_ui
        if self.manager_ui is None:
            raise ValueError("UIManager is not initialized.")
        self.undo_button = None
        self.add_button = None
        self.panel_moves = None
        self.moves_gui = None
        self.move_gui_rect = pygame.Rect(x_pixel, y_pixel, width, height)
        # Use division to keep relative sizes
        self.top_rect = self.calc_relative_rect(x_proportion=0.49, y_proportion=0.1, width_proportion=0.75,
                                                height_proportion=0.1, parent=self.move_gui_rect)
        self.button_rect = self.calc_relative_rect(x_proportion=0.24, y_proportion=0.875, width_proportion=0.3,
                                                   height_proportion=0.1, parent=self.move_gui_rect)
        self.button2_rect = self.calc_relative_rect(x_proportion=0.74, y_proportion=0.875, width_proportion=0.3,
                                                    height_proportion=0.1, parent=self.move_gui_rect)
        self.moves_container_rect = self.calc_relative_rect(x_proportion=0.49, y_proportion=0.5, width_proportion=0.9,
                                                            height_proportion=0.6, parent=self.move_gui_rect)
        self.moves_text_rect = self.calc_relative_rect(x_proportion=0.49, y_proportion=0.49, width_proportion=1,
                                                       height_proportion=1, parent=self.moves_container_rect)
        self.top_label_rect = self.calc_relative_rect(x_proportion=0.49, y_proportion=0.5, width_proportion=1,
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

        self.panel_moves = UIPanel(relative_rect=self.moves_container_rect,
                                   starting_height=1,
                                   # this is like padding inside the panel
                                   manager=self.manager_ui,
                                   container=panel)

        ulabel = UILabel(relative_rect=self.top_label_rect,
                         text='Moves made in game:',
                         manager=self.manager_ui,
                         container=panel_top)

        self.undo_button = UIButton(relative_rect=self.button_rect,
                                    starting_height=2,
                                    text='Undo',
                                    manager=self.manager_ui,
                                    container=panel)

        # self.add_button = UIButton(relative_rect=self.button2_rect,
        #                            starting_height=2,
        #                            text='add move',
        #                            manager=self.manager_ui,
        #                            container=panel)

        self.moves_gui = UITextBox(relative_rect=self.moves_text_rect,
                                   html_text=self.moves_made,
                                   manager=self.manager_ui,
                                   container=self.panel_moves)

    def add_move(self, move):
        formatted_move = str(move).ljust(3)  # Ensures move is left-aligned in 3 characters
        # Determine padding based on the length of the formatted move
        padding = " " * (20 - len(formatted_move))
        # Use string formatting to create a uniformly padded string
        move_entry = f"<pre>{formatted_move}{padding}<pre>"

        if self.move_count % 2 == 0:
            self.moves_made += move_entry
        else:
            # Complete the buffer with the formatted move
            self.moves_made += f"<p>{formatted_move}</p>"
        self.moves_gui.html_text = self.moves_made  # Update the html_text of the UITextBox
        self.moves_gui.rebuild()  # Rebuild the UITextBox to reflect the changes
        self.move_count += 1