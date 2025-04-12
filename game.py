import pygame
import sys
from connect4.music_player import play_music, stop_music, next_track, previous_track  
from connect4.agents import minimax_agent, random_agent, smart_agent, ml_agent
from connect4.game_logic import game_loop, draw_board
from connect4.utils import create_board, drop_piece, valid_move, check_win, block_player_move
from connect4.message import display_message, ask_play_again  # Import from message.py

# Initialize Pygame
pygame.init()

# Constants for game
SQUARE_SIZE = 100  
COLUMN_COUNT = 7  
ROW_COUNT = 6  
WIDTH = COLUMN_COUNT * SQUARE_SIZE  
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE  

# Colours
WHITE = (255, 255, 255)
BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up display
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")

# Font for text
font = pygame.font.SysFont("Arial", 40)

def main_menu():
    """Displays the main menu for game mode selection."""
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

def difficulty_menu():
    """Displays the difficulty menu for AI selection."""
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

if __name__ == "__main__":
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

    # Launch the game
    game_loop(game_mode, player1_agent, player2_agent, display_message, ask_play_again, main_menu, difficulty_menu)
