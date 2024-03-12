import pygame
import pygame_gui

pygame.init()

window_size = (800, 600)
window_surface = pygame.display.set_mode(window_size)
background = pygame.Surface(window_size)
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager(window_size)

# Create a panel
panel_rect = pygame.Rect(50, 50, 300, 400)  # Position and size of the panel
panel = pygame_gui.elements.UIPanel(relative_rect=panel_rect,
                                    starting_height=1,
                                    manager=manager)

# Create a button inside the panel
button_rect = pygame.Rect(50, 50, 100, 50)  # Position and size of the button relative to the panel
button = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                      text='Click Me',
                                      manager=manager,
                                      container=panel)  # Notice how we specify the panel as the container

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
