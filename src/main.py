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

def boardpieces(screen, gs, selectedsquare, getallMoves):
    drawboard(screen)
    drawpieces(screen, gs.board)
    seeMoves(screen, gs, selectedsquare, getallMoves)


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

def seeMoves(screen, gs, selectedsquare, getallMoves):

    if selectedsquare != ():
        r, c = selectedsquare
        if gs.board[r][c][0] == ('w' if gs.whiteMove else 'b'):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('green'))
            screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))
            s.fill(p.Color('red'))
            for move in getallMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQUARE_SIZE, move.endRow * SQUARE_SIZE))


def main():
    
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("SaltyyChess, First python project")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_board.GameState()
    validMoves = gs.getvalidMoves()
    moveMade = False
    loadpng()
    running = True
    selectedSquare = ()
    playerClicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gs.Draw and not gs.CheckMate and not gs.staleMate:  # Game is still on
                    location = p.mouse.get_pos()  # Get mouse position
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if selectedSquare == (row, col):  # User clicked the same square twice
                        selectedSquare = ()  # Deselect
                        playerClicks = []  # Clear clicks
                    else:
                        selectedSquare = (row, col)  # Select square
                        playerClicks.append(selectedSquare)  # Append for move
                    if len(playerClicks) == 2:  # Check if two clicks (start and end of move)
                        move = chess_board.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                            selectedSquare = ()
                            playerClicks = []
                        else:
                            playerClicks = [selectedSquare]  # Keep the last click if the move wasn't valid
                else:
                    print("Game over. No further moves allowed.")
                    
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo move
                    gs.undo()
                    moveMade = True
                elif e.key == p.K_y:  # Redo move
                    gs.redo()
                    moveMade = True
        
        if moveMade:
            validMoves = gs.getvalidMoves()
            moveMade = False

        boardpieces(screen, gs, selectedSquare, validMoves)  # Draw pieces on the board
        clock.tick(FPS_MAX)
        p.display.flip()

if __name__ == "__main__":
    main()
