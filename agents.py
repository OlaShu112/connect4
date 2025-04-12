import random
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# Constants for the game
COLUMN_COUNT = 7
ROW_COUNT = 6

def valid_move(board, col):
    return board[0][col] == 0

def make_move(board, col, player):
    for row in range(ROW_COUNT - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return row
    return None

def check_win(board, player):
    # Check horizontal, vertical, and diagonal win conditions
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    for row in range(3, ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

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
            score = minimax(temp_board, 3, False, player)
            if score > best_score:
                best_score = score
                best_col = col
    return best_col

def minimax(board, depth, maximizing_player, player):
    if depth == 0 or check_win(board, 1) or check_win(board, 2):
        return evaluate_board(board, player)

    if maximizing_player:
        max_eval = -float('inf')
        for col in range(COLUMN_COUNT):
            if valid_move(board, col):
                temp_board = [row[:] for row in board]  # Copy the board
                row = make_move(temp_board, col, player)
                eval = minimax(temp_board, depth - 1, False, player)
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for col in range(COLUMN_COUNT):
            if valid_move(board, col):
                temp_board = [row[:] for row in board]  # Copy the board
                row = make_move(temp_board, col, 3 - player)
                eval = minimax(temp_board, depth - 1, True, player)
                min_eval = min(min_eval, eval)
        return min_eval

def evaluate_board(board, player):
    # A simple evaluation function for Minimax
    if check_win(board, player):
        return 100
    elif check_win(board, 3 - player):
        return -100
    return 0

# ================================
# Random AI Agent
# ================================
def random_agent(board, player):
    """
    A more professional random agent:
    - Blocks the player's winning move if possible.
    - Tries to win if a winning move exists.
    - Prioritizes central columns for better control of the game.
    - Randomly chooses from available columns if no immediate move.
    """
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
    """
    Checks if the player can win on the next move.
    If a winning move exists, return the column to play.
    """
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
    AI will block the player's winning move if possible.
    If a winning move exists for the player, the AI will block it.
    Returns the column to block.
    """
    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            # Try placing the player's piece temporarily
            row = make_move(board, col, player)
            if check_win(board, player):
                board[row][col] = 0  # Undo the move
                return col
            board[row][col] = 0  # Undo the move
    return None  # No immediate threat

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

# ================================
# Machine Learning Agent (Placeholder)
# ================================

# Load the dataset
data = pd.read_csv("connect4_dataset/connect-4.data", header=None, low_memory=False)

# Load the feature names (column names) from the .names file
with open("connect4_dataset/connect-4.names") as f:
    lines = f.readlines()

# Extract only the first 42 lines containing board positions (a1 to g6)
features = [line.split(':')[0].strip() for line in lines if ':' in line][:42]

# Debug print to confirm correct number of features
assert len(features) == 42, f"Expected 42 feature names, but found {len(features)}"

# Set the feature columns plus the 'winner' column
data.columns = features + ['winner']

# Drop rows where 'winner' is missing or not a string
data = data[data['winner'].apply(lambda x: isinstance(x, str))]

# Separate features and target
X = data.drop('winner', axis=1)
y = data['winner']

# Encode the target labels (winner) into numbers
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Function to convert board positions ('pos_01', 'pos_02', ...) into numeric values
def convert_board_positions_to_numeric(df):
    for column in df.columns:
        if df[column].dtype == 'object':  # Check if the column is categorical
            # Apply conversion only to valid strings with '_'
            df[column] = df[column].apply(
                lambda x: int(x.split('_')[1]) if isinstance(x, str) and '_' in x else x
            )
    return df

# Convert the board positions in X into numeric values
X = convert_board_positions_to_numeric(X)

# Ensure that all columns in X are numeric after conversion
for column in X.columns:
    # If a column is still not numeric, attempt to convert it
    if X[column].dtype == 'object':
        X[column] = pd.to_numeric(X[column], errors='coerce')

# Drop any rows with NaN values that couldn't be converted
X = X.dropna()

# Ensure that all columns in X are now numeric
assert all(np.issubdtype(X[col], np.number) for col in X.columns), "Not all columns are numeric."

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Function to predict the best move — placeholder logic
def predict_move(board):
    # Flatten the board (6x7) to a 1D array
    feature_vector = np.array(board).flatten().reshape(1, -1)

    # Predict the outcome (not the move yet)
    prediction = model.predict(feature_vector)

    # Decode prediction back to label
    predicted_label = label_encoder.inverse_transform(prediction)[0]

    return predicted_label  # Placeholder: not an actual move column yet

# ML agent function to be used by the game
def ml_agent(board, player):
    return predict_move(board)