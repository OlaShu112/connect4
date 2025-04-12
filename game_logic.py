import pygame
import sys
from connect4.utils import create_board, drop_piece, valid_move, check_win, block_player_move
from connect4.music_player import play_music, stop_music, next_track, previous_track
from connect4.message import display_message, ask_play_again, main_menu, difficulty_menu
from connect4.agents import minimax_agent, random_agent

# Initialize pygame
pygame.init()

# Define constants
SQUARE_SIZE = 100  # Size of each square in the grid
ROW_COUNT = 6  # Number of rows
COLUMN_COUNT = 7  # Number of columns
WIDTH = SQUARE_SIZE * COLUMN_COUNT
HEIGHT = SQUARE_SIZE * (ROW_COUNT + 1)

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

def switch_turn(turn):
    return 2 if turn == 1 else 1

def get_column_from_mouse(event):
    return event.pos[0] // SQUARE_SIZE

def board_is_full(board):
    return all(board[0][c] != 0 for c in range(len(board[0])))

def ai_move(board, agent, turn, label):
    opponent = 1 if turn == 2 else 2
    block_col = block_player_move(board, opponent)

    if block_col != -1:
        row = drop_piece(board, block_col, turn)
        if row != -1:
            if check_win(board, turn):
                draw_board(board, turn)
                display_message(f"{label} wins!")
                return True
            elif board_is_full(board):
                draw_board(board, turn)
                display_message("It's a tie!")
                return True
            draw_board(board, switch_turn(turn))
        return False

    col = agent(board, turn)
    try:
        col = int(float(col))
    except (ValueError, TypeError):
        print(f"Invalid column received from {label}: {col}")
        col = -1

    if col == -1:
        print(f"{label} couldn't find a valid move. Skipping turn.")
        return False

    row = drop_piece(board, col, turn)
    if row != -1:
        if check_win(board, turn):
            draw_board(board, turn)
            display_message(f"{label} wins!")
            return True
        elif board_is_full(board):
            draw_board(board, turn)
            display_message("It's a tie!")
            return True
        draw_board(board, switch_turn(turn))
    return False

def draw_board(board, current_turn):
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))

    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    hover_color = YELLOW if current_turn == 1 else RED
    pygame.draw.circle(screen, hover_color, (pygame.mouse.get_pos()[0] // SQUARE_SIZE * SQUARE_SIZE + SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
    pygame.display.flip()

def game_logic(game_mode):
    if game_mode == 'human':
        running = True
        turn = 1
        board = create_board()

        while running:
            screen.fill(BLACK)
            draw_board(board, turn)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if game_mode == 'human' and event.type == pygame.MOUSEBUTTONDOWN:
                    col = get_column_from_mouse(event)
                    if valid_move(board, col):
                        row = drop_piece(board, col, turn)
                        if row != -1:
                            if check_win(board, turn):
                                draw_board(board, turn)
                                display_message(f"Player {turn} wins!")
                                running = False
                            elif board_is_full(board):
                                draw_board(board, turn)
                                display_message("It's a tie!")
                                running = False
                            else:
                                turn = switch_turn(turn)
                                draw_board(board, turn)

def game_loop(game_mode, player1_agent, player2_agent, display_message, ask_play_again, main_menu, difficulty_menu):
    while True:
        board = create_board()
        running = True
        turn = 1
        draw_board(board, turn)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        play_music()
                    elif event.key == pygame.K_s:
                        stop_music()
                    elif event.key == pygame.K_RIGHT:
                        next_track()
                    elif event.key == pygame.K_LEFT:
                        previous_track()

                if game_mode == 'human' and event.type == pygame.MOUSEBUTTONDOWN:
                    col = get_column_from_mouse(event)
                    if valid_move(board, col):
                        row = drop_piece(board, col, turn)
                        if row != -1:
                            if check_win(board, turn):
                                draw_board(board, turn)
                                display_message(f"Player {turn} wins!")
                                running = False
                            elif board_is_full(board):
                                draw_board(board, turn)
                                display_message("It's a tie!")
                                running = False
                            turn = switch_turn(turn)
                            draw_board(board, turn)

                elif game_mode == 'player_vs_ai' and turn == 1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        col = get_column_from_mouse(event)
                        if valid_move(board, col):
                            row = drop_piece(board, col, turn)
                            if row != -1:
                                if check_win(board, turn):
                                    draw_board(board, turn)
                                    display_message(f"Player {turn} wins!")
                                    running = False
                                elif board_is_full(board):
                                    draw_board(board, turn)
                                    display_message("It's a tie!")
                                    running = False
                                turn = 2
                                draw_board(board, turn)
                                pygame.time.delay(1000)

                elif game_mode == 'player_vs_ai' and turn == 2:
                    pygame.time.delay(1000)
                    if ai_move(board, player2_agent, turn, "AI Player"):
                        running = False
                    else:
                        turn = 1

            # AI vs AI Logic
            if game_mode == 'ai_vs_ai' and running:
                pygame.time.delay(500)
                agent = player1_agent if turn == 1 else player2_agent
                label = "AI 1" if turn == 1 else "AI 2"
                if ai_move(board, agent, turn, label):
                    running = False
                else:
                    turn = switch_turn(turn)

            if not running:
                if ask_play_again():
                    break
                else:
                    game_mode = main_menu()
                    player1_agent = difficulty_menu()
                    player2_agent = random_agent if game_mode == 'ai_vs_ai' else minimax_agent
                    break

# Run the game loop
if __name__ == "__main__":
    game_mode = main_menu()
    player1_agent = difficulty_menu()
    player2_agent = random_agent if game_mode == 'ai_vs_ai' else minimax_agent
    game_loop(game_mode, player1_agent, player2_agent, display_message, ask_play_again, main_menu, difficulty_menu)
