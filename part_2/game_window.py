import pygame


class GameWindow:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.display_surface = None

    def initWindow(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Game Window')

    def updateWindow(self):
        # This will update the contents of the entire display
        pygame.display.flip()

    def drawBoard(self):
        # This method will be used to draw the game board on the display surface
        # You'll need to fill in the specifics of how you want to draw your board.
        pass  # replace this with your drawing code

