import pygame as pg
from pygame import Rect
import random

NUM_COLUMNS = 10
NUM_ROWS = 4
BRICK_HEIGHT = 35
TEXT_ROW_HEIGHT = 50

def initializeBricks(screen):
        bricks = []
        for i in range(0, NUM_COLUMNS):
            for j in range(0, NUM_ROWS):
                bricks.append(Rect(pg.Vector2((screen.get_width() / NUM_COLUMNS) * i, BRICK_HEIGHT * j), ((screen.get_width() / NUM_COLUMNS), BRICK_HEIGHT)))
        return bricks

def resetBall(screen):
     return screen.get_width() / 2, (screen.get_height() * 0.5) + TEXT_ROW_HEIGHT

def resetPlayer(player, screen):
     return (screen.get_width() / 2) - player.width / 2

def getBrickID(brick, brickID):
     return list(brickID.keys())[list(brickID.values()).index(brick)]

def resetBallHoriSpeed(ballHoriSpeed):
     ballHoriSpeed = random.randint(0,125)
     if ballHoriSpeed % 2 == 0:
          ballHoriSpeed *= -1
     return ballHoriSpeed