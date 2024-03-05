import pygame
import os

pieces_pos = [
    ("rook_black", (0, 0)), ("knight_black", (1, 0)), ("bishop_black", (2, 0)),
    ("queen_black", (3, 0)), ("king_black", (4, 0)), ("bishop_black", (5, 0)),
    ("knight_black", (6, 0)), ("rook_black", (7, 0)),
    *[(f"pawn_black", (i, 1)) for i in range(8)],

    *[(f"pawn_white", (i, 6)) for i in range(8)],
    ("rook_white", (0, 7)), ("knight_white", (1, 7)), ("bishop_white", (2, 7)),
    ("queen_white", (3, 7)), ("king_white", (4, 7)), ("bishop_white", (5, 7)),
    ("knight_white", (6, 7)), ("rook_white", (7, 7))
]

def load_draw_pieces(screen):
    SIZE = 100
    piece_size = 60
    offset = (SIZE - piece_size) // 2

    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    pieces_path = os.path.join(current_dir, '..', 'assets', 'pieces')

    for pieces_name, pos in pieces_pos:
        image_path = os.path.join(pieces_path, pieces_name + ".png")
        try:
            piece_image = pygame.image.load(image_path).convert_alpha()
            piece_image = pygame.transform.scale(piece_image,(piece_size, piece_size))
            pixel_pos = (pos[0] * SIZE + offset, pos[1] * SIZE + offset)
            screen.blit(piece_image, pixel_pos)
        except pygame.error as e:
            print(f"Erreur lors du charmgement de la piece {image_path}: {e}")
