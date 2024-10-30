#Sample of a main exemple for a bot versus bot game
#Just copy paste it in main.py to test it
import pygame as p
import chess_board
import game_ui
from load_sounds import load_sounds, play_sound
from bots.random import play_bot_move

WIDTH = HEIGHT = 800
FPS_MAX = 15
TOTAL_GAMES = 10

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    game_ui.load_images()
    sounds = load_sounds()

    results = {'White Wins': 0, 'Black Wins': 0, 'Draw': 0}

    for game_number in range(TOTAL_GAMES):

        gs = chess_board.GameState()
        gs.setup_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        
        valid_moves = gs.get_valid_moves()
        move_made = False
        game_over = False

        while not game_over:
            bot_move = play_bot_move(gs)
            if bot_move:
                gs.make_move(bot_move, is_final_move=True)
                move_made = True

                if bot_move.piece_captured != "--":
                    play_sound(sounds, "capture")
                else:
                    play_sound(sounds, "move")

            if gs.checkmate:
                if gs.white_to_move:
                    results['Black Wins'] += 1
                    print(f"Game {game_number + 1}: Black wins!")
                else:
                    results['White Wins'] += 1
                    print(f"Game {game_number + 1}: White wins!")
                play_sound(sounds, "mate")
                game_over = True
            elif gs.stalemate:
                results['Draw'] += 1
                print(f"Game {game_number + 1}: Stalemate")
                play_sound(sounds, "check")
                game_over = True
            elif gs.repetition_draw:
                results['Draw'] += 1
                print(f"Game {game_number + 1}: Draw by repetition")
                play_sound(sounds, "check")
                game_over = True
            elif gs.is_insufficient_material():
                results['Draw'] += 1
                print(f"Game {game_number + 1}: Draw by insufficient material")
                game_over = True
            elif gs.MoveCount >= 50:
                results['Draw'] += 1
                print(f"Game {game_number + 1}: Draw by 50-move rule")
                game_over = True

            if move_made:
                valid_moves = gs.get_valid_moves()
                move_made = False

            game_ui.draw_game_state(screen, gs, valid_moves, ())
            clock.tick(FPS_MAX)
            p.display.flip()


        print(f"Final FEN for Game {game_number + 1}: {gs.getPosKey()}")


    print("\n--- Final Stats ---")
    print(f"Total Games: {TOTAL_GAMES}")
    print(f"White Wins: {results['White Wins']}")
    print(f"Black Wins: {results['Black Wins']}")
    print(f"Draws: {results['Draw']}")

if __name__ == "__main__":
    main()
