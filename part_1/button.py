import tkinter as tk


class Button:
    def __init__(self, master, text, command, position, size=(100, 30), bg_color="white", fg_color="black"):
        """
        Initialize a new MyButton instance.

        :param master: The parent widget.
        :param text: The text on the button.
        :param command: The function to be called when the button is clicked.
        :param position: The position to place the button in the form of (x, y).
        :param size: The size of the button in the form of (width, height).
        :param bg_color: Background color of the button.
        :param fg_color: Foreground (text) color of the button.
        """
        self.master = master
        self.text = text
        self.command = command
        self.position = position
        self.size = size
        self.bg_color = bg_color
        self.fg_color = fg_color

        self.create_button()

    def create_button(self):
        """Create and place the button widget."""
        self.button = tk.Button(self.master, text=self.text, command=self.command, bg=self.bg_color, fg=self.fg_color)
        self.button.place(x=self.position[0], y=self.position[1], width=self.size[0], height=self.size[1])
