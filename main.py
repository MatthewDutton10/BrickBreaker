# Example file showing a circle moving on screen
import pygame as pg
import random
from pygame import Rect

from helper import *

# DOCS: https://www.pygame.org/docs/

# pygame setup
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
dt = 0

# constants
FIRST_TEXT_ROW_POS = 200
HORIZONTAL_CENTER = screen.get_width() / 2
INITIAL_BALL_Y = screen.get_height() / 2 + TEXT_ROW_HEIGHT
INITIAL_BALL_VERT_SPEED = 350
BRICK_VAL = 50
NUM_LIVES = 3


# player information
playerHeight = screen.get_height() * 0.80
player_pos = pg.Vector2(HORIZONTAL_CENTER, playerHeight)
playerVelocity = 0
player = Rect(player_pos, (screen.get_width() / 10, 25))
player.x -= player.width / 2
playerSpeed = 25

# ball coords
ballX = HORIZONTAL_CENTER
ballY = INITIAL_BALL_Y

# ball velo and radius
ballVerticalVelocity = INITIAL_BALL_VERT_SPEED
ballHoriVelocity = resetBallHoriSpeed()
ballRadius = 10

windowSize = pg.display.get_window_size()
pg.display.set_caption("BrickBreaker")

# timeouts to limit consecutive player and brick collisions
playerCollideTimeout = 0
brickCollideTimeout = 0

# list of bricks (pygame rects)
bricks = initializeBricks(screen)

# assign color to each brick
id=0
brickID = {}
colors = ["orange", "pink", "red", "green", "purple", "brown", "yellow"]
random.shuffle(colors)
for brick in bricks:
    brickID[id] = brick
    id+=1

# true when player is in the game, specifically when the ball is moving (not paused, between levels, etc)
inGame = False

# true when the ball collides with the player
touchedPlayer = False

# score and combo info
score = 0
scoreMultiplier = 0
comboText = ""
combo = 0
multiplierVal = 20
highScore = 0

# current lives and level
lives = NUM_LIVES
level = 1

# pause info
paused = False
pauseTimer = 0

if pg.font:
    font = pg.font.Font(None, 64)

# true when there are no more bricks
levelComplete = False

# main loop
while running:
    # poll for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    keys = pg.key.get_pressed()

    # user quit
    if (keys[pg.K_ESCAPE] and (not inGame or paused)):
        running = False
        continue
    elif ((keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]) # user pause
        and inGame
        and pauseTimer == 0):
        paused = not paused
        pauseTimer = 20
        continue
    elif pauseTimer > 0:
        pauseTimer -= 1

    # user currently playing level, or starting to play
    if ((keys[pg.K_TAB] or inGame) 
         and not paused):
        inGame = True
        levelComplete = False

        # new game after a game over
        if (lives == 0):
            ballVerticalVelocity = INITIAL_BALL_VERT_SPEED
            ballHoriVelocity = resetBallHoriSpeed()
            level = 1
            score = 0
            lives = NUM_LIVES
            bricks = initializeBricks(screen)
            random.shuffle(colors)
    
        # Player moving Left
        if (keys[pg.K_a] or keys[pg.K_LEFT]) and playerVelocity > 0:
            playerVelocity = -1 * playerSpeed * dt
        elif (keys[pg.K_a] or keys[pg.K_LEFT]):
            playerVelocity -= playerSpeed * dt

        # Player moving right
        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and playerVelocity < 0:
            playerVelocity = playerSpeed * dt
        elif (keys[pg.K_d] or keys[pg.K_RIGHT]):
            playerVelocity += playerSpeed * dt

        # player moving Left and Right
        if ((keys[pg.K_a] or keys[pg.K_LEFT]) and (keys[pg.K_d] or keys[pg.K_RIGHT])):
            playerVelocity = 0

        # Hard stop
        if not (keys[pg.K_a] or keys[pg.K_d]
                or keys[pg.K_LEFT] or keys[pg.K_RIGHT]):
            playerVelocity = 0

        player = player.move(playerVelocity, 0)
        player.x = min(player.x, windowSize[0] - player.width)
        player.x = max(player.x, 0)

        # Ball movement
        ballY += ballVerticalVelocity * dt
        ballX += ballHoriVelocity * dt

        # Ball bounces off walls & ceiling
        if (ballX > windowSize[0] - ballRadius):
            ballX = windowSize[0] - ballRadius
            ballHoriVelocity *= -1
        elif (ballX < 0 + ballRadius):
            ballX = 0 + ballRadius
            ballHoriVelocity *= -1
        if (ballY <= 0 + ballRadius):
            ballY = 0 + ballRadius
            ballVerticalVelocity *= -1
        elif (ballY >= windowSize[1] - ballRadius):
            lives-=1
            inGame=False
            player.x = resetPlayer(player, screen)
            ballHoriVelocity = resetBallHoriSpeed()
            ballX, ballY = resetBall(screen)
            comboText = ""
            touchedPlayer = False
            scoreMultiplier = 0
            combo = 0

    # game over
    elif lives == 0:
        gameOverText = font.render("Game over :(", True, "red")
        if (score >= highScore):
            highScore = score
            gameOverText = font.render("Game over, new high score!!", True, "red")
        textpos = gameOverText.get_rect(centerx=HORIZONTAL_CENTER, y=FIRST_TEXT_ROW_POS)
        screen.blit(gameOverText, textpos)
        finalScoreText = font.render("Final Score: " + str(score), True, "red")
        finalScorePos = finalScoreText.get_rect(centerx=HORIZONTAL_CENTER, y=FIRST_TEXT_ROW_POS + TEXT_ROW_HEIGHT)
        screen.blit(finalScoreText, finalScorePos)
        newGameText = font.render("Press 'tab' to start a new game", True, "red")
        newGamePos = newGameText.get_rect(centerx=HORIZONTAL_CENTER, y=FIRST_TEXT_ROW_POS + (TEXT_ROW_HEIGHT * 2))
        screen.blit(newGameText, newGamePos)
        quitText = font.render("Press 'Esc' to quit", True, "red")
        quitTextPos = quitText.get_rect(centerx=HORIZONTAL_CENTER, y=FIRST_TEXT_ROW_POS + (TEXT_ROW_HEIGHT * 3))
        screen.blit(quitText, quitTextPos)

    # level complete, game starting, or death text
    elif pg.font and not paused:
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

        textpos2 = textLine1.get_rect(centerx=HORIZONTAL_CENTER, y=FIRST_TEXT_ROW_POS)
        screen.blit(textLine1, textpos2)
        textpos3 = textLine2.get_rect(centerx=HORIZONTAL_CENTER, y=FIRST_TEXT_ROW_POS + TEXT_ROW_HEIGHT)
        screen.blit(textLine2, textpos3)
        textpos4 = textLine3.get_rect(centerx=HORIZONTAL_CENTER, y=FIRST_TEXT_ROW_POS + (TEXT_ROW_HEIGHT * 2))
        screen.blit(textLine3, textpos4)
        shiftPos = shiftText.get_rect(centerx=HORIZONTAL_CENTER, y=FIRST_TEXT_ROW_POS + (TEXT_ROW_HEIGHT * 3))
        screen.blit(shiftText, shiftPos)

    # paused text
    elif pg.font and paused:
        pausedText = font.render("Paused", True, "red")
        pausedPos = pausedText.get_rect(centerx=HORIZONTAL_CENTER, y=FIRST_TEXT_ROW_POS)
        screen.blit(pausedText, pausedPos)

    # draw the player and ball
    drawnPlayer = pg.draw.rect(screen, "green", player, 40) 
    drawnBall = pg.draw.circle(screen, "white", pg.Vector2(ballX, ballY), ballRadius)

    drawnBricks = []
    removeBrickIDs = []
    x=0
    # check for brick collisions with the ball
    for brick in bricks:
        currentBrickID = getBrickID(brick, brickID)
        brick_rect = pg.Rect(brick[0], brick[1], screen.get_width() / NUM_COLUMNS, BRICK_HEIGHT)
        drawnBricks.append(pg.draw.rect(screen, colors[currentBrickID % len(colors)], brick_rect))

        # Create a rectangle around the ball (bounding box of the circle)
        ball_rect = pg.Rect(ballX - ballRadius, ballY - ballRadius, 2 * ballRadius, 2 * ballRadius)

        if brick_rect.colliderect(ball_rect) and brickCollideTimeout == 0:
            # Determine the side of collision
            dx = min(abs(ball_rect.right - brick_rect.left), abs(ball_rect.left - brick_rect.right))
            dy = min(abs(ball_rect.bottom - brick_rect.top), abs(ball_rect.top - brick_rect.bottom))

            if dx < dy:
                ballHoriVelocity *= -1
            else:
                ballVerticalVelocity *= -1
            
            removeBrickIDs.insert(0, currentBrickID)
            combo += scoreMultiplier*multiplierVal
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
    
    # player cleared all bricks
    if (not bricks):
        inGame = False
        levelComplete = True
        
        level+=1
        multiplierVal *= 2
        multiplierVal = min(multiplierVal, 5000)
        scoreMultiplier=0

        # increase ball speed with each level
        ballVerticalVelocity = abs(ballVerticalVelocity)
        ballVerticalVelocity += ballVerticalVelocity*0.1
        
        # reset player and ball pos
        player.x = resetPlayer(player, screen)
        ballX, ballY = resetBall(screen)

        # reset bricks
        drawnBricks = []
        random.shuffle(colors)
        bricks = initializeBricks(screen)
        for brick in bricks:
            currentBrickID = getBrickID(brick, brickID)
            drawnBricks.append(pg.draw.rect(screen, colors[currentBrickID % len(colors)], brick, 40))


    if (brickCollideTimeout > 0):
        brickCollideTimeout -= 1

    # do ball and player collide
    if (pg.Rect.colliderect(drawnPlayer, drawnBall) 
        and ballY <= playerHeight + 5 # ignore collisions with the side of the rectangle with some tolerance
        and playerCollideTimeout == 0): # timeout to prevent spamming direction changes
        horiDir = 1
        if drawnBall.x <= (drawnPlayer.x + (drawnPlayer.width/2)):
            horiDir = -1

        # set hori velocity based on where the ball connected with the player
        ballHoriVelocity = horiDir * abs((drawnBall.x - (drawnPlayer.x + (drawnPlayer.width/2)))/(drawnPlayer.width)) * (abs(ballVerticalVelocity) + 50)
        ballVerticalVelocity *= -1
        playerCollideTimeout = 5
        touchedPlayer = True
        score += combo
        combo = 0
        scoreMultiplier = 0
        comboText = ""
    elif playerCollideTimeout > 0:
        playerCollideTimeout -= 1
    
    # text at the bottom of the window
    scoreText = font.render("Score: " + str(score), True, "red") # + " " + comboText
    scoreTextpos = scoreText.get_rect(centerx=0 + (3*screen.get_width() / 20), y=screen.get_height() - 50)
    screen.blit(scoreText, scoreTextpos)

    comboTextFont = font.render(comboText, True, "green")
    comboTextPos = comboTextFont.get_rect(centerx=0 + (3*screen.get_width() / 20), y=screen.get_height() - (50*2))
    screen.blit(comboTextFont, comboTextPos)

    highScoreText = font.render("High Score: " + str(highScore) , True, "red")
    highScoreTextpos = highScoreText.get_rect(centerx=(screen.get_width() / 4) + (screen.get_width() / 5), y=screen.get_height() - 50)
    screen.blit(highScoreText, highScoreTextpos)

    livesText = font.render("Level: " + str(level) + " ~ Lives: " + str(lives), True, "red")
    livesTextPos = livesText.get_rect(centerx=(3 * screen.get_width() / 4) + (screen.get_width() / 20), y=screen.get_height() - 50)
    screen.blit(livesText, livesTextPos)

    # flip() the display to put work on screen
    pg.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pg.quit()