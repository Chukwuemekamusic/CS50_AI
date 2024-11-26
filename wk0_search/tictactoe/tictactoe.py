
"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board) == True:
        return X
    if board == initial_state():
        return X
    count_diff = sum(row.count(X) - row.count(O) for row in board)
    return O if count_diff > 0 else X
    
    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    # if terminal(board) == True:
    #     return possible_moves
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                possible_moves.add((i, j))
    return possible_moves

    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError('invalid action')
    
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # horizontal check
        if board[i][0] == board[i][1] == board[i][2] is not None:
            return board[i][0]
        # vertical check
        if board[0][i] == board[1][i] == board[2][i] is not None:
            return board[0][i]
    
    # diagonal check
    if board[0][0] == board[1][1] == board[2][2] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] is not None:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check for winner or possible move to be made
    if winner(board) is not None or not any(None in row for row in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # You may assume utility will only be called on a board if terminal(board) is True.
    win = winner(board)
    if win == X:
        return 1 
    elif win == O:
        return -1
    else: 
        return 0
    


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        _, best_move = max_value(board, float('-inf'), float('inf'))
    else:
        _, best_move = min_value(board, float('-inf'), float('inf'))
    
    return best_move
        
        
def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    
    v = float('-inf')
    best_move = None
    for action in actions(board):
        max_val, _ = min_value(result(board, action), alpha, beta)
        if max_val > v:
            v = max_val
            best_move = action
        alpha = max(alpha, v)
        if beta <= alpha:
            break            
    return v, best_move

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    
    v = float('inf')
    best_move = None
    for action in actions(board):
        # v = min(v, max_value(result(board,action)))
        min_val, _ = max_value(result(board, action), alpha, beta)
        if min_val < v:
            v = min_val
            best_move = action
        beta = min(v, beta)
        if beta <= alpha:
            break
    return v, best_move
