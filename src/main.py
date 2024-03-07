import pygame as p
import chess_board

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION
FPS_MAX = 15
IMAGES = {}

def loadpng():

    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("assets/pieces" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def main():
    
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill((255, 255, 255))
    gs = chess_board.GameState()
    #loadpng()
    print(gs.board)
    running = True

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        
        clock.tick(FPS_MAX)
        p.display.flip()

if __name__ == "__main__":
    main()