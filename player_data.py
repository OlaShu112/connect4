import json
import os

DATA_FILE = "player_data.json"

# Ensure the JSON file exists
def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)

# Register or update a player's win count
def save_player_score(player_name, score):
    init_data_file()
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if player_name in data:
        data[player_name]["wins"] += score
    else:
        data[player_name] = {"wins": score}

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Get all player scores
def get_scoreboard():
    init_data_file()
    with open(DATA_FILE, "r") as f:
        return json.load(f)


# connect4/player_data.py

def register_player(player_num):
    # Your logic for registering a player
    name = input(f"Enter name for Player {player_num}: ")
    print(f"Player registered with name: {name}")
    return name


# Display the scoreboard sorted by score
def display_scoreboard():
    scoreboard = get_scoreboard()
    sorted_scores = sorted(scoreboard.items(), key=lambda x: x[1]["wins"], reverse=True)

    print("\n===== SCOREBOARD =====")
    for i, (name, stats) in enumerate(sorted_scores, 1):
        print(f"{i}. {name} - {stats['wins']} wins")
    print("======================\n")
