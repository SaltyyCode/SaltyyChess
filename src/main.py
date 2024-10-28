import pygame as p
import chess_board
import game_ui
from load_sounds import load_sounds, play_sound

WIDTH = HEIGHT = 800
FPS_MAX = 15

def main():

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("grey"))
    gs = chess_board.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    game_ui.load_images()
    sounds = load_sounds()
    running = True
    selected_square = ()
    player_clicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()
                col = loc[0] // game_ui.SQUARE_SIZE
                row = loc[1] // game_ui.SQUARE_SIZE
                if selected_square == (row, col):
                    selected_square = ()
                    player_clicks = []
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square)
                if len(player_clicks) == 2:
                    move = chess_board.Move(player_clicks[0], player_clicks[1], gs.board)
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            gs.make_move(valid_moves[i])
                            move_made = True
                            selected_square = ()
                            player_clicks = []
                            if move.piece_captured != "--":
                                play_sound(sounds, "capture")
                            else:
                                play_sound(sounds, "move")

                    if not move_made:
                        player_clicks = [selected_square]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True

            if gs.checkmate:
                if gs.white_to_move:
                    print("Black wins")
                else:
                    print("White wins")
                play_sound(sounds, "mate")
                running = False
            elif gs.stalemate:
                print("Stalemate")
                running = False
            elif gs.in_check():
                play_sound(sounds, "check")  # Jouer le son d'échec

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        game_ui.draw_game_state(screen, gs, valid_moves, selected_square)
        clock.tick(FPS_MAX)
        p.display.flip()

if __name__ == "__main__":
    main()
