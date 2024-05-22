import pygame as pg
from pygame import Rect, Surface
import random

NUM_COLUMNS = 10
NUM_ROWS = 4
BRICK_HEIGHT = 35
TEXT_ROW_HEIGHT = 50

# create brick objects for each row/column
def initializeBricks(screen:Surface):
        bricks = []
        for i in range(0, NUM_COLUMNS):
            for j in range(0, NUM_ROWS):
                bricks.append(Rect(pg.Vector2((screen.get_width() / NUM_COLUMNS) * i, BRICK_HEIGHT * j), ((screen.get_width() / NUM_COLUMNS), BRICK_HEIGHT)))
        return bricks

# return ball to original location
def resetBall(screen:Surface) -> float:
     return screen.get_width() / 2, (screen.get_height() * 0.5) + TEXT_ROW_HEIGHT

# return player to original location
def resetPlayer(player:Rect, screen:Surface) -> float:
     return (screen.get_width() / 2) - player.width / 2

# return a brick's ID
def getBrickID(brick:Rect, brickID):
     return list(brickID.keys())[list(brickID.values()).index(brick)]

# set the initial horizontal speed of ball to a random value
def resetBallHoriSpeed() -> int:
     ballHoriSpeed = random.randint(0,125)
     if ballHoriSpeed % 2 == 0:
          ballHoriSpeed *= -1
     return ballHoriSpeed