import tkinter as tk


class Button:
    def __init__(self, master, text, position, command=None, size=(100, 30), bg_color="white", fg_color="black", type="simple", options=None, default_option =""):
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
        self.options = options
        self.selected_option = None if self.options == None else tk.StringVar(value=default_option)
        if (type == "simple"):
            self.create_button()
        elif (type == "dropdown"):
            self.create_dropdown()


    def create_button(self):
        """Create and place the button widget."""
        self.button = tk.Button(self.master, text=self.text, command=self.command, bg=self.bg_color, fg=self.fg_color)
        self.button.place(x=self.position[0], y=self.position[1], width=self.size[0], height=self.size[1])

    def create_dropdown(self):
        # Use the selected_option variable for the OptionMenu
        self.button = tk.OptionMenu(self.master, self.selected_option, *self.options,
                                           command=self.update_button_text)
        self.button.place(x=self.position[0], y=self.position[1], width=self.size[0], height=self.size[1])

    def update_button_text(self, selected_option):
        self.selected_option.set(selected_option)
        self.button.config(text=f"{self.text}: {selected_option}")

    def get_selected_option(self):
        return self.selected_option.get()