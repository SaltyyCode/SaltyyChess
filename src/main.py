import pygame as p
import chess_board
import game_ui
from bots.random import play_bot_move
from load_sounds import load_sounds, play_sound


WIDTH = HEIGHT = 800
FPS_MAX = 15

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("grey"))
    gs = chess_board.GameState()

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" #Default Postion in fen
    gs.setup_from_fen(fen) 

    valid_moves = gs.get_valid_moves()
    move_made = False
    game_ui.load_images()
    sounds = load_sounds()
    running = True
    selected_square = ()
    player_clicks = []
    game_over = False
    in_check_status = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and not game_over:
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
                            gs.make_move(valid_moves[i], is_final_move=True)
                            move_made = True
                            selected_square = ()
                            player_clicks = []
                            if move.piece_captured != "--":
                                play_sound(sounds, "capture")
                            else:
                                play_sound(sounds, "move")
                            in_check_status = False

                    if not move_made:
                        player_clicks = [selected_square]

            elif e.type == p.KEYDOWN and not game_over:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True
                    in_check_status = False

            if not game_over and gs.checkmate:
                if gs.white_to_move:
                    print("Black wins")
                else:
                    print("White wins")
                play_sound(sounds, "mate")
                game_over = True

            elif not game_over and gs.stalemate:
                print("Stalemate")
                play_sound(sounds, "check")
                game_over = True

            elif not game_over and gs.in_check() and not in_check_status:
                play_sound(sounds, "check")
                in_check_status = True

        if not gs.white_to_move and not move_made: #Delete this bloc to play against human
            play_bot_move(gs)
            move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        game_ui.draw_game_state(screen, gs, valid_moves, selected_square)
        clock.tick(FPS_MAX)
        p.display.flip()

if __name__ == "__main__":
    main()
