import pygame
import pygame_gui
from pygame_gui.elements import UIButton

pygame.init()

# top part who cares
pygame.display.set_caption('Quick Start')
# main window/surface etc
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background2 = pygame.Surface((200, 200))
background2.fill(pygame.Color('#000000'))
background.fill(pygame.Color('#F00F00'))

# needed
manager = pygame_gui.UIManager((800, 600))

# button is added to the gui element list hmmm
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=manager)
# usually needs a clock
clock = pygame.time.Clock()
is_running = True

button_layout_rect = pygame.Rect(30, 20, 100, 20)

UIButton(relative_rect=button_layout_rect,
         text='Hello', manager=manager,
         container=ui_window,
         anchors={'left': 'left',
                  'right': 'right',
                  'top': 'top',
                  'bottom': 'bottom'})

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print('Hello World!')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    window_surface.blit(background2,  (100, 100))
    manager.draw_ui(window_surface)

    pygame.display.update()