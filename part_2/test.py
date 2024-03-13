import pygame
import pygame_menu
import sys

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 400))

def start_game():
    print("Game started")
    # Place game start logic here

def quit_game():
    # Exit the program
    pygame.quit()

# Create the menu
menu = pygame_menu.Menu('Welcome', 600, 400,
                       theme=pygame_menu.themes.THEME_BLUE)

# Add a button for starting the game
menu.add.button('Start', start_game)

# Add a button for quitting
menu.add.button('Quit', quit_game)

# Main loop
while True:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    # Background color
    screen.fill((0, 0, 0))

    # Draw and update the menu
    menu.update(events)
    menu.draw(screen)

    pygame.display.flip()
