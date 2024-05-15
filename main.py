# Example file showing a circle moving on screen
import pygame, random
from pygame import Rect

from helper import *

# TODO 
# brick sizing/spacing
# changes between levels
# high score


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
ballGravity = 350 # 300
ballMaxHoriSpeed = 500
ballHoriSpeed = random.randint(20,200)
if ballHoriSpeed % 2 == 0:
    ballHoriSpeed *= -1
ballRadius = 10

windowSize = pygame.display.get_window_size()

pygame.display.set_caption("BrickBreaker")
playerCollideTimeout = 0
brickCollideTimeout = 0

bricks = initializeBricks(screen)
        

id=0
brickID = {}
colors = ["orange", "pink", "red", "green", "purple", "brown", "yellow"]
random.shuffle(colors)
for brick in bricks:
    brickID[id] = brick
    id+=1

inGame = False
touchedPlayer = False

score = 0
scoreMultiplier = 0
comboText = ""
BRICK_VAL = 50
MULTIPLIER_VAL = 20
NUM_LIVES = 3

lives = NUM_LIVES
paused = False
pauseTimer = 0

if pygame.font:
    font = pygame.font.Font(None, 64)

levelComplete = False
level = 1

combo = 0

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
    elif ((keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
        and inGame
        and pauseTimer == 0):
        paused = not paused
        pauseTimer = 20
        continue
    elif pauseTimer > 0:
        pauseTimer -= 1

    if ((keys[pygame.K_TAB] or inGame)
         and not paused):
        inGame = True
        levelComplete = False

        # new game after a game over
        if (lives == 0):
            score = 0
            lives = NUM_LIVES
            bricks = initializeBricks(screen)
            random.shuffle(colors)
    
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
            player.x = resetPlayer(player, screen)
            ballX, ballY = resetBall(screen)
            comboText = ""
            touchedPlayer = False
            scoreMultiplier = 0
            combo = 0
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

    elif pygame.font and not paused:
        if levelComplete:
            textLine1 = font.render("Level " + str(level-1) + " Complete!", True, "red")
            textLine2 = font.render("Press 'tab' to start next level", True, "red")
        elif lives == NUM_LIVES:
            textLine1 = font.render("Welcome to BrickBreaker!", True, "red")
            textLine2 = font.render("Press 'tab' to start", True, "red")
        else:
            textLine1 = font.render("You died :(", True, "red")
            textLine2 = font.render("Press 'tab' to try again", True, "red")
        textLine3 = font.render("Press 'Esc' to quit", True, "red")
        shiftText = font.render("Press 'Shift' to pause", True, "red")

        textpos2 = textLine1.get_rect(centerx=screen.get_width() / 2, y=150)
        screen.blit(textLine1, textpos2)
        textpos3 = textLine2.get_rect(centerx=screen.get_width() / 2, y=200)
        screen.blit(textLine2, textpos3)
        textpos4 = textLine3.get_rect(centerx=screen.get_width() / 2, y=250)
        screen.blit(textLine3, textpos4)
        shiftPos = shiftText.get_rect(centerx=screen.get_width() / 2, y=300)
        screen.blit(shiftText, shiftPos)
    elif pygame.font and paused:
        pausedText = font.render("Paused", True, "red")
        pausedPos = pausedText.get_rect(centerx=screen.get_width() / 2, y=200)
        screen.blit(pausedText, pausedPos)



        
    drawnPlayer = pygame.draw.rect(screen, "green", player, 40) 
    drawnBall = pygame.draw.circle(screen, "white", pygame.Vector2(ballX, ballY), ballRadius)

    drawnBricks = []
    removeBrickIDs = []
    x=0
    for brick in bricks:
        currentBrickID = getBrickID(brick, brickID)
        drawnBricks.append(pygame.draw.rect(screen, colors[currentBrickID % len(colors)], brick, 40))
        if (pygame.Rect.colliderect(drawnBricks[x], drawnBall)
            and brickCollideTimeout == 0):
            ballGravity *= -1
            removeBrickIDs.insert(0, currentBrickID)
            combo += scoreMultiplier*MULTIPLIER_VAL
            scoreMultiplier+=1
            score+=BRICK_VAL
            brickCollideTimeout = 5
            if (touchedPlayer):
                score += combo
                comboText = ""
            else:
                comboText = "+ Combo x" + str(scoreMultiplier)
            touchedPlayer = False
        x+=1

    # remove collided bricks
    for removeID in removeBrickIDs:
        bricks.remove(brickID[removeID])
    
    if (not bricks):
        inGame = False
        levelComplete = True
        drawnBricks = []
        bricks = initializeBricks(screen)
        level+=1
        # ballGravity += (ballGravity*0.05)
        scoreMultiplier=0
        random.shuffle(colors)
        player.x = resetPlayer(player, screen)
        ballX, ballY = resetBall(screen)
        for brick in bricks:
            currentBrickID = getBrickID(brick, brickID)
            drawnBricks.append(pygame.draw.rect(screen, colors[currentBrickID % len(colors)], brick, 40))


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
        score += combo
        combo = 0
        scoreMultiplier = 0
        comboText = ""
    elif playerCollideTimeout > 0:
        playerCollideTimeout -= 1
    
    scoreText = font.render("Score: " + str(score) + " " + comboText, True, "red")
    scoreTextpos = scoreText.get_rect(centerx=screen.get_width() / 5, y=screen.get_height() - 50)
    screen.blit(scoreText, scoreTextpos)

    levelText = font.render("Level: " + str(level), True, "red")
    levelTextPos = levelText.get_rect(centerx=screen.get_width() / 2, y=screen.get_height() - 50)
    screen.blit(levelText, levelTextPos)

    livesText = font.render("Lives: " + str(lives), True, "red")
    livesTextPos = livesText.get_rect(centerx=4 * screen.get_width() / 5, y=screen.get_height() - 50)
    screen.blit(livesText, livesTextPos)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()