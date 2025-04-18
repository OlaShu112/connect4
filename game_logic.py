import pygame
import time
import sys
from connect4.game_utils import drop_piece, valid_move, check_win, block_player_move, ai_move, switch_turn
from connect4.music_player import play_music, stop_music, next_track, previous_track
from connect4.message import display_message, ask_play_again, main_menu, difficulty_menu
from connect4.agents.random_agent import random_agent
from connect4.agents.minimax_agent import minimax_agent
from connect4.agents.ml_agent import ml_agent
from connect4.constants import BLACK, WHITE, WIDTH, HEIGHT, SQUARE_SIZE, ROW_COUNT, COLUMN_COUNT, RED, YELLOW, BLUE
from connect4.game_utils import create_board, board_is_full, get_column_from_mouse
from connect4.graphics import draw_board
from connect4.player_data import save_player_score
from connect4.player_data import register_player

TURN_TIME_LIMIT = 10  # seconds

def game_loop(game_mode, player1_agent, player2_agent, display_message, ask_play_again, main_menu, difficulty_menu, screen, player1_name, player2_name):
    while True:
        board = create_board()
        running = True
        turn = 1
        draw_board(board, turn, screen)

        turn_start_time = time.time()  # Start of each turn

        while running:
            time_left = TURN_TIME_LIMIT - int(time.time() - turn_start_time)
            pygame.display.set_caption(f"Connect 4 - Time left: {time_left}s")

            if time_left <= 0:
                print("Turn timed out!")
                turn = switch_turn(turn)
                turn_start_time = time.time()
                draw_board(board, turn, screen)

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
                                draw_board(board, turn, screen)
                                winner = player1_name if turn == 1 else player2_name
                                display_message(f"{winner} wins!")
                                save_player_score(winner, 1)
                                running = False
                            elif board_is_full(board):
                                draw_board(board, turn, screen)
                                display_message("It's a draw!")
                                save_player_score(player1_name, 0.5)
                                save_player_score(player2_name, 0.5)
                                running = False
                            else:
                                turn = switch_turn(turn)
                                turn_start_time = time.time()
                                draw_board(board, turn, screen)

                elif game_mode == 'player_vs_ai' and turn == 1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        col = get_column_from_mouse(event)
                        if valid_move(board, col):
                            row = drop_piece(board, col, turn)
                            if row != -1:
                                if check_win(board, turn):
                                    draw_board(board, turn, screen)
                                    display_message(f"{player1_name} wins!")
                                    save_player_score(player1_name, 1)
                                    running = False
                                elif board_is_full(board):
                                    draw_board(board, turn, screen)
                                    display_message("It's a tie!")
                                    save_player_score(player1_name, 0.5)
                                    save_player_score(player2_name, 0.5)
                                    running = False
                                else:
                                    turn = 2
                                    turn_start_time = time.time()
                                    draw_board(board, turn, screen)
                                    pygame.time.delay(1000)

                elif game_mode == 'player_vs_ai' and turn == 2:
                    pygame.time.delay(1000)
                    if ai_move(board, player2_agent, turn, player2_name, screen):
                        save_player_score(player2_name, 1)
                        running = False
                    else:
                        turn = 1
                        turn_start_time = time.time()

            if game_mode == 'ai_vs_ai' and running:
                pygame.time.delay(2000)
                agent = player1_agent if turn == 1 else player2_agent
                label = player1_name if turn == 1 else player2_name
                if ai_move(board, agent, turn, label, screen):
                    save_player_score(label, 1)
                    running = False
                else:
                    turn = switch_turn(turn)
                    turn_start_time = time.time()

            if not running:
                if ask_play_again():
                    break
                else:
                    game_mode = main_menu()

                    if game_mode == 'ai_vs_ai':
                        from connect4.agents.ml_agent import ml_agent
                        player1_agent = minimax_agent
                        player2_agent = ml_agent

                    player1_agent = difficulty_menu()
                    break

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")

    game_mode = main_menu()
    player1_agent = difficulty_menu()
    player2_agent = random_agent if game_mode == 'ai_vs_ai' else minimax_agent

    if game_mode == 'ai_vs_ai':
        player1_name = "AI 1"
        player2_name = "AI 2"
    elif game_mode == 'player_vs_ai':
        player1_name = register_player(1)
        player2_name = "AI"
    else:
        player1_name = register_player(1)
        player2_name = register_player(2)

    game_loop(game_mode, player1_agent, player2_agent, display_message, ask_play_again, main_menu, difficulty_menu, screen, player1_name, player2_name)
