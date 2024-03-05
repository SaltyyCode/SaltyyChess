import pygame
import os

pieces_pos = [
    ("rook_black", (0, 0)), ("knight_black", (1, 0)), ("bishop_black", (2, 0))
    ("queen_black", (3, 0)), ("king_black", (4, 0)), ("bishop_black", (5, 0))
    ("knight_black", (6, 0)), ("rook_black", (7, 0)),
    *[(f"pawn_black", (i, 1)) for i in range(8)],

    *[(f"pawn_white", (i, 6)) for i in range(8)],
    ("rook_white", (0, 7)), ("knight_white", (1, 7)), ("bishop_white", (2, 7))
    ("queen_white", (3, 7)), ("king_white", (4, 7)), ("bishop_white", (5, 7))
    ("knight_white", (6, 7)), ("rook_white", (7, 7))
]

