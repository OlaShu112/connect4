# utils.py

COLUMN_COUNT = 7
ROW_COUNT = 6

def create_board():
    """Creates a new empty board."""
    return [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

def drop_piece(board, col, player):
    """Drops a piece into the specified column for the current player."""
    col = int(float(col))  # Handles both '5' and '5.0'
    if col < 0 or col >= COLUMN_COUNT:
        return -1  # Invalid column index

    for row in range(ROW_COUNT - 1, -1, -1):  # Start from the bottom of the board
        if board[row][col] == 0:  # If the space is empty
            board[row][col] = player  # Drop the piece
            return row  # Return the row where the piece was placed
    return -1  # If the column is full

def valid_move(board, col):
    """Checks if the move is valid in the given column."""
    col = int(float(col))
    return 0 <= col < COLUMN_COUNT and board[0][col] == 0

def check_win(board, piece):
    """Checks for a win condition for the specified player (piece)."""
    # Horizontal check
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Positive diagonal check
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Negative diagonal check
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

# utils.py

def block_player_move(board, player):
    """
    Check if the opponent can win in the next move and return the column to block it.
    If no blocking move is found, return -1.
    """
    for col in range(len(board[0])):  # Iterate through all columns
        if valid_move(board, col):  # Check if the column is a valid move
            # Simulate the move for the opponent (make a copy of the board)
            temp_board = [row.copy() for row in board]
            row = drop_piece(temp_board, col, player)  # Drop the player's piece in the simulated board
            if check_win(temp_board, player):  # Check if the opponent wins
                return col  # Block the winning move by returning the column
    return -1  # No blocking move found


