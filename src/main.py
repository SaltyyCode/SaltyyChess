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
        IMAGES[piece] = p.transform.scale(p.image.load("assets/pieces/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

def boardpieces(screen, gs):
    drawboard(screen)
    drawpieces(screen, gs.board)


def drawboard(screen):
    colors = [p.Color(255, 255, 255), p.Color(98, 62, 8)]
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            color = colors[((x+y) % 2)]
            p.draw.rect(screen, color, p.Rect(y*SQUARE_SIZE, x*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawpieces(screen, board):
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            piece = board[x][y]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(y*SQUARE_SIZE, x*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def main():
    
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("SaltyyChess, First python project")
    clock = p.time.Clock()
    screen.fill((255, 255, 255))
    gs = chess_board.GameState()
    validMove = gs.getvalidMoves()
    moveMade = False
    loadpng()
    running = True
    selectedsquare = ()
    playerClick = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQUARE_SIZE
                row = location[1]//SQUARE_SIZE
                if selectedsquare == (row, col):
                    selectedsquare = ()
                    playerClick = []
                else:
                    selectedsquare = (row, col)
                    playerClick.append(selectedsquare)
                if len(playerClick) == 2:
                    move = chess_board.Move(playerClick[0], playerClick[1], gs.board)
                    if move in validMove:
                        gs.makeMove(move)
                        moveMade = True
                        selectedsquare = ()
                        playerClick = []
                    else: # If player clicks twice on board or on different pieces, the last click is saved.
                        playerClick = [selectedsquare] # If a move is possible in the next click, it will be done.
                    
            elif e.type == p.KEYDOWN:
                if e.key == p.K_LEFT:
                    gs.undo()
                elif e.key == p.K_RIGHT:
                    gs.redo()
        
        if moveMade:
            validMove = gs.getvalidMoves()
            moveMade = False

        boardpieces(screen, gs)
        clock.tick(FPS_MAX)
        p.display.flip()

if __name__ == "__main__":
    main()
