import pygame
import sys

def display_board(screen):

    WHITE = (255, 255, 255)
    PURPLE = (128, 0, 128)
    SIZE = 100

    for row in range(8):
        for col in range(8):
            x = col * SIZE
            y = row * SIZE
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = PURPLE
            pygame.draw.rect(screen, color, (x, y, SIZE, SIZE))
