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
    x_ajust = 10
    new_size = (80, 80)

    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    pieces_path = os.path.join(current_dir, '..', 'assets', 'pieces')

    for piece_name, position in pieces_pos:
        image_path = os.path.join(pieces_path, piece_name + ".png")
        try:
            piece_image = pygame.image.load(image_path).convert_alpha()
            if "knight" in piece_name or "bishop" in piece_name or "pawn" in piece_name:
                piece_image = pygame.transform.scale(piece_image, new_size)
                pixel_pos = ((position[0] * SIZE) + (SIZE - new_size[0]) // 2 + x_ajust,
                             (position[1] * SIZE) + (SIZE - new_size[1]) // 2)
            else:
                pixel_pos = (position[0] * SIZE + x_ajust, position[1] * SIZE)
            screen.blit(piece_image, pixel_pos)
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image {image_path}: {e}")

