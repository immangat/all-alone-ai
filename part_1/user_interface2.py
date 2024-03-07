import math
import time
import tkinter as tk

from button import Button


class Displayer:
    """
    Display the user interface on the screen using Tkinter
    """
    def __init__(self, manager=None):
        """
        Initialize the display object
        :param manager: is the game manager object
        """
        self.selected_circles = []
        self.window = tk.Tk()
        self.window.title("Abalone Game")
        self.canvas = tk.Canvas(self.window, width=800, height=700, bg='white')
        self.canvas.pack()

        self.r = 20  # Radius of circles
        self.circle_objects = {}  # This will map board coordinates to circle objects
        self.circle_ids = {}  # This will map circle objects to board coordinates
        self.board = None

        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.time_label = tk.Label(self.canvas, text="Black Timer: 0 seconds\nWhite Timer: 0 seconds")
        self.next_move_label = tk.Label(self.canvas, text="Next Move: [F7, F8] R")
        self.next_move_label.place(x=10, y=50)
        self.time_label.place(x=10, y=10)
        self.selected_circles = []  # To keep track of the first selected circlex
        self.current_timer_ran = False
        self.selected_direction = "right"
        self.manager = manager  # Reference to the game manager

    def update_board(self, board, score, moves, playerColor):
        # Update the display based on the provided Board object
        self.board = board
        self.canvas.delete("all")  # Clear the canvas
        self.draw_board()
        self.manager.print_moves()
        self.print_info(score, moves, playerColor)
        self.run()

    def draw_circle(self, x, y, r, tag, text, marble_color, **kwargs):
        """
        Draw a circle
        :param x: is the x position of the circle
        :param y: is the y position of the circle ()
        :param r: is the radius of the circle
        :param tag: is the tuple representing the circle
        :param text: is the text inside the circle
        :param marble_color: the color of the marble as a String
        """
        # Draw the circle
        circle = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=marble_color, **kwargs)
        self.circle_objects[tag] = circle

        # Inserting the circle code here
        self.canvas.create_text(x, y, text=text, fill='black', font=('Arial', 8), tags=tag)

        return circle

    # Modified on_canvas_click method
    def on_canvas_click(self, event):
        """
        Called when the user clicks on a clickable button for direction to make a move
        :param event: the event object that triggered
        """
        clicked_circle = self.get_clicked_circle_tag(event)
        if clicked_circle in ["left", "right", "up_left", "up_right", "down_left", "down_right", "undo"]:
            self.handle_special_action(clicked_circle)
        elif clicked_circle is not None:
            circle = self.board.get_circle(clicked_circle[0], int(clicked_circle[1:]))
            if clicked_circle:

                if clicked_circle not in self.selected_circles:  # selecting marbles
                    self.select_marble(clicked_circle)
                else:
                    # If the same circle is clicked again, deselect it
                    self.deselect_marble(clicked_circle)

                if circle.getMarble() is None:  # selecting an empty circle
                    if 3 >= len(self.selected_circles) >= 0:
                        self.attempt_move(self.selected_circles, clicked_circle)

    def handle_special_action(self, action):
        """
        :param action: the action that will be triggered
        """
        if action == "undo":
            pass
        else:
            self.manager.direction = action
            self.highlight_direction(action)

    def highlight_direction(self, action_tag, select=True):
        """
        :param action_tag: the action that will be triggered
        :param select: whether to select the next action
        """
        # Reset the highlight of the previously selected direction, if any
        if self.selected_direction and self.selected_direction != action_tag:
            self.canvas.itemconfig(self.circle_objects[self.selected_direction],
                                   fill="white")  # Assuming default color is white
        # Highlight the new selected direction
        if select:
            self.canvas.itemconfig(self.circle_objects[action_tag],
                                   fill="gray")  # Change fill color to indicate selection
        self.selected_direction = action_tag if select else None

    def get_clicked_circle_tag(self, event):
        """
        Getter for the clicked circle tag
        :param event: the event object that triggered
        """
        for tag, (cx, cy) in self.circle_ids.items():
            if (event.x - cx) ** 2 + (event.y - cy) ** 2 <= self.r ** 2:
                return tag
        return None

    # Highlight function to visually mark selected circles
    def highlight_circle(self, tag, select):
        """
        highlights and undoes highlights for the selected circle
        :param tag: tuple representing the circle
        :param select: whether to select the next action as a boolean
        """
        tag = f"{tag[0]}{tag[1]}"
        circle = self.circle_objects[tag]
        outline_color = "red" if select else "black"
        self.canvas.itemconfig(circle, outline=outline_color)

    def select_marble(self, tag):
        """
        a function that selects marbles that are within circles on the gui
        :param tag: is the tuple representing the circle
        """
        circle = self.board.get_circle(tag[0], int(tag[1:]))
        if circle.getMarble() is not None and circle.getMarble().get_color() == self.manager.current_player.get_color():
            # First circle selected, highlight it
            self.selected_circles.append(tag)
            self.highlight_circle(tag, True)

    def deselect_marble(self, tag):
        """
        a function that deselects marbles that are already selected circles on the gui
        :param tag: is the tuple representing the circle
        """
        # Deselect the marble and highlight it
        self.selected_circles.remove(tag)
        self.highlight_circle(tag, False)

    @staticmethod
    def _get_move_direction(first_clicked_marble, to_circle):
        """
        gets the direction using the first clicked marble and the second clicked
        circle on the UI
        :param first_clicked_marble: is the first clicked marbles Circle that contains it
        :param to_circle: is the second clicked marbles is used to determine wanted direction
        :return is a string representing the direction that the user can move
        """
        marble_clicked_row = first_clicked_marble[0]
        marble_clicked_number = first_clicked_marble[1]
        to_circle_row = to_circle[0]
        to_circle_number = to_circle[1]
        number_sum = to_circle_number - marble_clicked_number
        row_sum = ord(to_circle_row) - ord(marble_clicked_row)
        if row_sum == 0 and number_sum == 0:
            return 'Invalid'
        elif row_sum == 0 and number_sum > 0:
            return "R"
        elif row_sum == 0 and number_sum < 0:
            return "L"
        elif row_sum > 0 and number_sum == 0:
            return "UL"
        elif row_sum > 0 and number_sum > 0:
            return "UR"
        elif row_sum < 0 and number_sum == 0:
            return "DR"
        elif row_sum < 0 and number_sum < 0:
            return "DL"

    def attempt_move2(self, tags, to_circle_tag):
        """
        attempts to move two marbles at once
        :param tags: is the array of tuples of marbles representations
        :return:
        """
        if len(tags) >= 1:
            to_circle = (to_circle_tag[0], int(to_circle_tag[1:]))
            marbles = [(tag[0], int(tag[1:])) for tag in tags]
            can_all_be_moved = True
            for marble in marbles:
                move_direction_for_marble = Displayer._get_move_direction(marble, to_circle)
                if not self.manager.isValidMove2(marble, move_direction_for_marble):
                    can_all_be_moved = False
                    break
            print(move_direction_for_marble, can_all_be_moved)
            if can_all_be_moved:
                for marble in marbles:
                    self.manager.move_marble2(marble, move_direction_for_marble)
            for tag in tags:
                self.highlight_circle(tag, False)
            self.selected_circles = []

    def attempt_move(self, tags, to_circle_tag):
        """ Attempt to move a marble"""
        marbles = []
        neighbors = []
        to_circle = (to_circle_tag[0], int(to_circle_tag[1:]))
        for tag in tags:
            marbles.append((tag[0], int(tag[1:])))
        if len(tags) == 1:
            # marbles.append((tags[0][0], int(tags[0][1:])))
            if to_circle in self.board.get_neighbors(*marbles[0]):
                # Proceed with the move if the destination is a neighbor
                self.selected_circles = []  # Reset the selection
                self.manager.move_marble(marbles[0], to_circle)
                self.highlight_circle(tags[0], False)
            else:
                print("Invalid move")
                self.highlight_circle(tags[0], False)
                self.selected_circles = []

        else:  # logic for multiple marbles
            for marble in marbles:
                neighbors.append(self.board.get_neighbors(*marble))
            neighbors = [item for sublist in neighbors for item in sublist]  # flatten to 1D list

            if to_circle in neighbors:
                # Proceed with the move if the destination is a neighbor
                self.selected_circles = []  # Reset the selection
                self.manager.move_marble(marbles, to_circle)
                for tag in tags:
                    self.highlight_circle(tag, False)
            else:
                print("Invalid move")
                for tag in tags:
                    self.highlight_circle(tag, False)
                self.selected_circles = []

    def draw_direction_buttons(self):
        """ Draw direction buttons """
        directions = [
            ("left", 50, 450),
            ("right", 150, 450),  # Assuming "right" is highlighted by default
            ("up_left", 50, 375),
            ("up_right", 150, 375),
            ("down_left", 50, 525),
            ("down_right", 150, 525),
        ]

        for direction in directions:
            tag, x, y = direction[:3]
            fill_color = "white"
            if len(direction) == 4:
                fill_color = direction[3]  # Custom fill color if specified
            elif tag == self.selected_direction:
                fill_color = "gray"  # Highlighted color if this direction is selected

            self.draw_circle(x, y, 35, tag, tag.replace("_", " ").title(), fill_color, outline='black')
            self.circle_ids[tag] = (x, y)

    def draw_board(self):
        """ Draws the board that abalone is played on the screen"""
        if self.board is not None:
            start_x = 400  # Center the board on the canvas
            start_y = 50
            row_labels = "IHGFEDCBA"

            y = start_y
            for i, num in enumerate(self.board.rows):
                current_row_width = (self.r * 2 * (num - 1)) + self.r
                x = start_x - (current_row_width / 2)

                for j in range(num):
                    tag = f"{row_labels[i]}{j + self.board.starting_numbers[i]}"
                    circle_color = 'white'

                    # Check if there is a marble in the circle
                    if (row_labels[i], j + self.board.starting_numbers[i]) in self.board.circles:
                        marble = self.board.circles[(row_labels[i], j + self.board.starting_numbers[i])].getMarble()
                        if marble is not None:
                            circle_color = 'black' if marble.get_color().lower() == 'black' else 'lightgray'

                    self.draw_circle(x + (self.r * 2 * j), y, self.r, tag, outline='black', text=tag,
                                     marble_color=circle_color)
                    # Track the circle with its board coordinate
                    self.circle_ids[tag] = (x + (self.r * 2 * j), y)

                y += int(self.r * math.sqrt(3))  # Adjust the vertical distance between rows of circles
        self.draw_direction_buttons()

        Button(text='Undo', master=self.window, command=self.manager.undo_move, position=(280, 360), size=(100, 30))
        Button(text='Pause/unpause', master=self.window,
               command=self.manager.toggle_pause_game, position=(390, 360),
               size=(100, 30))
        self.start_button()

    def start_button(self):
        options = ["Default", "Belgian Daisy", "German Daisy"]
        human_ai = ["Human x Human", "AI(B) x Human(W)", "Human(B) x AI(W)"]
        setup_menu = Button(text='Option types', master=self.window, options=options, position=(340, 450),
                           size=(120, 30), type="dropdown", default_option="Setup Type")
        human_ai_menu = Button(text='Option types', master=self.window, options=human_ai, position=(320, 490),
                             size=(150, 30), type="dropdown", default_option="Game Type")
        Button(text='Start / Reset', master=self.window,
               command=lambda: self.manager.start_game(setup_menu.get_selected_option(),
                                                       human_ai_menu.get_selected_option()), position=(350, 530),
               size=(100, 30))

        Button(text='Stop', master=self.window,
               command=lambda: self.manager.start_game("", ""), position=(350, 580),
               size=(100, 30))

    def print_timer(self):
        """
        Prints the current time and the players moves side by side
        :return:
        """
        if not self.manager.game_paused:
            player_one_time, player_one_agg, player_one_last_move, player_two_time, player_two_agg, player_two_last_move = self.manager.get_time_to_display()
            self.time_label.config(
                text=f"White Timer: {player_one_time} s Agg: {player_one_agg} Last Mov: {player_one_last_move}\nBlack "
                     f"Timer: {player_two_time} s Agg: {player_two_agg} Last Mov: {player_two_last_move}")
        self.time_label.after(1000, self.print_timer)

    def print_info(self, scores, moves, player_color):
        info_text = f"Black Score: {scores[0]} | White Score: {scores[1]} | " \
                    f"Black Moves: {moves[0]} | White Moves: {moves[1]} | " \
                    f"Current Player: {player_color}"

        self.canvas.create_text(400, 650, text=info_text, font=('Arial', 12), anchor=tk.CENTER)

    def run(self):
        if not self.current_timer_ran:
            self.print_timer()
            self.current_timer_ran = True
        self.window.mainloop()
