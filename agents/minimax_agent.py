
from connect4.game_utils import COLUMN_COUNT, valid_move, make_move, check_win

# ================================
# MiniMax AI Agent (With Alpha-Beta Pruning)
# ================================
def minimax_agent(board, player):
    # This function will return the best column for the minimax agent
    best_col = None
    best_score = -float('inf')
    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            temp_board = [row[:] for row in board]  # Copy the board
            row = make_move(temp_board, col, player)
            score = minimax(temp_board, 3, -float('inf'), float('inf'), False, player)
            if score > best_score:
                best_score = score
                best_col = col
    return best_col

def minimax(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or check_win(board, 1) or check_win(board, 2):
        return evaluate_board(board, player)

    if maximizing_player:
        max_eval = -float('inf')
        for col in range(COLUMN_COUNT):
            if valid_move(board, col):
                temp_board = [row[:] for row in board]  # Copy the board
                row = make_move(temp_board, col, player)
                eval = minimax(temp_board, depth - 1, alpha, beta, False, player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:  # Beta cut-off
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for col in range(COLUMN_COUNT):
            if valid_move(board, col):
                temp_board = [row[:] for row in board]  # Copy the board
                row = make_move(temp_board, col, 3 - player)
                eval = minimax(temp_board, depth - 1, alpha, beta, True, player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:  # Alpha cut-off
                    break
        return min_eval

def evaluate_board(board, player):
    """Evaluates the board, taking into account the potential for creating 2- or 3-piece streaks"""
    score = 0
    # Horizontal check
    for r in range(len(board)):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r][c + i] for i in range(4)]
            score += evaluate_window(window, player)

    # Vertical check
    for c in range(COLUMN_COUNT):
        for r in range(len(board) - 3):
            window = [board[r + i][c] for i in range(4)]
            score += evaluate_window(window, player)

    # Positive diagonal check
    for r in range(len(board) - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, player)

    # Negative diagonal check
    for r in range(3, len(board)):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

def evaluate_window(window, player):
    score = 0
    opp_player = 3 - player
    if window.count(player) == 4:
        score += 100  # Win
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5  # Potential for a 4-piece streak
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2  # Potential for a 3-piece streak
    elif window.count(opp_player) == 3 and window.count(0) == 1:
        score -= 4  # Block opponent's 3-piece streak
    elif window.count(opp_player) == 2 and window.count(0) == 2:
        score -= 2  # Block opponent's 2-piece streak
    return score
