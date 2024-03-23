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
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],] # Init state of board.
        self.whiteMove = True
        self.moveLog = [] # Move history list.
        self.redoLog = [] # stores undo-ed moves in list to redo after.
        self.moveFunc = {'p': self.pawnMove, 'N': self.knightMoves,
                         'B': self.bishopMove, 'Q': self.queenMoves,
                         'K': self.kingMove, 'R': self.rookMove}
        self.pins = []
        self.checks = []
        self.wkLoc = (7, 4)
        self.bKloc = (0,4)
        self.CheckMate = False
        self.staleMate = False 
        self.MoveHistory = {}
        self.MoveCount = 0
        self.Draw = False
        self.GameOver = False
        
    def         

    def makeMove(self, move, capture_sound=None):
        
            self.board[move.startRow][move.startCol] = '--' # Replace starting square by empty space.
            if self.board[move.endRow][move.endCol] != '--':
                if capture_sound:
                    capture_sound.play()
            self.board[move.endRow][move.endCol] = move.movedPiece
            self.moveLog.append(move) 
            self.whiteMove = not self.whiteMove # Change flag to allow opp to play
            self.redoLog.clear() 
            if move.movedPiece == 'wK':
                self.wkLoc = (move.endRow, move.endCol)
            elif move.movedPiece == 'bK':
                self.bKloc = (move.endRow, move.endCol)
                
            posKey = self.getPosKey()
            if posKey in self.MoveHistory:
                self.MoveHistory[posKey] += 1
            else:
                self.MoveHistory[posKey] = 1
            
            if move.movedPiece[1] == 'p' or move.capturedPiece != '':
                self.MoveCount = 0
            else:
                self.MoveCount += 1
                if self.MoveCount == 100:
                    self.Draw = True
            self.CheckGameStatus()
                    
    
    def getPosKey(self):
        
        posKey = ''.join([''.join(row) for row in self.board]) # Converts the 2D list representation of a chess board into a single string
        return posKey;
    
    
    def undo(self): # Go back to previous moves.*

        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.movedPiece
            self.board[move.endRow][move.endCol] = move.capturedPiece
            self.whiteMove = not self.whiteMove
            self.redoLog.append(move)
            if move.movedPiece == 'wK':
                self.wkLoc = (move.startRow, move.startCol) # Always keep track of king position 
            elif move.movedPiece == 'bK':
                self.bKloc = (move.startRow, move.startCol)
                
        

    def redo(self): 

        if len(self.redoLog) > 0:
            move = self.redoLog.pop()
            self.board[move.startRow][move.startCol] = '--'
            self.board[move.endRow][move.endCol] = move.movedPiece
            self.whiteMove = not self.whiteMove
            self.moveLog.append(move)
            if move.movedPiece == 'wK':
                self.wkLoc = (move.endRow, move.endCol) # Double check king location like in undo 
            elif move.movedPiece == 'bK':
                self.bKloc = (move.endRow, move.endCol)



    def getvalidMoves(self):

        moves = self.getallMoves()
        for i in range(len(moves)-1, -1, -1): # Check the list of moves in decreasing order
            self.makeMove(moves[i])
            self.whiteMove = not self.whiteMove # Switch to other player
            if self.IsCheck():
                moves.remove(moves[i])  # If there is a check, the move is removed from the list 
            self.whiteMove = not self.whiteMove  # Comeback to actual player
            self.undo() # Dont allow the move
        
        if len(moves) == 0:
            
            if self.IsCheck():
                self.CheckMate = True
                print("GG y'a mat")
                      
            else:
                self.staleMate = True
                print("Nulle :(")
        else:
            self.CheckMate = False # In case of undo / redo
            self.staleMate = False
            
        posKey = self.getPosKey()
        if self.MoveHistory.get(posKey, 0) >= 6: # Check the string to see if the current pos already occured s
            self.Draw = True
            print("Draw with repetition")
        else:
            self.Draw = False
        
        return moves
    
    def IsCheck(self):

        if self.whiteMove:
            return self.AttackedSquare(self.wkLoc[0], self.wkLoc[1]) # Check is white king is attacked; if return True, yes and so check
        else:
            return self.AttackedSquare(self.bKloc[0], self.bKloc[1])
        

    def AttackedSquare(self, r, c):

        self.whiteMove = not self.whiteMove 
        oppMoves = self.getallMoves()
        self.whiteMove = not self.whiteMove
        for move in oppMoves: # Check all moves for opponent
            if move.endRow == r and move.endCol == c: # If a move ends on our col anb our row
                return True # The square is attacked 
        return False


    
    def getallMoves(self):

        moves = []

        for r in range (len(self.board)):
            for c in range (len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteMove) or (turn == 'b' and not self.whiteMove):
                    piece = self.board[r][c][1]
                    self.moveFunc[piece](r, c, moves) # Uses a function dictionary to check pieces moves.
        return moves


    def pawnMove(self, r, c, moves):
        if self.whiteMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: # Diagonal capture.
                if self.board[r-1][c-1][0] == 'b':
                 moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: # Same as previous but for right capture.
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else: # For black pawns.
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
        
        dir = ((-1, 0), (0, -1), (1, 0), (0, 1)) # Directions where rook can go (up/left/down/right).
        othercolor = "b" if self.whiteMove else "w"

        for d in dir:
            for x in range(1, 8): # Rook can move on all the available col or row.
                endRow = r + d[0] * x 
                endCol = c + d[1] * x # x = num of squares we want the rook to travel.
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == othercolor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # If enPiece = same color.
                        break
                else : # If endPiece = out of board.
                    break

    def kingMove(self, r, c, moves):

        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)) # King moves in every direction.
        opponentColor = "b" if self.whiteMove else "w"

        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] == opponentColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
        
    def bishopMove(self, r, c, moves):

        dir = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # Only diagonals moves here.
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

    def queenMoves(self, r, c, moves): # Queen is litteraly Bishop & Rook moves.
        
        self.bishopMove(r, c, moves)
        self.rookMove(r, c, moves)
    
    def knightMoves(self, r, c, moves):
    
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)] # Knight moves in L style, so we go one square in 1 direction then 2 in an opposite one.
        allyColor = "w" if self.whiteMove else "b"

        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():

    # Dictionaries for converting ranks and files between algebraic notation (used in chess) and list indices used in the program.
    rankstoRow = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    filestoCols = {"a": 7, "b": 6, "c": 5, "d": 4, 
                   "e": 3, "f": 2, "g": 1, "h": 0}
    
    # Inverting the previous dictionaries for converting list indices back to algebraic notation.
    rowtoRanks = {v: k for k, v in rankstoRow.items()}
    colstoFiles = {v: k for k, v in filestoCols.items()}

    def __init__(self, stSquare, endSquare, board):

        # Initializing a move with the starting position, ending position, and the current state of the board to determine moved and captured pieces.
        self.startRow = stSquare[0]
        self.startCol = stSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.movedPiece = board[self.startRow][self.startCol]
        self.capturedPiece = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, other):

        # Method for comparing two moves, useful for checking if a given move has already been made.
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
