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
touchedPlayer = False

score = 0
scoreMultiplier = 0
comboText = ""
BRICK_VAL = 50
MULTIPLIER_VAL = 20

lives = 3

if pygame.font:
    font = pygame.font.Font(None, 64)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_ESCAPE] and not inGame):
        running = False
        continue
    elif keys[pygame.K_ESCAPE]:
        # TODO pause

    if (keys[pygame.K_TAB] or inGame):
        inGame = True

        # new game after a game over
        if (lives == 0):
            score = 0
            lives = 3
            bricks = []
            for i in range(0,10):
                for j in range(0,5):
                    bricks.append(Rect(pygame.Vector2((screen.get_width() / 10) * i, 20 * j), ((screen.get_width() / 10), 25)))
    
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
        elif (ballY >= windowSize[1] - ballRadius):
            lives-=1
            inGame=False
            player.x = (screen.get_width() / 2) - player.width / 2
            ballX = screen.get_width() / 2
            ballY = screen.get_height() * 0.5
            comboText = ""
            touchedPlayer = False
            scoreMultiplier = 0
    elif lives == 0:
        gameOverText = font.render("Game over :(", True, "red")
        textpos = gameOverText.get_rect(centerx=screen.get_width() / 2, y=150)
        screen.blit(gameOverText, textpos)
        finalScoreText = font.render("Final Score: " + str(score), True, "red")
        finalScorePos = finalScoreText.get_rect(centerx=screen.get_width() / 2, y=200)
        screen.blit(finalScoreText, finalScorePos)
        newGameText = font.render("Press 'tab' to start a new game", True, "red")
        newGamePos = newGameText.get_rect(centerx=screen.get_width() / 2, y=250)
        screen.blit(newGameText, newGamePos)
        quitText = font.render("Press 'Esc' to quit", True, "red")
        quitTextPos = quitText.get_rect(centerx=screen.get_width() / 2, y=300)
        screen.blit(quitText, quitTextPos)

    elif pygame.font:
        if lives == 3:
            textLine1 = font.render("Welcome to BrickBreaker!", True, "red")
            textLine2 = font.render("Press 'tab' to start", True, "red")
        else:
            textLine1 = font.render("You died :(", True, "red")
            textLine2 = font.render("Press 'tab' to try again", True, "red")
        textLine3 = font.render("Press 'Esc' to quit", True, "red")

        textpos2 = textLine1.get_rect(centerx=screen.get_width() / 2, y=200)
        screen.blit(textLine1, textpos2)
        textpos3 = textLine2.get_rect(centerx=screen.get_width() / 2, y=250)
        screen.blit(textLine2, textpos3)
        textpos4 = textLine3.get_rect(centerx=screen.get_width() / 2, y=300)
        screen.blit(textLine3, textpos4)


        
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
            if (touchedPlayer):
                score+=BRICK_VAL
                scoreMultiplier+=1
                comboText = ""
            else:
                score += BRICK_VAL + (scoreMultiplier * MULTIPLIER_VAL)
                scoreMultiplier+=1
                comboText = "+ Combo x" + str(scoreMultiplier)
            touchedPlayer = False
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
        touchedPlayer = True
        comboText = ""
    elif playerCollideTimeout > 0:
        playerCollideTimeout -= 1

    
    scoreText = font.render("Score: " + str(score) + " " + comboText, True, "red")
    scoreTextpos = scoreText.get_rect(centerx=screen.get_width() / 4, y=screen.get_height() - 50)
    screen.blit(scoreText, scoreTextpos)

    livesText = font.render("Lives: " + str(lives), True, "red")
    livesTextPos = livesText.get_rect(centerx=3 * screen.get_width() / 4, y=screen.get_height() - 50)
    screen.blit(livesText, livesTextPos)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()