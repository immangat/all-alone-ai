import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
timer_seconds = 10
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == timer_event:
            timer_seconds -= 1
            if timer_seconds <= 0:
                pygame.time.set_timer(timer_event, 0)  # Stop the timer event
                print("Time's up!")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill((255, 255, 255))
    text = font.render(str(timer_seconds), True, (0, 0, 0))
    screen.blit(text, (180, 130))

    pygame.display.flip()
    clock.tick(60)
