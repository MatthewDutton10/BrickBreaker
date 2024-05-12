import pygame as pg
from pygame import Rect

NUM_COLUMNS = 10
NUM_ROWS = 5

def initializeBricks(screen):
        bricks = []
        for i in range(0, NUM_COLUMNS): # 10
            for j in range(0, NUM_ROWS): # 5
                bricks.append(Rect(pg.Vector2((screen.get_width() / 10) * i, 20 * j), ((screen.get_width() / 10), 25)))
        return bricks

def resetBall(screen):
     return screen.get_width() / 2, screen.get_height() * 0.5

def resetPlayer(player, screen):
     return (screen.get_width() / 2) - player.width / 2

def getBrickID(brick, brickID):
     return list(brickID.keys())[list(brickID.values()).index(brick)]