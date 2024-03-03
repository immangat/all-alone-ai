import tkinter as tk
import math


class Displayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Abalone Game")
        self.canvas = tk.Canvas(window, width=800, height=700, bg='white')
        self.canvas.pack()

        self.r = 20  # Radius of circles
        self.circle_objects = {}  # This will map board coordinates to circle objects
        self.circle_ids = {}  # This will map circle objects to board coordinates
        self.draw_board()

        # Bind the click event to the canvas
        self.canvas.bind('<Button-1>', self.on_canvas_click)

    def draw_circle(self, x, y, r, tag, **kwargs):
        circle = self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)
        self.circle_objects[tag] = circle
        return circle

    def on_canvas_click(self, event):
        # Check if the click is within the radius of any circle
        for tag, (cx, cy) in self.circle_ids.items():
            if (event.x - cx) ** 2 + (event.y - cy) ** 2 <= self.r ** 2:
                print(f"Circle {tag} clicked")
                circle = self.circle_objects[tag]
                self.canvas.itemconfig(circle, fill="blue")
                break  # Exit the loop after finding the circle

    def draw_board(self):
        start_x = 400  # Center the board on the canvas
        start_y = 50
        row_labels = "IHGFEDCBA"
        starting_numbers = [5, 4, 3, 2, 1, 1, 1, 1, 1]
        rows = [5, 6, 7, 8, 9, 8, 7, 6, 5]

        y = start_y
        for i, num in enumerate(rows):
            current_row_width = (self.r * 2 * (num - 1)) + self.r
            x = start_x - (current_row_width / 2)
            for j in range(num):
                tag = f"{row_labels[i]}{j + starting_numbers[i]}"
                self.draw_circle(x + (self.r * 2 * j), y, self.r, tag, outline='black')
                # Track the circle with its board coordinate
                self.circle_ids[tag] = (x + (self.r * 2 * j), y)
            y += int(self.r * math.sqrt(3))  # Adjust the vertical distance between rows of circles

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    window = tk.Tk()
    game = Displayer(window)
    game.run()
