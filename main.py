import pygame
import sys
from connect4.music_player import play_music, stop_music, next_track, previous_track  
from connect4.agents.smart_agent import smart_agent
from connect4.agents.random_agent import random_agent
from connect4.agents.minimax_agent import minimax_agent
from connect4.agents.ml_agent import ml_agent
from connect4.game_logic import game_loop
from connect4.graphics import draw_board
from connect4.game_utils import COLUMN_COUNT, ROW_COUNT, valid_move, drop_piece, check_win, block_player_move
from connect4.constants import screen, WIDTH, HEIGHT, YELLOW, RED, BLACK, WHITE
from connect4.message import display_message, ask_play_again
from connect4.player_data import save_player_score, display_scoreboard

pygame.init()

pygame.display.set_caption("Connect 4")

font = pygame.font.SysFont("Arial", 40)

board = [[0 for _ in range(7)] for _ in range(6)]  
turn = 1 

# Register Player Function
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
                    # Register player
                    return input_player_name()
                elif event.key == pygame.K_n:
                    # No registration, proceed to the game
                    return None

def input_player_name():
    name = ""
    input_active = True

    while input_active:
        screen.fill(BLACK)
        text = font.render("Enter your name:", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

        # Render the entered name
        input_text = font.render(name, True, WHITE)
        screen.blit(input_text, (WIDTH // 2 - input_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # When Enter is pressed, return the name
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character
                    name = name[:-1]
                else:
                    # Add character to name
                    name += event.unicode

# Main Menu Function
def main_menu():
    while True:
        screen.fill(BLACK)

        # Display options for 2-Player Game, AI vs AI, and Player vs AI
        text1 = font.render("Press 1 for 2-Player Game", True, WHITE)
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 3))

        text2 = font.render("Press 2 for AI vs AI", True, WHITE)
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))

        text3 = font.render("Press 3 for Player vs AI", True, WHITE)  # Added Player vs AI option
        screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 1.5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'human'  # 2-Player Game
                elif event.key == pygame.K_2:
                    return 'ai_vs_ai'  # AI vs AI
                elif event.key == pygame.K_3:
                    return 'player_vs_ai'  # Player vs AI

# Difficulty Menu Function
def difficulty_menu():
    while True:
        screen.fill(BLACK)

        # Display options for Easy, Medium, Hard difficulty, and ML agent
        text1 = font.render("Press 1 for Easy (Random Agent)", True, WHITE)
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 3))

        text2 = font.render("Press 2 for Medium (Smart Agent)", True, WHITE)
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))

        text3 = font.render("Press 3 for Hard (Minimax Agent)", True, WHITE)
        screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 1.5))

        text4 = font.render("Press 4 for ML Agent (Advanced AI)", True, WHITE)  # New ML agent option
        screen.blit(text4, (WIDTH // 2 - text4.get_width() // 2, HEIGHT // 1.2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return random_agent  # Easy, Random Agent
                elif event.key == pygame.K_2:
                    return smart_agent  # Medium, Smart Agent
                elif event.key == pygame.K_3:
                    return minimax_agent  # Hard, Minimax Agent
                elif event.key == pygame.K_4:
                    return ml_agent  # ML Agent (Advanced AI)

# Main Execution Block
if __name__ == "__main__":
    player_name = register_player()

    if player_name:
        print(f"Player registered with name: {player_name}")
    
    game_mode = main_menu()  # Get selected game mode

    # Set AI agents based on selected mode
    if game_mode == 'human':
        player1_agent = None
        player2_agent = None
    elif game_mode == 'ai_vs_ai':
        player1_agent = difficulty_menu()
        player2_agent = difficulty_menu()
    elif game_mode == 'player_vs_ai':
        player1_agent = None  # Human player
        player2_agent = difficulty_menu()  # AI opponent

    player1_name = "Player 1"
    player2_name = "Player 2" if game_mode == 'human' else "AI"
    # Launch the game loop
    game_loop(game_mode, player1_agent, player2_agent, display_message, ask_play_again, main_menu, difficulty_menu, screen, player1_name, player2_name)
    display_scoreboard()


## References
# [1] https://www.pygame.org/docs/
# https://scikit-learn.org/stable/
# https://www.youtube.com/watch?v=UYgyRArKDEs&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV
# https://www.askpython.com/python/examples/connect-four-game
# https://www.youtube.com/watch?v=yzj5TAfPI5Y
# https://labex.io/tutorials/python-connect-four-game-human-vs-ai-298858
# https://www.youtube.com/watch?v=cONc0NcKE7s
# https://www.youtube.com/watch?app=desktop&v=XpYz-q1lxu8&t=0s
# https://github.com/Buzzpy/Python-Projects/blob/main/Music_player.py
# https://github.com/hardbyte/python-can/blob/main/can/message.py
# https://github.com/cansozbir/Connect-4