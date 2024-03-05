import pygame
from displayboard import display_board
from displaypieces import *

def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("SaltyyChess, First python project")
    display_board(screen)
    load_draw_pieces(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
if __name__ == "__main__":
    main()