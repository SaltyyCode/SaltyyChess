import random
import chess_board

class RandomBot: 
    def __init__(self, game_state):
        self.game_state = game_state

    def get_best_move(self):
        valid_moves = self.game_state.get_valid_moves()
        return random.choice(valid_moves) if valid_moves else None  #Litteraly plays randomly

def play_bot_move(game_state):
    bot = RandomBot(game_state)
    move = bot.get_best_move()
    if move:
        game_state.make_move(move)