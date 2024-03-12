import pygame

pygame.init()

pygame.display.set_caption('Quick Start') # top part
window_surface = pygame.display.set_mode((800, 600)) # window

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#FFC0CB'))

is_running = True

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window_surface.blit(background, (0, 0)) # replaces the window with the background?

    pygame.display.update()