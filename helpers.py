def create_board():
    """Create initial board with numbers and return as string.
    
    >>> create_board()
    '[[1, 2, 3], [4, 5, 6], [7, 8, 9]]'
    """

    return "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]"

def show_board(board):
    """Change form of board for display in Slack.

    >>> show_board("[['X', 2, 3], [4, 5, 6], [7, 8, 'O']]")
    ' |  X  |  2  |  3  |
    | ---+---+--- |
    |  4  |  5  |  6  |
    | ---+---+--- |
    |  7  |  8  |  O  |'
    """

    board = eval(board)

    return ''' |  %s  |  %s  |  %s  |
| ---+---+--- |
|  %s  |  %s  |  %s  |
| ---+---+--- |
|  %s  |  %s  |  %s  |''' % (board[0][0], board[0][1], board[0][2],
						board[1][0], board[1][1], board[1][2],
						board[2][0], board[2][1], board[2][2])


def make_move(board, position, player):
    """Update board based on user input and return new board. 
    If invalid move, send error.

    >>> board = "[[1, 2, 'O'], [4, 'O', 6], ['X', 'O', 'X']]" 

    >>> updated_board = make_move(board, 2, 'X')

    >>> updated_board
    "[[1, 'X', 'O'], [4, 'O', 6], ['X', 'O', 'X']]"

    >>> make_move(updated_board, 5, 'O')
    
    >>> make_move(updated_board, 4, 'O')
    "[[1, 'X', 'O'], ['O', 'O', 6], ['X', 'O', 'X']]"
    """

    board = eval(board)

    col, row = divmod(position - 1, 3)
    if board[col][row] not in ['X', 'O']:
        board[col][row] = player
        return str(board)
    else:
        return None


def is_board_full(board):
    """Check if board is full by traversing board and checking for numbers.

    >>> is_board_full("[[1, 2, 3], [4, 'X', 6], [7, 8, 9]]")
    False

    >>> is_board_full("[['X', 'O', 'X'], ['X', 'O', 'X'], ['O', 8, 'O']]")
    False

    >>> is_board_full("[['X', 'O', 'X'], ['X', 'O', 'O'], ['O', 'X', 'O']]")
    True
    """

    board = eval(board)

    for row in board:
        for col in range(3):
            if row[col] in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                return False

    return True


def find_winner(board):
    """Traverse board to find winner across, down, or diagonally.

    >>> print find_winner("[[1, 2, 3], ['X', 5, 'O'], [7, 8, 9]]")
    None

    >>> find_winner("[['X', 2, 3], ['X', 5, 'O'], ['X', 8, 9]]")
    'X'

    >>> find_winner("[['X', 'O', 'X'], ['O', 'O', 'X'], ['O', 'X', 'X']]")
    'X'

    >>> find_winner("[['X', 2, 'O'], ['X', 'O', 'O'], ['O', 8, 9]]")
    'O'
    """

    board = eval(board)
    #Across check
    for row in range(3):
        if board[row][0] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and board[row][0] == board[row][1] == board[row][2]:
            return board[row][0]
    #Down check
    for col in range(3):
        if board[0][col] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
    #Diagonal from upper left check
    if board[0][0] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    #Diagonal from lower left check
    if board[2][0] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and board[2][0] == board[1][1] == board[0][2]:
        return board[2][0]


if __name__ == "__main__":
    import doctest

    if doctest.testmod().failed == 0:
        print "\n*** ALL TESTS PASS.\n"