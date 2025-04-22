import pygame
import sys
import os
import connect4

# Music and agents
from connect4.music_player import play_music, stop_music, next_track, previous_track
from connect4.agent_utils.smart_agent import smart_agent
from connect4.agent_utils.random_agent import random_agent
from connect4.agent_utils.minimax_agent import minimax_agent

# Import the ML agent properly
try:
    from connect4.agent_utils.ml_agent import train_model, ml_agent
except ImportError as e:
    print(f"Error importing ML Agent: {e}")
    train_model = None
    ml_agent = None

# Game logic and utilities
from connect4.game_logic import game_loop
from connect4.graphics import draw_board
from connect4.game_utils import COLUMN_COUNT, ROW_COUNT, valid_move, check_win
from connect4.constants import screen, WIDTH, HEIGHT, YELLOW, RED, BLACK, WHITE
from connect4.message import display_message, ask_play_again
from connect4.game_help import block_player_move, drop_piece
from connect4.player_data import save_player_score, display_scoreboard

pygame.init()
pygame.display.set_caption("Connect 4")
font = pygame.font.SysFont("Arial", 40)

# Initialize game board and turn
board = [[0 for _ in range(7)] for _ in range(6)]
turn = 1  # 1 = Player 1, 2 = Player 2

# Paths for the dataset and names
dataset_path = os.path.join(os.path.dirname(__file__), "connect4_dataset", "connect-4.data")
names_path = os.path.join(os.path.dirname(__file__), "connect4_dataset", "connect-4.names")


# Function to register player
def register_player():
    while True:
        screen.fill(BLACK)
        text = font.render("Do you want to register your name? (Y/N)", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return input_player_name()
                elif event.key == pygame.K_n:
                    return None


# Function to input player name
def input_player_name():
    name = ""
    input_active = True

    while input_active:
        screen.fill(BLACK)
        prompt = font.render("Enter your name:", True, WHITE)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 3))

        typed = font.render(name, True, WHITE)
        screen.blit(typed, (WIDTH // 2 - typed.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode


# Main menu function
def main_menu():
    while True:
        screen.fill(BLACK)

        options = [
            "Press 1 for 2-Player Game",
            "Press 2 for AI vs AI",
            "Press 3 for Player vs AI"
        ]

        for i, option in enumerate(options):
            text = font.render(option, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'human'
                elif event.key == pygame.K_2:
                    return 'ai_vs_ai'
                elif event.key == pygame.K_3:
                    return 'player_vs_ai'


# Difficulty menu function
def difficulty_menu():
    while True:
        screen.fill(BLACK)

        difficulties = [
            "Press 1 for Easy (Random Agent)",
            "Press 2 for Medium (Smart Agent)",
            "Press 3 for Hard (Minimax Agent)",
            "Press 4 for ML Agent (Advanced AI)"
        ]

        for i, option in enumerate(difficulties):
            text = font.render(option, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return random_agent
                elif event.key == pygame.K_2:
                    return smart_agent
                elif event.key == pygame.K_3:
                    return minimax_agent
                elif event.key == pygame.K_4:
                    if model:
                        return lambda board, turn: ml_agent(board, turn, model)
                    else:
                        print("ML model unavailable. Falling back to Minimax agent.")
                        return minimax_agent


# Main program execution
if __name__ == "__main__":
    player_name = register_player()
    if player_name:
        print(f"Player registered with name: {player_name}")

    # ML model training
    model = None
    if train_model:
        try:
            model = train_model(dataset_path, names_path)
            print("ML model trained successfully.")
        except Exception as e:
            print(f"Error training ML model: {e}")
    else:
        print("ML training function not available.")

    game_mode = main_menu()

    player1_agent = None
    player2_agent = None

    # Setup players based on game mode
    if game_mode == 'human':
        player1_name = "Player 1"
        player2_name = "Player 2"

    elif game_mode == 'ai_vs_ai':
        player1_name = "AI 1"
        player2_name = "AI 2"
        player1_agent = minimax_agent
        if model:
            player2_agent = lambda board, turn: ml_agent(board, turn, model)
            print("AI 2 using ML agent.")
        else:
            print("ML agent not available. Falling back to minimax.")
            player2_agent = minimax_agent

    elif game_mode == 'player_vs_ai':
        player1_name = "Player 1"
        player2_name = "AI"
        player1_agent = None

        selected_agent = difficulty_menu()

        if selected_agent == ml_agent:
            if model:
                player2_agent = lambda board, turn: ml_agent(board, turn, model)
                print("Player selected ML agent.")
            else:
                print("ML model unavailable. Falling back to Minimax agent.")
                player2_agent = minimax_agent
        else:
            player2_agent = selected_agent

        if player2_agent is None:
            print("AI agent setup failed. Returning to main menu.")
            sys.exit()

    # Start the game loop
    try:
        game_loop(
            game_mode,
            player1_agent,
            player2_agent,
            display_message,
            ask_play_again,
            main_menu,
            difficulty_menu,
            screen,
            player1_name,
            player2_name
        )
    except Exception as e:
        print(f"Game error: {e}")
        pygame.quit()
        sys.exit()


## References
# [1] https://www.pygame.org/docs/
# https://scikit-learn.org/stable/
# https://www.youtube.com/watch?v=UYgyRArKDEs&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV
# https://www.askpython.com/python/examples/connect-four-game
# https://www.youtube.com/watch?v=yzj5TAfPI5Y
# https://labex.io/tutorials/python-connect-four-game-human-vs-ai-298858
# https://www.youtube.com/watch?v=cONc0NcKE7s
# https://github.com/Buzzpy/Python-Projects/blob/main/Music_player.py
# https://github.com/hardbyte/python-can/blob/main/can/message.py
# https://github.com/cansozbir/Connect-4
# This is a Connect Four game implementation with options for human, AI vs AI, and player vs AI modes.