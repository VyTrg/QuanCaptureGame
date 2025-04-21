import math
import random


def alpha_beta(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or check_win(board) != None:
        return evaluate(board)

    if is_maximizing:
        value = -float('inf')
        for i in range(10):
            if board[i] == ' ':
                board[i] = 'D'
                value = max(value, alpha_beta(board, depth-1, alpha, beta, False))
                board[i] = ' '
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return value
    else:
        value = float('inf')
        for i in range(10):
            if board[i] == ' ':
                board[i] = 'Q'
                value = min(value, alpha_beta(board, depth-1, alpha, beta, True))
                board[i] = ' '
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return value

def check_win(board):
    for i in range(10):
        if board[i] == 'D' and board[i+1] == 'D' and board[i+2] == 'D':
            return 'D'
    if board[10] == 'Q' and board[11] == 'Q':
        return 'Q'
    return None


def evaluate(board):
    if check_win(board) == 'D':
        return 10
    elif check_win(board) == 'Q':
        return -10
    else:
        return 0