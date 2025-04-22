import pygame
import time
import sys
from connect4.game_utils import (
    drop_piece, valid_move, check_win, ai_move,
    switch_turn, create_board, board_is_full, get_column_from_mouse
)
from connect4.music_player import play_music, stop_music, next_track, previous_track
from connect4.agent_utils.random_agent import random_agent
from connect4.agent_utils.minimax_agent import minimax_agent
from connect4.agent_utils.ml_agent import train_model
from connect4.constants import BLACK, WHITE, WIDTH, HEIGHT, SQUARE_SIZE, ROW_COUNT, COLUMN_COUNT, RED, YELLOW, BLUE
from connect4.graphics import draw_board
from connect4.player_data import save_player_score
from connect4.game_help import block_player_move  # Correct import here

TURN_TIME_LIMIT = 10  # seconds

def game_loop(game_mode, player1_agent, player2_agent, display_message, ask_play_again,
              main_menu, difficulty_menu, screen, player1_name, player2_name, model=None):
    """
    Main game loop for Connect 4.
    Handles different game modes, time limit per turn, player moves, AI moves, and music control.
    """
    while True:
        board = create_board()
        running = True
        turn = 1  # Player 1 starts
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
                    elif event.key == pygame.K_4:
                        print("Training ML agent manually...")
                        try:
                            model = train_model("connect4_dataset/connect-4.data", "connect4_dataset/connect-4.names")
                            print("Manual training complete.")
                        except Exception as e:
                            print(f"Error training ML agent: {e}")

                # Handle mouse click for human player
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

                # Handle moves in Player vs AI mode
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
                                    display_message("It's a draw!")
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
                    if ai_move is not None:
                        if ai_move(board, player2_agent, turn, player2_name, screen):
                            save_player_score(player2_name, 1)
                            running = False
                        else:
                            turn = 1
                            turn_start_time = time.time()
                    else:
                        print("AI move function is not available.")

            # Handle AI vs AI mode
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
                    elif game_mode == 'player_vs_ai':
                        player1_agent = difficulty_menu()
                        player2_agent = minimax_agent
                    else:
                        player1_agent = difficulty_menu()
                        player2_agent = difficulty_menu()
                    break
