import pygame as p
import chess_board
from load_sounds import load_sounds
from game_ui import loadpng, boardpieces, drawpieces, drawboard, seeMoves


WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION
FPS_MAX = 15
IMAGES = {}


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
    sounds = load_sounds()
    move_sound = sounds["move"]
    capture_sound = sounds["capture"]
    check_sound = sounds["check"]
    mate_sound = sounds["mate"]
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
                        gs.makeMove(move, capture_sound)
                        if gs.IsCheck():
                            check_sound.play()
                        else:
                            move_sound.play()
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
            if gs.CheckMate:
                mate_sound.play()

        boardpieces(screen, gs, selectedsquare, validMove)
        clock.tick(FPS_MAX)
        p.display.flip()

if __name__ == "__main__":
    main()
