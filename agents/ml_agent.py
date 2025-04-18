import random
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from connect4.game_utils import COLUMN_COUNT, valid_move, make_move, check_win, block_player_move
from connect4.graphics import draw_board


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
    try:
        # Map player to the correct label (e.g., 'O' or 'X')
        player_label_map = {1: 'O', 2: 'X'}  # Example mapping, adapt as needed
        player_label = player_label_map[player]
        
        # Ensure the label used during prediction exists in the label encoder
        if player_label not in label_encoder.classes_:
            # If the label is not in the encoder, we add it manually
            label_encoder.fit(np.append(label_encoder.classes_, player_label))
        
        # Transform the player label for prediction
        class_index = label_encoder.transform([player_label])[0]
        
        prediction = predict_move(board)
        
        # Only accept the prediction if it's a valid column (0–6) and the move is allowed
        if isinstance(prediction, int) and 0 <= prediction < COLUMN_COUNT and valid_move(board, prediction):
            return prediction
    except Exception as e:
        print(f"Error during ML agent move: {e}")
        pass

    # Fallback: return a random valid column
    valid_columns = [col for col in range(COLUMN_COUNT) if valid_move(board, col)]
    if valid_columns:
        return random.choice(valid_columns)
    else:
        return None  # Board full or error — no valid moves


# ============================
# CRITICAL LIMITATION (for evaluation)
# ============================
# The model predicts the *game outcome* (winner label: 'win', 'loss', 'draw') 
# based on the current board state — NOT the optimal move (i.e., column number 0–6).
# Therefore, the ML agent cannot choose strategic moves directly from the model.
# It instead selects randomly from valid columns when prediction is unsuitable.
# 
# This limits the agent's gameplay ability — it cannot "learn" to play.
# A future enhancement would involve training the model to predict optimal moves directly.
