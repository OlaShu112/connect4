from connect4.game_utils import valid_move, drop_piece, check_win, COLUMN_COUNT, ROW_COUNT



def block_player_move(board, player):
    for col in range(len(board[0])): 
        if valid_move(board, col):  
            temp_board = [row.copy() for row in board]
            row = drop_piece(temp_board, col, player)  
            if check_win(temp_board, player):  # Check if the opponent wins
                return col  # Block the winning move by returning the column
    return -1
