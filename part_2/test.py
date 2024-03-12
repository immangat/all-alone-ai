import pygame
import math

class AbaloneGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = None
        self.r = 20  # Radius of circles
        self.circle_objects = {}  # This will map board coordinates to circle objects
        self.circle_ids = {}  # This will map circle objects to board coordinates
        self.init_window()
        self.draw_board()

    def init_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Abalone Game")
        self.screen.fill((255, 255, 255))

    def draw_circle(self, x, y, r, tag, **kwargs):
        color = kwargs.get('outline', (0, 0, 0))
        circle = pygame.draw.circle(self.screen, color, (x, y), r)
        self.circle_objects[tag] = circle
        self.circle_ids[tag] = (x, y)
        return circle

    def on_canvas_click(self, position):
        x, y = position
        # Check if the click is within the radius of any circle
        for tag, (cx, cy) in self.circle_ids.items():
            if (x - cx) ** 2 + (y - cy) ** 2 <= self.r ** 2:
                print(f"Circle {tag} clicked")
                self.draw_circle(cx, cy, self.r, tag, outline=(0, 0, 255))  # Blue fill
                pygame.display.flip()
                break  # Exit the loop after finding the circle

    def draw_board(self):
        start_x = self.width // 2  # Center the board on the canvas
        start_y = 50
        row_labels = list(range(1, 10))  # 1 to 9 instead of I to A
        starting_numbers = [5, 4, 3, 2, 1, 1, 1, 1, 1]
        rows = [5, 6, 7, 8, 9, 8, 7, 6, 5]

        y = start_y
        for i, num in enumerate(rows):
            current_row_width = (self.r * 2 * (num - 1)) + self.r
            x = start_x - (current_row_width // 2)
            for j in range(num):
                # Change 'row_labels[i]' to match the '1' to '9' scheme
                tag = f"{row_labels[8-i]}{j + starting_numbers[i]}"  # Flip the row_labels index for '1' at the bottom
                self.draw_circle(x + (self.r * 2 * j), y, self.r, tag, outline=(0, 0, 0))
                # Track the circle with its board coordinate
                self.circle_ids[tag] = (x + (self.r * 2 * j), y)
            y += int(self.r * math.sqrt(3))  # Adjust the vertical distance between rows of circles
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    self.on_canvas_click(event.pos)
        pygame.quit()


if __name__ == "__main__":
    game = AbaloneGame(800, 700)
    game.run()
