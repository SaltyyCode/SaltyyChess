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

    def makeMove(self, move):
        
        if not self.redoLog:
            self.board[move.startRow][move.startCol] = '--'
            self.board[move.endRow][move.endCol] = move.movedPiece
            self.moveLog.append(move) 
            self.whiteMove = not self.whiteMove 
            self.redoLog.clear()
        else:
            print("Un redo est disponible, vous ne pouvez pas faire un nouveau coup maintenant.")
    
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
        print(self.moveID) 


    def __eq__(self, other):

        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False