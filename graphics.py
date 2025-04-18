import pygame
from connect4.constants import BLACK, WHITE, WIDTH, HEIGHT, SQUARE_SIZE, ROW_COUNT, COLUMN_COUNT, RED, YELLOW, BLUE

def draw_board(board, turn, screen):
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARE_SIZE))

    # Draw all pieces on the board
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    # Hover effect for current turn piece
    hover_color = YELLOW if turn == 1 else RED
    hover_x = pygame.mouse.get_pos()[0] // SQUARE_SIZE * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.circle(screen, hover_color, (hover_x, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    pygame.display.flip()


