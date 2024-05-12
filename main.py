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
brick_pos = pygame.Vector2(screen.get_width() / 2, 20)

playerVelocity = 0
player = Rect(player_pos, (screen.get_width() / 10, 25))
player.x -= player.width / 2

ballX = screen.get_width() / 2
ballY = screen.get_height() * 0.5

ballDown = True
ballRight = True

playerSpeed = 25
ballGravity = 300
ballMaxHoriSpeed = 500
ballHoriSpeed = random.randint(20,200)
if ballHoriSpeed % 2 == 0:
    ballHoriSpeed *= -1
ballRadius = 10

windowSize = pygame.display.get_window_size()

pygame.display.set_caption("BrickBreaker")
playerCollideTimeout = 0
brickCollideTimeout = 0

bricks = []
for i in range(0,10):
    for j in range(0,5):
        bricks.append(Rect(pygame.Vector2((screen.get_width() / 10) * i, 20 * j), ((screen.get_width() / 10), 25)))


brickColors = {0:"orange", 1:"pink", 2:"red", 3:"green", 4:"purple", 5:"brown", 6:"yellow", 7:"orange", 8:"pink", 9:"red", 10:"green"}

inGame = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_TAB] or inGame):
        inGame = True
    
        # Moving Left
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and playerVelocity > 0:
            playerVelocity = -1 * playerSpeed * dt
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            playerVelocity -= playerSpeed * dt

        # Moving right
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and playerVelocity < 0:
            playerVelocity = playerSpeed * dt
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            playerVelocity += playerSpeed * dt

        # Left and Right
        if ((keys[pygame.K_a] or keys[pygame.K_LEFT]) and (keys[pygame.K_d] or keys[pygame.K_RIGHT])):
            playerVelocity = 0

        # Hard stop
        if not (keys[pygame.K_a] or keys[pygame.K_d]
                or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            playerVelocity = 0

        player = player.move(playerVelocity, 0)
        player.x = min(player.x, windowSize[0] - player.width)
        player.x = max(player.x, 0)

        # Ball movement
        ballY += ballGravity * dt
        ballX += ballHoriSpeed * dt

        # Ball bounces off walls & ceiling
        if (ballX > windowSize[0] - ballRadius):
            ballX = windowSize[0] - ballRadius
            ballHoriSpeed *= -1
        elif (ballX < 0 + ballRadius):
            ballX = 0 + ballRadius
            ballHoriSpeed *= -1
        if (ballY <= 0 + ballRadius):
            ballY = 0 + ballRadius
            ballGravity *= -1
    elif pygame.font:
        # Put Text On The Background, Centered
        font = pygame.font.Font(None, 64)
        text = font.render("Welcome to BrickBreaker!", True, "red")
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=200)
        screen.blit(text, textpos)
        textLine2 = font.render("Press 'tab' to start", True, "red")
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=250)
        screen.blit(textLine2, textpos)


        
    drawnPlayer = pygame.draw.rect(screen, "green", player, 40) 
    drawnBall = pygame.draw.circle(screen, "white", pygame.Vector2(ballX, ballY), ballRadius)

    drawnBricks = []
    x=0
    for brick in bricks:
        drawnBricks.append(pygame.draw.rect(screen, brickColors[x % 10], brick, 40))
        if (pygame.Rect.colliderect(drawnBricks[x], drawnBall)
            and brickCollideTimeout == 0):
            ballGravity *= -1
            bricks.remove(brick)
        x+=1

    if (brickCollideTimeout > 0):
        brickCollideTimeout -= 1


    if (pygame.Rect.colliderect(drawnPlayer, drawnBall) # do ball and player collide
        and ballY <= playerHeight + 5 # ignore collisions with the side of the rectangle with some tolerance
        and playerCollideTimeout == 0): # add timeout to prevent spamming direction changes
        horiDir = 1
        if drawnBall.x <= (drawnPlayer.x + (drawnPlayer.width/2)):
            horiDir = -1
        ballHoriSpeed = horiDir * abs((drawnBall.x - (drawnPlayer.x + (drawnPlayer.width/2)))/(drawnPlayer.width)) * ballMaxHoriSpeed
        
        ballGravity *= -1
        playerCollideTimeout = 5
    elif playerCollideTimeout > 0:
        playerCollideTimeout -= 1

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()