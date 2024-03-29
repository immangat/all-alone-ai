import pygame


class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, position, size=None):
        super().__init__()
        self.image = pygame.image.load(image)  # Load the image from a file or surface

        # Resize the image if size is provided, else use the original size
        if size:
            self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.topleft = position  # Set the position of the sprite

    def update(self, *args):
        # Update the sprite's position or properties
        # 'args' can be anything your game needs to update the sprite, like a time delta
        pass
