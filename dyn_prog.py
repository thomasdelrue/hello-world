import numpy

N = 8
board_state_memory = {}
board = np.zeros((N, N), np.int8)


def create_board_strin(board):
    board_string = ''
    for i in range(N):
        for j in range(N):
            board_string += str(board[i][j])
    return board_string


board_copy = board.copy()
board_copy[0, 1] = 1


def is_board_safe(board):
    board_key = create_board_string(board)

    if board_key in board_state_memory:
        print('Using cached information')
        return board_state_memory[board_key]

    row_sum = np.sum(board, axis=1)
    if len(row_sum[np.where(row_sum > 1)]) > 0:
        board_state_memory[board_key] = False
        return False

    col_sum = np.sum(board, axis=0)
    if len(col_sum[np.where(col_sum > 1)]) > 0:
        board_state_memory[board_key] = False
        return False

    diags = [board[::-1, :].diagonal(i) for i in range(-board.shape[0] + 1, board.shape[1])]
    diags.extend(board.diagonal(i) for i in range(board.shape[1] - 1, -board.shape[0], -1))
    for diag in diags:
        if np.sum(diag) > 1:
            board_state_memory[board_key] = False
            return False

    board_state_memory[board_key] = True
    return True
