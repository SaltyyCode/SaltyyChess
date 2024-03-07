import pygame as p
from main import *

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION
FPS_MAX = 15
IMAGES = {}

def drawboard(screen):
    colors = [p.Color(255, 255, 255), p.Color(98, 62, 8)]
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            color = colors[((x+y) % 2)]
            p.draw.rect(screen, color, p.Rect(y*SQUARE_SIZE, x*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


