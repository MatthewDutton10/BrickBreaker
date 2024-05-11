# Example file showing a circle moving on screen
import pygame, random
from pygame import Rect

# DOCS: https://www.pygame.org/docs/

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

playerHeight = screen.get_height() * 0.80
player_pos = pygame.Vector2(screen.get_width() / 2, playerHeight)

playerVelocity = 0
player = Rect(player_pos, (100, 25))
player.x -= player.width / 2

ballX = screen.get_width() / 2
ballY = screen.get_height() * 0.5

ballDown = True
ballRight = True

playerSpeed = 25
ballGravity = 200
ballHoriSpeed = random.randint(50,250)
ballMovingRight = False
if random.randint(0,1) == 0:
    ballMovingRight = True
ballRadius = 10

windowSize = pygame.display.get_window_size()

pygame.display.set_caption("BrickBreaker")
collideTimeout = 5

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
    if keys[pygame.K_a] and playerVelocity > 0:
        playerVelocity = -1 * playerSpeed * dt
    elif keys[pygame.K_a]:
        playerVelocity -= playerSpeed * dt

    # Moving right
    if keys[pygame.K_d] and playerVelocity < 0:
        playerVelocity = playerSpeed * dt
    elif keys[pygame.K_d]:
        playerVelocity += playerSpeed * dt

    # Left and Right
    if keys[pygame.K_a] and keys[pygame.K_d]:
        playerVelocity = 0

    # Hard stop
    if not (keys[pygame.K_a] or keys[pygame.K_d]):
        playerVelocity = 0

    player = player.move(playerVelocity, 0)
    player.x = min(player.x, windowSize[0] - player.width)
    player.x = max(player.x, 0)

    # Ball vertical movement
    if ballDown:
        ballY += ballGravity * dt
    else:
        ballY -= ballGravity * dt


    # Ball horizontal movement
    if (ballMovingRight):
        ballX += ballHoriSpeed * dt
    else:
        ballX -= ballHoriSpeed * dt

    # Ball bounces off walls
    if (ballX >= windowSize[0] - ballRadius):
        ballX = windowSize[0] - ballRadius
        ballMovingRight = not ballMovingRight
    elif (ballX <= 0 + ballRadius):
        ballX = 0 + ballRadius
        ballMovingRight = not ballMovingRight 
    if (ballY <= 0 + ballRadius):
        ballY = 0 + ballRadius
        ballGravity *= -1


    pygame.Rect.colliderect(pygame.draw.rect(screen, "green", player, 40),
                            pygame.draw.circle(screen, "white", pygame.Vector2(ballX, ballY), ballRadius))
    
    drawnPlayer = pygame.draw.rect(screen, "green", player, 40) 
    drawnBall = pygame.draw.circle(screen, "white", pygame.Vector2(ballX, ballY), ballRadius)


    if (pygame.Rect.colliderect(drawnPlayer, drawnBall) # do ball and player collide
        and ballY <= playerHeight + 5 # ignore collisions with the side of the rectangle with some tolerance
        and collideTimeout == 0): # add timeout to prevent spamming direction changes
        ballGravity *= -1
        collideTimeout = 5
    elif collideTimeout > 0:
        collideTimeout -= 1

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()