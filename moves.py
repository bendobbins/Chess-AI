def valid_moves_pawn(start, board, piece, moveCounter):
    moveList = []
    if piece in range(25, 33):
        moveList = check_pawn_move(board, (start[0] + 1, start[1] + 1), moveList, False)
        if start[0] != 0:
            moveList = check_pawn_move(board, (start[0] - 1, start[1] + 1), moveList, False)
        if not board[start[0]][start[1] + 1]:
            if not moveCounter:
                if not board[start[0]][start[1] + 2]:
                    moveList.append((start[0], start[1] + 2))
            moveList.append((start[0], start[1] + 1))

    else:
        moveList = check_pawn_move(board, (start[0] + 1, start[1] - 1), moveList, True)
        if start[0] != 0:
            moveList = check_pawn_move(board, (start[0] - 1, start[1] - 1), moveList, True)
        if not board[start[0]][start[1] - 1]:
            if not moveCounter:
                if not board[start[0]][start[1] - 2]:
                    moveList.append((start[0], start[1] - 2))
            moveList.append((start[0], start[1] - 1))

    return moveList

def check_pawn_move(board, space, moveList, white):
    try:
        if white:
            if board[space[0]][space[1]] in range(18, 33):
                moveList.append((space[0], space[1]))
        else:
            if board[space[0]][space[1]] in range(2, 17):
                moveList.append((space[0], space[1]))
    except IndexError:
        pass
    return moveList


def valid_moves_knight(start, board, piece):
    moveList = []
    possibleMoves = [
        (start[0] - 1, start[1] + 2),
        (start[0] + 1, start[1] + 2),
        (start[0] + 1, start[1] - 2),
        (start[0] - 1, start[1] - 2),
        (start[0] + 2, start[1] + 1),
        (start[0] - 2, start[1] + 1),
        (start[0] - 2, start[1] - 1),
        (start[0] + 2, start[1] - 1)
    ]
    if piece in range(21, 23):
        for move in possibleMoves:
            moveList = check_knight_move(board, move, moveList, False)
    else:
        for move in possibleMoves:
            moveList = check_knight_move(board, move, moveList, True)
    return moveList

def check_knight_move(board, space, moveList, white):
    try:
        if space[0] < 0 or space[1] < 0:
            return moveList
        if white:
            if board[space[0]][space[1]] in range(18, 33) or board[space[0]][space[1]] == 0:
                moveList.append((space[0], space[1]))
        else:
            if board[space[0]][space[1]] in range(2, 17) or board[space[0]][space[1]] == 0:
                moveList.append((space[0], space[1]))
    except IndexError:
        pass
    return moveList