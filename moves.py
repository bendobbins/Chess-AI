def valid_moves_pawn(start, board, piece, moveCounter):
    moveList = []
    if piece in range(25, 33):
        moveList = check_pawn_move(board, (start[0] + 1, start[1] + 1), moveList)
        if start[0] != 0:
            moveList = check_pawn_move(board, (start[0] - 1, start[1] + 1), moveList)
        if not board[start[0]][start[1] + 1]:
            if not moveCounter:
                if not board[start[0]][start[1] + 2]:
                    moveList.append((start[0], start[1] + 2))
            moveList.append((start[0], start[1] + 1))
        moveCounter += 1

    if piece in range(9, 17):
        moveList = check_pawn_move(board, (start[0] + 1, start[1] - 1), moveList)
        if start[0] != 0:
            moveList = check_pawn_move(board, (start[0] - 1, start[1] - 1), moveList)
        if not board[start[0]][start[1] - 1]:
            if not moveCounter:
                if not board[start[0]][start[1] - 2]:
                    moveList.append((start[0], start[1] - 2))
            moveList.append((start[0], start[1] - 1))
        moveCounter += 1

    return moveList


def check_pawn_move(board, space, moveList):
    try:
        if board[space[0]][space[1]]:
            moveList.append((space[0], space[1]))
    except:
        pass
    return moveList