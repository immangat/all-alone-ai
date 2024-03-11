import pygame

from part_2.sprite import MySprite


class GameWindow:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.display_surface = None
        self.sprites = pygame.sprite.Group() # Group to hold all sprite objects

    def initWindow(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Game Window')
        self.loadSprites()

    def updateWindow(self):
        # This will update the contents of the entire display
        self.display_surface.fill((255, 255, 255))  # Clear the screen with a white background
        self.sprites.update()  # Update all the sprites in the group
        self.sprites.draw(self.display_surface)  # Draw all the sprites in the group
        pygame.display.flip()

    def loadSprites(self):
        # Load the images as sprites
        black_marble_sprite = MySprite('assets/black_marble.png', (100, 100), (65,65))
        white_marble_sprite = MySprite('assets/marble_white.png', (150, 150), (50,50))
        self.sprites.add(black_marble_sprite, white_marble_sprite)  # Add them to the group

    def drawBoard(self):
        # This method will be used to draw the game board on the display surface
        # You'll need to fill in the specifics of how you want to draw your board.
        pass  # replace this with your drawing code

if __name__ == "__main__":
    game_window = GameWindow(800, 600)
    game_window.initWindow()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game_window.updateWindow()
    pygame.quit()