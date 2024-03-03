import tkinter as tk
import math


class Displayer:
    def __init__(self, manager=None):
        self.selected_circles = []
        self.window = tk.Tk()
        self.window.title("Abalone Game")
        self.canvas = tk.Canvas(self.window, width=800, height=700, bg='white')
        self.canvas.pack()

        self.r = 20  # Radius of circles
        self.circle_objects = {}  # This will map board coordinates to circle objects
        self.circle_ids = {}  # This will map circle objects to board coordinates
        self.board = None

        # Bind the click event to the canvas
        self.canvas.bind('<Button-1>', self.on_canvas_click)

        self.selected_circle = None  # To keep track of the first selected circle
        self.manager = manager  # Reference to the game manager

    def updateBoard(self, board):
        # Update the display based on the provided Board object
        self.board = board
        self.canvas.delete("all")  # Clear the canvas
        self.draw_board()
        self.run()

    def draw_circle(self, x, y, r, tag, text, marble_color, **kwargs):
        # Draw the circle
        # print(marble_color)
        circle = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=marble_color, **kwargs)
        self.circle_objects[tag] = circle

        # Inserting the circle code here
        self.canvas.create_text(x, y, text=text, fill='black', font=('Arial', 8), tags=tag)

        return circle

    # Modified on_canvas_click method
    def on_canvas_click(self, event):
        for tag, (cx, cy) in self.circle_ids.items():
            if (event.x - cx) ** 2 + (event.y - cy) ** 2 <= self.r ** 2:
                if self.selected_circle is None:
                    self.select_marble(tag)
                else:
                    self.attempt_move(tag)
                    break

    # Highlight function to visually mark selected circles
    def highlight_circle(self, tag, select):
        tag = f"{tag[0]}{tag[1]}"
        print(tag)
        circle = self.circle_objects[tag]
        outline_color = "red" if select else "black"
        self.canvas.itemconfig(circle, outline=outline_color)

    def select_marble(self, tag):
        circle = self.board.getCircle(tag[0], int(tag[1:]))
        # print(circle.getMarble().getColor())
        if circle.getMarble() is not None and circle.getMarble().getColor() in ['Black', 'White']:
            # First circle selected, highlight it
            self.selected_circle = tag
            self.highlight_circle(tag, True)

    def attempt_move(self, tag):
        # Second circle selected, try to make a move
        from_circle = (self.selected_circle[0], int(self.selected_circle[1:]))
        to_circle = (tag[0], int(tag[1:]))
        print(self.board.get_neighbors(*from_circle))
        if to_circle in self.board.get_neighbors(*from_circle):
            # Proceed with the move if the destination is a neighbor
            self.selected_circle = None  # Reset the selection
            print(self.selected_circle)
            self.manager.moveMarble(from_circle, to_circle)
            self.highlight_circle(tag, False)
        else:
            print("Invalid move")
            self.highlight_circle(self.selected_circle, False)
            self.selected_circle = None

    def draw_board(self):
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
                            circle_color = 'black' if marble.getColor().lower() == 'black' else 'lightgray'

                    self.draw_circle(x + (self.r * 2 * j), y, self.r, tag, outline='black', text=tag,
                                     marble_color=circle_color)
                    # Track the circle with its board coordinate
                    self.circle_ids[tag] = (x + (self.r * 2 * j), y)

                y += int(self.r * math.sqrt(3))  # Adjust the vertical distance between rows of circles

    def run(self):
        self.window.mainloop()
