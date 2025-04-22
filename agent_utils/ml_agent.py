import os 
import random
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from connect4.game_utils import COLUMN_COUNT, valid_move, make_move

# === GLOBALS ===
label_encoder = LabelEncoder()

def outcome_score(outcome):
    if outcome == 'win':
        return 1.0
    elif outcome == 'draw':
        return 0.5
    elif outcome == 'loss':
        return 0.0
    return 0.25

def convert_board_positions_to_numeric(df):
    """Map board symbols to numbers."""
    mapping = {'x': 1, 'o': 2, 'b': 0}
    return df.applymap(lambda val: mapping.get(val, 0))

def train_model(dataset_file_name="connect-4.data", names_file_name="connect-4.names"):
    print(f"Training model using dataset: {dataset_file_name}")
    base_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(base_dir, "..", "connect4_dataset", dataset_file_name)

    print(f"Dataset path: {dataset_path}")  # For debugging

    try:
        # Read the dataset from CSV
        data = pd.read_csv(dataset_path, header=None, low_memory=False)
        print("Dataset loaded successfully!")
    except FileNotFoundError:
        print(f"File not found at {dataset_path}. Please check the file path.")
        raise
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        raise

    # Apply mapping: x = 1, o = 2, b = 0
    data.iloc[:, :-1] = convert_board_positions_to_numeric(data.iloc[:, :-1])

    # Encode the labels (win/draw/loss)
    y = label_encoder.fit_transform(data.iloc[:, -1])
    X = data.iloc[:, :-1]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"Model trained. Test Accuracy: {accuracy:.4f}")

    # Ensure models directory exists
    models_dir = os.path.join(base_dir, "..", "models")
    os.makedirs(models_dir, exist_ok=True)

    model_path = os.path.join(models_dir, "ml_agent_model.pkl")
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")

    return model

def predict_move(board, model):
    flat = np.array(board).flatten().reshape(1, -1)
    symbol_map = {'X': 1, 'O': 2, ' ': 0, 0: 0}
    flat = np.vectorize(lambda x: symbol_map.get(x, 0))(flat)
    prediction = model.predict(flat)
    predicted_class = label_encoder.inverse_transform(prediction)[0]
    return predicted_class

def ml_agent(board, player_symbol, model):
    best_score = -1
    best_move = None

    for col in range(COLUMN_COUNT):
        if valid_move(board, col):
            simulated_board = [row.copy() for row in board]
            make_move(simulated_board, col, player_symbol)
            try:
                prediction = predict_move(simulated_board, model)
                score = outcome_score(prediction)
                if score > best_score:
                    best_score = score
                    best_move = col
            except Exception as e:
                print(f"[ML Error] Prediction failed for column {col}: {e}")

    if best_move is not None:
        return best_move

    valid_columns = [col for col in range(COLUMN_COUNT) if valid_move(board, col)]
    return random.choice(valid_columns) if valid_columns else None

# === MAIN LOOP ===
if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    dataset_file = "connect-4.data"  # Updated to match the file name
    names_file = "connect-4.names"  # Updated to match the correct file name
    model_path = os.path.join(base_dir, "..", "models", "ml_agent_model.pkl")

    # Check if model exists, else train a new model
    if os.path.exists(model_path):
        print("Loading existing model...")
        model = joblib.load(model_path)
    else:
        print("Training new model...")
        model = train_model(dataset_file, names_file)

    # Test on empty board
    board = [[0 for _ in range(7)] for _ in range(6)]
    player_symbol = 'X'
    move = ml_agent(board, player_symbol, model)
    print(f"Predicted best move: {move}")
