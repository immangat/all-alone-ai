import pygame
import sys

class GameArea:
    def __init__(self, surface):
        self.surface = surface

    def draw(self):
        # Fill the game area with green
        self.surface.fill((0, 128, 0))

class HUD:
    def __init__(self, surface, screen_width, screen_height):
        self.surface = surface
        self.font = pygame.font.Font(None, 36)  # None uses the default font
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, score):
        self.score = score

    def draw(self):
        # Fill the HUD area with blue
        self.surface.fill((0, 0, 128))
        # Calculate position based on percentages
        text_x = self.screen_width * 0.05  # 5% from the left
        text_y = self.screen_height * 0.05  # 5% from the top of the HUD area
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.surface.blit(score_text, (text_x, text_y))

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Calculate the sizes based on percentages
hud_height_percentage = 0.1  # 10% of the screen height for each HUD
game_area_height = screen_height * (1 - 2 * hud_height_percentage)  # Remaining height for the game area
hud_height = screen_height * hud_height_percentage  # Height for each HUD

# Create surfaces for game area and HUDs
top_hud_surface = screen.subsurface(pygame.Rect(0, 0, screen_width, hud_height))
game_area_surface = screen.subsurface(pygame.Rect(0, hud_height, screen_width, game_area_height))
bottom_hud_surface = screen.subsurface(pygame.Rect(0, hud_height + game_area_height, screen_width, hud_height))

# Initialize game area and HUDs
game_area = GameArea(game_area_surface)
top_hud = HUD(top_hud_surface, screen_width, hud_height)
bottom_hud = HUD(bottom_hud_surface, screen_width, hud_height)

# Main game loop
running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update HUDs
    top_hud.update(score)
    bottom_hud.update(score)

    # Draw the game area and both HUDs
    game_area.draw()
    top_hud.draw()
    bottom_hud.draw()

    score += 1  # Increment the score for demonstration purposes

    pygame.display.flip()

pygame.quit()
sys.exit()
