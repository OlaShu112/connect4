from connect4.game_utils import COLUMN_COUNT, ROW_COUNT, valid_move, check_win, make_move
from connect4.agents.random_agent import random_agent






# ================================
# Smart AI Agent (Rule-Based)
# ================================


def smart_agent(board, player):
    """
    A smart agent that:
    1. Prioritizes immediate winning moves.
    2. Blocks the opponent's winning move if possible.
    3. Creates strategic setups for future wins.
    4. Falls back to random moves if no immediate options exist.
    """
    # Step 1: Check if the agent can win on the next move (Offensive Play)
    win_col = find_win_move(board, player)
    if win_col is not None:
        return win_col
    
    # Step 2: Check if the opponent can win and block them (Defensive Play)
    block_col = block_player_move(board, player)
    if block_col is not None:
        return block_col
    
    # Step 3: Try to set up for a future win by placing in strategic positions
    setup_col = find_setup_move(board, player)
    if setup_col is not None:
        return setup_col

    # Step 4: If no immediate moves, fallback to random play
    return random_agent(board, player)

def find_win_move(board, player):
    """
    Checks if the player can win on the next move.
    If a winning move exists, return the column to play.
    """
    from connect4.main import make_move  # Lazy import here

    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            row = make_move(board, col, player)
            if check_win(board, player):
                board[row][col] = 0  # Undo the move
                return col
            board[row][col] = 0  # Undo the move
    return None  # No winning move available

def block_player_move(board, player):
    """
    Checks if the opponent can win on the next move and blocks it.
    Returns the column where the agent should play to block the opponent.
    """
    opponent = 3 - player  # Opponent's player number
    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            row = make_move(board, col, opponent)
            if check_win(board, opponent):
                board[row][col] = 0  # Undo the move
                return col
            board[row][col] = 0  # Undo the move
    return None  # No need to block

def find_setup_move(board, player):
    """
    Attempts to set up the player for a future win by prioritizing plays
    that create a possible winning scenario in subsequent turns.
    """
    # Priority 1: Look for positions that will help the player create two-in-a-row
    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            row = make_move(board, col, player)
            if can_create_setup(board, player):
                board[row][col] = 0  # Undo the move
                return col
            board[row][col] = 0  # Undo the move
    return None  # No setup move found

def can_create_setup(board, player):
    """
    Checks if the current board setup has potential for a winning setup,
    like two pieces in a row, column, or diagonal with an open space.
    """
    # Horizontal, vertical, and diagonal checks for 2-in-a-row with an empty spot
    return any([
        check_two_in_a_row(board, player, direction='horizontal'),
        check_two_in_a_row(board, player, direction='vertical'),
        check_two_in_a_row(board, player, direction='diagonal')
    ])

def check_two_in_a_row(board, player, direction):
    """
    Checks for a two-in-a-row situation in the given direction where the player
    can complete a line on the next move.
    """
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
