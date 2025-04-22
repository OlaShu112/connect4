import random
import numpy as np
import pandas as pd
from connect4.constants import SQUARE_SIZE
from connect4.graphics import draw_board
from sklearn.preprocessing import LabelEncoder
from connect4.message import display_message

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

def get_available_columns(board):
    """
    Returns a list of columns that still have empty spots.
    """
    available_columns = []
    for col in range(len(board[0])):
        if board[0][col] == 0:  # Assuming 0 represents an empty spot
            available_columns.append(col)
    return available_columns

def preprocess_data(dataset_path, names_path):
    import pandas as pd

    print("Dataset loaded successfully.")
    df = pd.read_csv(dataset_path, header=None)

    print("Feature names loaded successfully.")
    with open(names_path, "r") as f:
        lines = f.readlines()
    feature_names = [line.strip() for line in lines if line.strip()]

    if df.isnull().values.any():
        print("Warning: Missing values found in the dataset.")
        df = df.dropna()

    print("Dataset shape after cleaning:", df.shape)

    # Assuming the last column is the target label
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    print("Feature conversion complete.")
    print("Data sample after conversion:")
    print(X.head())

    return X, y

def easy_ai_move(board, turn):
    from connect4.agents.random_agent import random_agent
    return random_agent(board, turn)

def medium_ai_move(board, turn):
    from connect4.agents.minimax_agent import minimax_agent
    return minimax_agent(board, turn, depth=3)

def hard_ai_move(board, turn, model):
    from connect4.agents.ml_agent import ml_agent
    return ml_agent(board, turn, model)

def ai_move(board, agent, turn, label, screen):
    opponent = 1 if turn == 2 else 2
    # Import block_player_move inside this function to prevent circular import
    from connect4.game_help import block_player_move
    block_col = block_player_move(board, opponent)

    # Attempt to block opponent if a blocking move is found
    if block_col != -1 and valid_move(board, block_col):
        col = block_col
    else:
        try:
            if agent.__name__ == "ml_agent":
                col = agent(board, turn, None)  # Assuming model is None for now
            else:
                col = agent(board, turn)
        except Exception as e:
            print(f"AI move generation failed for {label}: {e}")
            return False

    try:
        col = int(float(col))
    except (ValueError, TypeError):
        print(f"Invalid column received from {label}: {col}")
        return False

    valid_cols = [c for c in range(len(board[0])) if board[0][c] == 0]
    if col not in valid_cols:
        print(f"{label} couldn't find a valid move. Skipping turn.")
        return False

    row = drop_piece(board, col, turn)
    if row != -1:
        draw_board(board, turn, screen)

        if check_win(board, turn):
            display_message(f"{label} wins!")
            return True
        elif board_is_full(board):
            display_message("It's a draw!")
            return True

        draw_board(board, switch_turn(turn), screen)
    return False
