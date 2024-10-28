import pygame as p

DIMENSION = 8
SQUARE_SIZE = 800 // DIMENSION
IMAGES = {}

def load_images():

    pieces = ["bRook", "bN", "bBishop", "bQueen", "bKing", "bPawn", "wRook", "wN", "wBishop", "wQueen", "wKing", "wPawn"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("assets/pieces/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

def draw_game_state(screen, gs, valid_moves, selected_square):

    draw_board(screen)
    draw_pieces(screen, gs.board)
    highlight_moves(screen, gs, selected_square, valid_moves)

def draw_board(screen):

    colors = [p.Color(255, 255, 255), p.Color(98, 62, 8)]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlight_moves(screen, gs, selected_square, valid_moves):

    if isinstance(selected_square, tuple) and len(selected_square) == 2:
        row, col = selected_square

        if gs.board[row][col][0] == ('w' if gs.white_to_move else 'b'):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('green'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            s.fill(p.Color('red'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))
