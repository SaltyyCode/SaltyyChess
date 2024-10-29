class GameState:
    def __init__(self):
        # Initialisation des attributs de GameState
        self.board = [["--" for _ in range(8)] for _ in range(8)]
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.repetition_draw = False
        self.en_passant_possible = ()
        self.MoveHistory = {}
        self.MoveCount = 0
        self.castling_rights = CastlingRights(True, True, True, True)
        self.castling_rights_log = [CastlingRights(True, True, True, True)]
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.move_functions = {
            'P': self.pawnMove,
            'R': self.rookMove,
            'N': self.knightMoves,
            'B': self.bishopMove,
            'Q': self.queenMoves,
            'K': self.kingMove
        }

    def setup_from_fen(self, fen):
        piece_mapping = {
            "R": "Rook", "N": "N", "B": "Bishop", "Q": "Queen", "K": "King", "P": "Pawn"
        }
        
        parts = fen.split()
        piece_placement = parts[0]
        rows = piece_placement.split('/')
        for r, row in enumerate(rows):
            col = 0
            for char in row:
                if char.isdigit():
                    col += int(char)
                else:
                    color = 'w' if char.isupper() else 'b'
                    piece_type = piece_mapping[char.upper()]
                    self.board[r][col] = color + piece_type
                    col += 1

        self.white_to_move = (parts[1] == 'w')
        castling_rights = parts[2]
        self.castling_rights = CastlingRights(
            'K' in castling_rights,
            'Q' in castling_rights,
            'k' in castling_rights,
            'q' in castling_rights
        )
        en_passant = parts[3]
        if en_passant != '-':
            file, rank = en_passant[0], en_passant[1]
            self.en_passant_possible = (8 - int(rank), ord(file) - ord('a'))
        else:
            self.en_passant_possible = ()
        self.halfmove_clock = int(parts[4])
        self.fullmove_number = int(parts[5])


    def make_move(self, move, is_final_move=False):
        # Exécution du mouvement
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        # Mettre à jour les positions du roi
        if move.piece_moved == "wKing":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bKing":
            self.black_king_location = (move.end_row, move.end_col)

        # Promotion et capture en passant
        if move.pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Queen'
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = '--'

        # Mettre à jour la possibilité de prise en passant
        if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
            self.en_passant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.en_passant_possible = ()

        # Mouvements de roque
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = '--'
            else:
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = '--'

        # Mise à jour des droits de roque
        self.update_castling_rights(move)
        self.castling_rights_log.append(CastlingRights(self.castling_rights.wks, self.castling_rights.bks,
                                                    self.castling_rights.wqs, self.castling_rights.bqs))

        # Ajouter à MoveHistory seulement si c'est un mouvement final
        if is_final_move:
            posKey = self.getPosKey()
            self.MoveHistory[posKey] = self.MoveHistory.get(posKey, 0) + 1

            # Gestion de la règle des 50 coups
            if move.piece_moved[1] == 'P' or move.piece_captured != '--':
                self.MoveCount = 0
            else:
                self.MoveCount += 1
                print(f"Nombre de coups depuis la dernière capture ou mouvement de pion : {self.MoveCount}")
                if self.MoveCount == 50:
                    self.stalemate = True  # Match nul selon la règle des 50 coups

            # Vérification de la règle de matériel insuffisant
            if self.is_insufficient_material():
                self.stalemate = True
                print("Match nul pour cause de matériel insuffisant")

    def is_insufficient_material(self):

        white_material = []
        black_material = []
        for row in self.board:
            for square in row:
                if square != "--":
                    if square[0] == "w":
                        white_material.append(square[1])
                    else:
                        black_material.append(square[1])

        # Conditions de nulle par insuffisance de matériel
        if white_material == ["K"] and black_material == ["K"]:
            return True  # Roi contre roi
        if (white_material == ["K", "N"] and black_material == ["K"]) or (white_material == ["K"] and black_material == ["K", "N"]):
            return True  # Roi et cavalier contre roi
        if (white_material == ["K", "B"] and black_material == ["K"]) or (white_material == ["K"] and black_material == ["K", "B"]):
            return True  # Roi et fou contre roi
        if (white_material == ["K", "N"] and black_material == ["K", "B"]) or (white_material == ["K", "B"] and black_material == ["K", "N"]):
            return True  # Roi et cavalier contre roi et fou

        return False


            
    def undo_move(self):

        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            if move.piece_moved == "wKing":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bKing":
                self.black_king_location = (move.start_row, move.start_col)

            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = '--'
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.en_passant_possible = (move.end_row, move.end_col)
            if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
                self.en_passant_possible = ()

            self.castling_rights_log.pop()
            new_rights = self.castling_rights_log[-1]
            self.castling_rights = CastlingRights(new_rights.wks, new_rights.bks, new_rights.wqs, new_rights.bqs)

            if move.is_castle_move:
                if move.end_col - move.start_col == 2:
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = '--'
                else:
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = '--'

    def get_valid_moves(self):

        temp_en_passant_possible = self.en_passant_possible
        temp_castling_rights = CastlingRights(self.castling_rights.wks, self.castling_rights.bks, self.castling_rights.wqs, self.castling_rights.bqs)
        moves = self.get_all_possible_moves()

        if self.white_to_move:
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()

        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        posKey = self.getPosKey()
        if posKey not in self.MoveHistory:
            self.MoveHistory[posKey] = 1
        else:
            self.MoveHistory[posKey] += 1

        #print(f"Position FEN: {posKey}, Repetitions: {self.MoveHistory[posKey]}")

        if self.MoveHistory[posKey] >= 3:
            self.repetition_draw = True
            if self.MoveHistory[posKey] == 3:  # Afficher une seule fois
                print("Draw by repetition")
        else:
            self.repetition_draw = False

        # Restauration des variables temporaires
        self.en_passant_possible = temp_en_passant_possible
        self.castling_rights = temp_castling_rights
        return moves



    
    def getPosKey(self):
        posKey = ''
        for row in self.board:
            empty_squares = 0
            for piece in row:
                if piece == '--':  # Case vide
                    empty_squares += 1
                else:
                    if empty_squares > 0:
                        posKey += str(empty_squares)
                        empty_squares = 0
                    posKey += piece
            if empty_squares > 0:
                posKey += str(empty_squares)
            posKey += '/'  # Séparateur de lignes

        # Ajout d'informations supplémentaires
        posKey += f" {'w' if self.white_to_move else 'b'}"  # Indique le joueur
        posKey += f" KQkq"  # Ajoute les droits de roque
        posKey += f" {self.en_passant_possible if self.en_passant_possible else '-'}"  # Ajoute la case de prise en passant

        return posKey


    def in_check(self):

        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, r, c):

        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opponent_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False

    def get_all_possible_moves(self):

        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece in self.move_functions:
                        self.move_functions[piece](r, c, moves)
        return moves

    def pawnMove(self, r, c, moves):

        if self.white_to_move:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, is_enpassant_move=True))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, is_enpassant_move=True))
        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, is_enpassant_move=True))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, is_enpassant_move=True))

    def rookMove(self, r, c, moves):
    
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.white_to_move else "w"

        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def bishopMove(self, r, c, moves):

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = "b" if self.white_to_move else "w"

        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break
                
    def knightMoves(self, r, c, moves):

        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        ally_color = "w" if self.white_to_move else "b"
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def queenMoves(self, r, c, moves):

        self.rookMove(r, c, moves)
        self.bishopMove(r, c, moves)

    def kingMove(self, r, c, moves):

        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = "w" if self.white_to_move else "b"

        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_castle_moves(self, r, c, moves):

        if self.square_under_attack(r, c):
            return
        if (self.white_to_move and self.castling_rights.wks) or (not self.white_to_move and self.castling_rights.bks):
            self.get_king_side_castle_moves(r, c, moves)
        if (self.white_to_move and self.castling_rights.wqs) or (not self.white_to_move and self.castling_rights.bqs):
            self.get_queen_side_castle_moves(r, c, moves)

    def get_king_side_castle_moves(self, r, c, moves):

        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.square_under_attack(r, c + 1) and not self.square_under_attack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, is_castle_move=True))

    def get_queen_side_castle_moves(self, r, c, moves):

        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.square_under_attack(r, c - 1) and not self.square_under_attack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, is_castle_move=True))
    
    def update_castling_rights(self, move):

        if move.piece_moved == 'wKing':
            self.castling_rights.wks = False
            self.castling_rights.wqs = False
        elif move.piece_moved == 'bKing':
            self.castling_rights.bks = False
            self.castling_rights.bqs = False
        elif move.piece_moved == "wRook":
            if move.start_col == 0:
                self.castling_rights.wqs = False
            elif move.start_col == 7:
                self.castling_rights.wks = False
        elif move.piece_moved == "bRook":
            if move.start_col == 0:
                self.castling_rights.bqs = False
            elif move.start_col == 7:
                self.castling_rights.bks = False


class CastlingRights:

    def __init__(self, wks, bks, wqs, bqs):

        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move:

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant_move=False, is_castle_move=False):
    
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.pawn_promotion = (self.piece_moved == "wPawn" and self.end_row == 0) or (self.piece_moved == "bPawn" and self.end_row == 7)
        self.is_enpassant_move = is_enpassant_move
    
        if self.is_enpassant_move:
            self.piece_captured = "wPawn" if self.piece_moved == "bPawn" else "bPawn"
        self.is_castle_move = is_castle_move

        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):

        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):

        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):

        return self.cols_to_files[c] + self.rows_to_ranks[r]
