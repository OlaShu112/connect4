# test_import.py
import sys

try:
    import connect4
    print("Importing connect4 module was successful.")
    
    from connect4.agents.ml_agent import train_ml_agent
    print("train_ml_agent import successful")

    # Test if train_ml_agent function runs
    dataset_path = "connect4_dataset/connect-4.data"
    names_path = "connect4_dataset/connect-4.names"
    print("Attempting to run train_ml_agent...")

    model = train_ml_agent(dataset_path, names_path)  # Call the function to ensure it's working
    print("train_ml_agent executed successfully.")
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
