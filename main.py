# Example file showing a circle moving on screen
import pygame
from pygame import Rect

# DOCS: https://www.pygame.org/docs/

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() * 0.80)

horiMove = 0
verMove = 0
upOrDownPressed = False
leftOrRightPressed = False

player = Rect(player_pos, (100, 25))

speed = 25

windowSize = pygame.display.get_window_size()

pygame.display.set_caption("BrickBreaker")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    keys = pygame.key.get_pressed()
    
    # Moving Left
    if keys[pygame.K_a] and horiMove > 0:
        horiMove = -1 * speed * dt
    elif keys[pygame.K_a]:
        horiMove -= speed * dt

    # Moving right
    if keys[pygame.K_d] and horiMove < 0:
        horiMove = speed * dt
    elif keys[pygame.K_d]:
        horiMove += speed * dt

    # Left and Right
    if keys[pygame.K_a] and keys[pygame.K_d]:
        horiMove = 0

    # Hard stop
    if not (keys[pygame.K_a] or keys[pygame.K_d]):
        horiMove = 0

    player = player.move(horiMove, verMove)


    player.x = min(player.x, windowSize[0] - 50)
    player.x = max(player.x, 0) # left 

    pygame.draw.rect(screen, "green", player, 40) 

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()