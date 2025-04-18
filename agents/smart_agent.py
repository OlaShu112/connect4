from connect4.game_utils import COLUMN_COUNT, ROW_COUNT, valid_move, check_win, make_move
from connect4.agents.random_agent import random_agent


# ================================
# Smart AI Agent (Rule-Based)
# ================================


def smart_agent(board, player):
    # Step 1: Checking if the agent can win on the next move (Offensive Play)
    win_col = find_win_move(board, player)
    if win_col is not None:
        return win_col
    
    # Step 2: Checking if the opponent can win and block them (Defensive Play)
    block_col = block_player_move(board, player)
    if block_col is not None:
        return block_col
    
    # Step 3: Setting up for a future win by placing in strategic positions
    setup_col = find_setup_move(board, player)
    if setup_col is not None:
        return setup_col

    # Step 4: If no immediate moves, fallback to random play
    return random_agent(board, player)

def find_win_move(board, player):
    from connect4.main import make_move 

    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            row = make_move(board, col, player)
            if check_win(board, player):
                board[row][col] = 0  
                return col
            board[row][col] = 0  
    return None  

def block_player_move(board, player):
    opponent = 3 - player  
    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            row = make_move(board, col, opponent)
            if check_win(board, opponent):
                board[row][col] = 0 
                return col
            board[row][col] = 0  
    return None  # No need to block

def find_setup_move(board, player):
    # Priority 1: Look for positions that will help the player create two-in-a-row
    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            row = make_move(board, col, player)
            if can_create_setup(board, player):
                board[row][col] = 0  
                return col
            board[row][col] = 0  
    return None  # No setup move found

def can_create_setup(board, player):
    # Horizontal, vertical, and diagonal checks for 2-in-a-row with an empty spot
    return any([
        check_two_in_a_row(board, player, direction='horizontal'),
        check_two_in_a_row(board, player, direction='vertical'),
        check_two_in_a_row(board, player, direction='diagonal')
    ])

def check_two_in_a_row(board, player, direction):
    if direction == 'horizontal':
        return check_horizontal(board, player)
    elif direction == 'vertical':
        return check_vertical(board, player)
    elif direction == 'diagonal':
        return check_diagonal(board, player)
    return False

def check_horizontal(board, player):
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - 2):
            window = board[row][col:col+3]
            if window.count(player) == 2 and window.count(0) == 1:
                return True
    return False

def check_vertical(board, player):
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 2):
            window = [board[row+i][col] for i in range(3)]
            if window.count(player) == 2 and window.count(0) == 1:
                return True
    return False

def check_diagonal(board, player):
    # Check positively sloped diagonals
    for row in range(ROW_COUNT - 2):
        for col in range(COLUMN_COUNT - 2):
            window = [board[row+i][col+i] for i in range(3)]
            if window.count(player) == 2 and window.count(0) == 1:
                return True

    # Check negatively sloped diagonals
    for row in range(2, ROW_COUNT):
        for col in range(COLUMN_COUNT - 2):
            window = [board[row-i][col+i] for i in range(3)]
            if window.count(player) == 2 and window.count(0) == 1:
                return True

    return False
