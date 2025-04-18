import pygame

SQUARE_SIZE = 100  # Size of each square in the grid
ROW_COUNT = 6
COLUMN_COUNT = 7
WIDTH = SQUARE_SIZE * COLUMN_COUNT
HEIGHT = SQUARE_SIZE * (ROW_COUNT + 1)

# Colors
WHITE = (255, 255, 255)  
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (70, 130, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


