import random
from connect4.game_utils import COLUMN_COUNT, valid_move, make_move, check_win

# ================================
# Random AI Agent
# ================================
def random_agent(board, player):
    # First, check if the agent can win immediately
    win_col = find_win_move(board, player)
    if win_col is not None:
        return win_col
    
    # Then, check if the player can win and block that move
    block_col = block_player_move(board, player)
    if block_col is not None:
        return block_col
    
    # After that, try to play in the center columns for better positioning
    middle_columns = [3, 2, 4, 1, 5, 0, 6]  # Prioritize the center
    for col in middle_columns:
        if valid_move(board, col):
            return col
    
    # If no preferred move, pick a random valid column
    return random.choice([col for col in range(COLUMN_COUNT) if valid_move(board, col)])

def find_win_move(board, player):
    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            row = make_move(board, col, player)
            if check_win(board, player):
                board[row][col] = 0  
                return col
            board[row][col] = 0  
    return None  # No winning move available

def block_player_move(board, player):
    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            # Try placing the player's piece temporarily
            row = make_move(board, col, player)
            if check_win(board, player):
                board[row][col] = 0  # Undo the move
                return col
            board[row][col] = 0  # Undo the move
    return None  # No immediate threat