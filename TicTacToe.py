"""
Tic Tac Toe Player
"""
import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]  # # return
# returns the initial state of the board: board


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # should take board as input, and return which player's turn it is
    # in the initial game state X gets the first move
    # the player should alternate
    # if a terminal board is provided then any return value is acceptable

    "Count no. of EMPTY, if odd then X's turn"
    if sum([i.count(EMPTY) for i in board]) % 2 == 1:
        return X
    else:
        return O
# returns the current player of the board: X, O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    acts = []
    for row in range(0, 3):
        for column in range(0, 3):
            # print(row, column)
            if board[row][column] == EMPTY:
                acts.append((row, column))
    return acts
# returns a list of all available moves: [moves]


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    try:
        if board_copy[action[0]][action[1]] == EMPTY:
            board_copy[action[0]][action[1]] = player(board_copy)
            return board_copy
        else:
            raise IndexError
    except IndexError:
        print("Invalid move")
# returns the result of an action when applied to the board: board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for combos in winning_combinations(len(board)):
        if all(board[r][c] == X for r, c in combos):
            return X
        if all(board[r][c] == O for r, c in combos):
            return O

    return None
# returns the winner if there is one: X, O, None


def winning_combinations(n):
    # rows
    for r in range(n):
        yield [(r, c) for c in range(n)]
    # columns
    for c in range(n):
        yield [(r, c) for r in range(n)]
    # First Diagonal \
    yield [(i, i) for i in range(n)]
    # Second Diagonal /
    yield[(i, n-1-i) for i in range(n)]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there are no EMPTY values left then the game is over
    # or if the game has been won
    if sum([row.count(EMPTY) for row in board]) == 0:
        return True
    if winner(board) is not None:
        return True
    return False

    # raise NotImplementedError
# is the game over?: True, False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1 + sum(row.count(EMPTY) for row in board)   # so that the AI values a quick win higher
    elif winner(board) == O:
        return -1 - sum(row.count(EMPTY) for row in board)
    else:
        return 0
# returns the value of a certain outcome: 1,0,-1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # X needs to maximise utility
    # O needs to minimise utility
    best_move = None
    current_player = player(board)
    if current_player == X:
        best_value = -math.inf
        for action in actions(board):
            board_copy = board[:]
            k = MIN_value(result(board_copy, action))
            if k > best_value:
                best_value = k
                best_move = action

    elif current_player == O:
        best_value = math.inf
        for action in actions(board):
            board_copy = board[:]
            k = MAX_value(result(board_copy, action))
            if k < best_value:
                best_value = k
                best_move = action
    return best_move


def MIN_value(state):
    if terminal(state):
        return utility(state)
    if sum(row.count(EMPTY) for row in state) == 8:     # if the computer has the first go, prevents checking every state
        return random.randint(0, 18)
    value = math.inf
    for action in actions(state):
        # copy = state[:]
        value = min(value, MAX_value(result(state, action)))
    return value


def MAX_value(state):
    if terminal(state):
        return utility(state)
    if sum(row.count(EMPTY) for row in state) == 8:  # if the computer has the first go, prevents checking every state
        return random.randint(0, 18)
    value = - math.inf
    for action in actions(state):
        # copy = state[:]
        value = max(value, MIN_value(result(state, action)))
    return value
