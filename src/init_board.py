def init_chessboard():

    board = [[""for _ in range(8)] for _ in range(8)] #empty chessboard

    for i in range(8):
        board[1][i] = 'pawn_black'
        board[6][i] = 'pawn_white'
    board[0][0] = board[0][7] = 'rook_black'
    board[7][0] = board[7][7] = 'rook_white'
    board[0][1] = board[0][6] = 'knight_black'
    board[7][1] = board[7][6] = 'knight_white'
    board[0][2] = board[0][5] = 'bishop_black'
    board[7][2] = board[7][5] = 'bishop_white'
    board[0][3] = 'queen_black'
    board[7][3] = 'queen_white'
    board[0][4] = 'king_black'
    board[7][4] = 'king_white'

    return board