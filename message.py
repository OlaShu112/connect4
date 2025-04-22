import sys
import pygame

pygame.font.init()

# Font object to be used in all functions
font = pygame.font.SysFont("Arial", 40)

def display_message(message):
    screen = pygame.display.get_surface() 
    screen.fill((0, 0, 0))  
    
    text = font.render(message, True, (255, 255, 255))  
    
    # Position the text in the center of the screen
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 
                      screen.get_height() // 2 - text.get_height() // 2))
    
    pygame.display.flip()  
    pygame.time.wait(2000)  

def ask_play_again():
    while True:
        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))  
        
        # Render "Play Again?" text
        text = font.render("Play Again? (Y/N)", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
                           screen.get_height() // 2 - text.get_height() // 2))
        
        pygame.display.flip()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True  # Continue playing
                if event.key == pygame.K_n:
                    return False  # Go back to the main menu

def ai_move_wrapper(board, agent, turn, label, screen):
    # Import the necessary functions *inside* the function to prevent circular import
    from connect4.game_utils import (
        block_player_move, drop_piece, check_win,
        draw_board, board_is_full, switch_turn,
        easy_ai_move, medium_ai_move, hard_ai_move, ai_move
    )

    opponent = 1 if turn == 2 else 2
    block_col = block_player_move(board, opponent)

    if block_col != -1:
        col = block_col
    else:
        if agent.__name__ == "ml_agent":
            col = agent(board)
        else:
            col = agent(board, turn)

    row = drop_piece(board, col, turn)  # ← fixed bug: used block_col before, now using `col`

    if row != -1:
        if check_win(board, turn):
            draw_board(board, turn, screen)  
            display_message(f"{label} wins!")
            return True
        elif board_is_full(board):
            draw_board(board, turn, screen)
            display_message("It's a draw!")
            return True
        draw_board(board, switch_turn(turn), screen)

    return False
