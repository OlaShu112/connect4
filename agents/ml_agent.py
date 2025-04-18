import random
import pandas as pd
import numpy as np

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

data.columns = features + ['winner']

data = data[data['winner'].apply(lambda x: isinstance(x, str))]

X = data.drop('winner', axis=1)
y = data['winner']

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

def convert_board_positions_to_numeric(df):
    for column in df.columns:
        if df[column].dtype == 'object':  
            df[column] = df[column].apply(
                lambda x: int(x.split('_')[1]) if isinstance(x, str) and '_' in x else x
            )
    return df

X = convert_board_positions_to_numeric(X)

for column in X.columns:
    if X[column].dtype == 'object':
        X[column] = pd.to_numeric(X[column], errors='coerce')

X = X.dropna()

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


def ml_agent(board, player):
    try:
        player_label_map = {1: 'O', 2: 'X'}  # Example mapping, adapt as needed
        player_label = player_label_map[player]
        
        if player_label not in label_encoder.classes_:
            label_encoder.fit(np.append(label_encoder.classes_, player_label))
        
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
