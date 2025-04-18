from connect4.constants import SQUARE_SIZE
from connect4.message import display_message, ask_play_again, main_menu, difficulty_menu
from connect4.graphics import draw_board


COLUMN_COUNT = 7
ROW_COUNT = 6

def create_board():
    return [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

def drop_piece(board, col, player):
    col = int(float(col))  
    if col < 0 or col >= COLUMN_COUNT:
        return -1 

    for row in range(ROW_COUNT - 1, -1, -1): 
        if board[row][col] == 0: 
            board[row][col] = player  
            return row  
    return -1  


def valid_move(board, col):
    col = int(float(col))
    return 0 <= col < COLUMN_COUNT and board[0][col] == 0

def make_move(board, col, player):
    for row in range(ROW_COUNT - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return row
    return None

def check_win(board, piece):
    # Horizontal check
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Positive diagonal check
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Negative diagonal check
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

def switch_turn(turn):
    return 2 if turn == 1 else 1

def get_column_from_mouse(event):
    return event.pos[0] // SQUARE_SIZE

def board_is_full(board):
    return all(board[0][c] != 0 for c in range(len(board[0])))

def ai_move(board, agent, turn, label, screen):
    opponent = 1 if turn == 2 else 2
    block_col = block_player_move(board, opponent)

    if block_col != -1:
        row = drop_piece(board, block_col, turn)
        if row != -1:
            if check_win(board, turn):
                draw_board(board, turn, screen)  
                display_message(f"{label} wins!")
                return True
            elif board_is_full(board):
                draw_board(board, turn, screen)
                display_message("It's a draw!")
                return True
            draw_board(board, switch_turn(turn), screen)
        return False

    col = agent(board, turn)
    try:
        col = int(float(col))
    except (ValueError, TypeError):
        print(f"Invalid column received from {label}: {col}")
        col = -1
    valid_cols = [c for c in range(len(board[0])) if board[0][c] == 0]
    if col not in valid_cols:
        print(f"{label} couldn't find a valid move. Skipping turn.")
        return False

    row = drop_piece(board, col, turn)
    if row != -1:
        if check_win(board, turn):
            draw_board(board, turn, screen)
            display_message(f"{label} wins!")
            return True
        elif board_is_full(board):
            draw_board(board, turn, screen)
            display_message("It's a draw!")
            return True
        draw_board(board, switch_turn(turn), screen)
    return False

def block_player_move(board, player):
    for col in range(len(board[0])): 
        if valid_move(board, col):  
           
            temp_board = [row.copy() for row in board]
            row = drop_piece(temp_board, col, player)  
            if check_win(temp_board, player):  # Check if the opponent wins
                return col  # Block the winning move by returning the column
    return -1
