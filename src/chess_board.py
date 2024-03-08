class GameState():
    
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],]
        self.whiteMove = True
        self.moveLog = []
        self.redoLog = []
        self.moveFunc = {'p': self.pawnMove, 'N': self.knightMoves,
                         'B': self.bishopMove, 'Q': self.queenMoves,
                         'K': self.kingMove, 'R': self.rookMove}

    def makeMove(self, move):
        
        if not self.redoLog:
            self.board[move.startRow][move.startCol] = '--'
            self.board[move.endRow][move.endCol] = move.movedPiece
            self.moveLog.append(move) 
            self.whiteMove = not self.whiteMove 
            self.redoLog.clear()
        else:
            pass
    
    def undo(self):

        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.movedPiece
            self.board[move.endRow][move.endCol] = move.capturedPiece
            self.whiteMove = not self.whiteMove
            self.redoLog.append(move)

    
    def redo(self):

        if self.redoLog:
            move = self.redoLog.pop()
            self.board[move.startRow][move.startCol] = '--'
            self.board[move.endRow][move.endCol] = move.movedPiece
            self.whiteMove = not self.whiteMove
            self.moveLog.append(move)


    def getvalidMoves(self):

        return self.getallMoves()
    
    def getallMoves(self):

        moves = []

        for r in range (len(self.board)):
            for c in range (len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteMove) or (turn == 'b' and not self.whiteMove):
                    piece = self.board[r][c][1]
                    self.moveFunc[piece](r, c, moves)
        return moves


    def pawnMove(self, r, c, moves):
        if self.whiteMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                 moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w': 
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':  
                    moves.append(Move((r, c), (r+1, c+1), self.board))
    
    def rookMove(self, r, c, moves):
        
        dir = ((-1, 0), (0, -1), (1, 0), (0, 1))
        othercolor = "b" if self.whiteMove else "w"

        for d in dir:
            for x in range(1, 8):
                endRow = r + d[0] * x
                endCol = c + d[1] * x
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == othercolor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else :
                    break

    def kingMove(self, r, c, moves):

        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        opponentColor = "b" if self.whiteMove else "w"

        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] == opponentColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
        
    def bishopMove(self, r, c, moves):

        dir = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        opponentColor = "b" if self.whiteMove else "w"

        for d in dir:
            for x in range(1, 8):
                endRow = r + d[0] * x
                endCol = c + d[1] * x
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == opponentColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def queenMoves(self, r, c, moves):
        
        self.bishopMove(r, c, moves)
        self.rookMove(r, c, moves)
    
    def knightMoves(self, r, c, moves):
    
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        allyColor = "w" if self.whiteMove else "b"  # Utilisez la couleur alliée pour la vérification

        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != allyColor:  # Case vide ou contient une pièce adverse
                    moves.append(Move((r, c), (endRow, endCol), self.board))





class Move():

    rankstoRow = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    filestoCols = {"a": 7, "b": 6, "c": 5, "d": 4, 
                   "e": 3, "f": 2, "g": 1, "h": 0}
    rowtoRanks = {v: k for k, v in rankstoRow.items()}
    colstoFiles = {v: k for k, v in filestoCols.items()}

    def __init__(self, stSquare, endSquare, board):
        self.startRow = stSquare[0]
        self.startCol = stSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.movedPiece = board[self.startRow][self.startCol]
        self.capturedPiece = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, other):

        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False