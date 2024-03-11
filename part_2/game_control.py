import pygame

from part_2.game_window import GameWindow


class GameControl:
    def __init__(self, game_window):
        self.game_window = game_window  # This should be an instance of GameWindow class
        self.board_state = ''  # You would set this according to your game logic
        self.is_running = False

    def start(self):
        self.is_running = True
        self.game_window.initWindow()
        self.main_loop()

    def stop(self):
        self.is_running = False
        pygame.quit()

    def main_loop(self):
        # This would be the main loop where you keep the game running and handle events
        while self.is_running:
            self.game_window.drawBoard()
            self.game_window.updateWindow()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                # Handle other events (keyboard, mouse, etc)


if __name__ == "__main__":
    game = GameControl(GameWindow(800, 600))
    game.start()
