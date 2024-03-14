import pygame
import pygame_gui
from pygame_gui.elements import UILabel, UIImage, UIPanel, UIButton
from part_2 import player
from part_2.player import AIPlayer, HumanPlayer
from part_2.uis.button_ui_layout import ButtonUI
## making players for testing
ai_player = AIPlayer(name="AI Nico", color="Red")
human_player = HumanPlayer(name="Human Manhgott", color="Blue")

MOVE_GUI_WIDTH = 300
MOVE_GUI_HEIGHT = 500
MOVE_GUI_MARGIN = 10
BUTTONS_GUI_WIDTH = 300
BUTTONS_GUI_HEIGHT = 100
BUTTONS_GUI_MARGIN = 10

pygame.init()

#constants
display_info = pygame.display.Info()
WINDOW_WIDTH = display_info.current_w
WINDOW_HEIGHT = display_info.current_h
COLUM_LINE_1 = round(WINDOW_WIDTH * 0.75)
ROW_LINE_1 = round(WINDOW_HEIGHT * 0.1)
ROW_LINE_2 = round(WINDOW_HEIGHT * 0.3)
ROW_LINE_3 = round(WINDOW_HEIGHT * 0.9)
# Set the size of the pygame window
window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Dynamic Layout Example")

# Clock to control the frame rate
clock = pygame.time.Clock()

# UIManager to manage UI elements
manager = pygame_gui.UIManager(window_size, "gui_json/theme.json")

# Define a UI containers (optional, depending on your needs))
abalone_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, ROW_LINE_1), (COLUM_LINE_1, ROW_LINE_3 - ROW_LINE_1)),
                                             manager=manager)

# not style ? why
player_1_hud_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), (COLUM_LINE_1, ROW_LINE_1)),
                                                  manager=manager,
                                                  object_id="player1")

player_2_hud_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,ROW_LINE_3), (COLUM_LINE_1, ROW_LINE_1)),
                                                  manager=manager,
                                                  object_id="player2")
# Your button layout rect
button_layout_rect = pygame.Rect(30, 20, 100, 20)
clock_image_1 = pygame.image.load('assets/clock1.png')


turn_remaining_window = pygame_gui.elements.UIPanel(relative_rect= pygame.Rect((COLUM_LINE_1, 0), (WINDOW_WIDTH - COLUM_LINE_1, ROW_LINE_2)))

moves_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((COLUM_LINE_1, ROW_LINE_2), (WINDOW_WIDTH - COLUM_LINE_1, WINDOW_HEIGHT - ROW_LINE_2 - ROW_LINE_1)))

buttons_gui_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((COLUM_LINE_1, ROW_LINE_3), (WINDOW_WIDTH - COLUM_LINE_1, WINDOW_HEIGHT- ROW_LINE_3)))

#Create and add player elements to player1 container
player_1_info = UILabel(relative_rect=pygame.Rect(0, 0, -1, 50),
                        text='Player 1: {}'.format(ai_player.name),
                        manager=manager,
                        container=player_1_hud_window,
                        object_id="player1",
                        anchors={"centery": "centery"})

player_1_score = UILabel(relative_rect=pygame.Rect((0, 0, -1, -1)),
                         text=' SCORE: {}'.format(ai_player.score),
                         manager=manager,
                         container=player_1_hud_window,
                         object_id="player1",
                         anchors={"centery": "centery",
                         "left": "left", "left_target": player_1_info})

player_1_time = UILabel(relative_rect=pygame.Rect(-45, 0, -1, -1),
                        text='TIME: {} '.format(human_player.clock.current_time),
                        manager=manager,
                        container=player_1_hud_window,
                        object_id="player2",
                        anchors={'left': 'right', 'right': 'right', 'centery': 'centery'})

# create and add buttons
buttons_gui = ButtonUI(buttons_gui_window, manager)
buttons_gui.create_gui()

# player_1_clock = UIImage(relative_rect=pygame.Rect(0, 0, 25, 25),
#                          manager=manager,
#                          container=player_1_hud_window,
#                          image_surface=clock_image_1)


# player_1_clock_label = UILabel(relative_rect=pygame.)

#create and add player2 elements to player2 container
player_2_info = UILabel(relative_rect=pygame.Rect(0, 0, -1, 50),
                        text='Player 2: {}'.format(human_player.name),
                        manager=manager,
                        container=player_2_hud_window,
                        object_id="player2",
                        anchors={"centery": "centery"})

player_2_score = UILabel(relative_rect=pygame.Rect((0, 0, -1, -1)),
                         text=' SCORE: {}'.format(ai_player.score),
                         manager=manager,
                         container=player_2_hud_window,
                         object_id="player2",
                         anchors={"centery": "centery", "left": "left", "left_target": player_2_info})




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

    # print players times to console as a test
    print(human_player.clock.current_time)
    human_player.clock.tick_timer()
    ai_player.clock.tick_timer()

    #updates the clockuilabel with current time
    player_1_time.set_text(' TIME: {:.2f}'.format(human_player.clock.current_time))


    # Update the display
    pygame.display.flip()

pygame.quit()
