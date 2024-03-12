import pygame
import pygame_gui

pygame.init()

#constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
COLUM_LINE_1 = round(WINDOW_WIDTH * 0.75)
ROW_LINE_1 = round(WINDOW_HEIGHT * 0.1)
ROW_LINE_2 = round(WINDOW_HEIGHT * 0.3)
ROW_LINE_3 = round(WINDOW_HEIGHT * 0.9)
# Set the size of the pygame window
window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("UI Button Example")

# Clock to control the frame rate
clock = pygame.time.Clock()

# UIManager to manage UI elements
manager = pygame_gui.UIManager(window_size)

# Define a UI container (optional, depending on your needs))
abalone_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, ROW_LINE_1), (COLUM_LINE_1, ROW_LINE_3 - ROW_LINE_1)),
                                        manager=manager)
player_1_hud_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), (COLUM_LINE_1, ROW_LINE_1)))

player_2_hud_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,ROW_LINE_3), (COLUM_LINE_1, ROW_LINE_1)))
# Your button layout rect
button_layout_rect = pygame.Rect(30, 20, 100, 20)

turn_remaining_window = pygame_gui.elements.UIPanel(relative_rect= pygame.Rect((COLUM_LINE_1, 0), (WINDOW_WIDTH - COLUM_LINE_1, ROW_LINE_2)))

moves_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((COLUM_LINE_1, ROW_LINE_2), (WINDOW_WIDTH - COLUM_LINE_1, WINDOW_HEIGHT - ROW_LINE_2 - ROW_LINE_1)))

options_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((COLUM_LINE_1, ROW_LINE_3), (WINDOW_WIDTH - COLUM_LINE_1, WINDOW_HEIGHT- ROW_LINE_3)))

# Create a UIButton
button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                      text='Hello',
                                      manager=manager,
                                      container=abalone_window)

running = True
while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pass the event to the UIManager
        manager.process_events(event)

    # Update UIManager
    manager.update(time_delta)

    # Clear the screen to black (or any other color)
    screen.fill((0, 0, 0))

    # Draw UI elements
    manager.draw_ui(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()
