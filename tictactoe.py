from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    X, O = 0, 0
    for row in board:
        for element in row:
            if element == 'X':
                X += 1
            elif element == 'O':
                O += 1
    if X <= O or (X == 0 and O == 0):
        return 'X'
    else:
        return 'O'



def actions(board):
    actions = []
    for i, row in enumerate(board):
        for j, element in enumerate(row):
            if not element:
                actions.append((i, j))
    return actions


def result(board, action):
    i, j = action[0], action[1]
    if board[i][j]:
        raise Exception("Action isn't valid")
    board = deepcopy(board)
    board[i][j] = player(board)
    return board

def check_sequence_winner(sequence):
    if sequence == ['X', 'X', 'X']:
        return 'X'
    elif sequence == ['O', 'O', 'O']:
        return 'O'
    return None

def winner(board):
    for i in range(3):
        row_winner = check_sequence_winner(board[i])
        if row_winner:
            return row_winner

        column_winner = check_sequence_winner([board[j][i] for j in range(3)])
        if column_winner:
            return column_winner

    diagonals = [
        [board[i][i] for i in range(3)],
        [board[i][2 - i] for i in range(3)]
    ]
    for diag in diagonals:
        diag_winner = check_sequence_winner(diag)
        if diag_winner:
            return diag_winner

    return None


print(winner(initial_state()))

def terminal(board):
    if winner(board):
        return True
    for row in board:
        for element in row:
            if not element:
                return False
    return True


def utility(board):

    game_winner = winner(board)
    if game_winner == 'X':
        return 1
    elif game_winner == 'O':
        return -1
    else:
        return 0

def minimax(board):

    if terminal(board):
        return
    if board == initial_state():
        return (0, 0)

    actual_player = player(board)
    if actual_player == 'O':
        return minimize(board)[1]
    return maximize(board)[1]

def minimize(board):
    if terminal(board):
        return (utility(board), 0)

    min_value, min_action = float('inf'), 0

    for action in actions(board):
        action_result = maximize(result(board, action))
        if action_result[0] < min_value:
            min_value = action_result[0]
            min_action = action
    return (min_value, min_action)

def maximize(board):
    if terminal(board):
        return (utility(board), 0)

    max_value, max_action = float('-inf'), 0    
    for action in actions(board):
        action_result = minimize(result(board, action))
        
        if action_result[0] > max_value:
            max_value = action_result[0]
            max_action = action
    return (max_value, max_action)