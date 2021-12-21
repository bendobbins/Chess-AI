import operator

def valid_moves_pawn(start, board, piece, moveCounter):
    moveList = []
    if piece in range(17, 33):
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
            if board[space[0]][space[1]] in range(17, 33):
                moveList.append((space[0], space[1]))
        else:
            if board[space[0]][space[1]] in range(1, 17):
                moveList.append((space[0], space[1]))
    except IndexError:
        pass
    return moveList



def valid_moves_knight(start, board, piece, checkProtected):
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
    for move in possibleMoves:
        if piece in range(17, 33):
            moveList = check_knight_move(board, move, moveList, False, checkProtected)
        else:
            moveList = check_knight_move(board, move, moveList, True, checkProtected)
    return moveList

def check_knight_move(board, space, moveList, white, checkProtected):
    if space[0] < 0 or space[1] < 0 or space[0] > 7 or space[1] > 7:
        return moveList
    if not checkProtected:
        if white:
            if board[space[0]][space[1]] == 0 or board[space[0]][space[1]] in range(17, 33):
                moveList.append((space[0], space[1]))
        else:
            if board[space[0]][space[1]] in range(0, 17):
                moveList.append((space[0], space[1]))
    else:
        moveList.append(space)
    return moveList



def valid_moves_bishop(start, board, piece, checkProtected):
    moveList = []
    directions = [
        (operator.sub, operator.add),
        (operator.sub, operator.sub),
        (operator.add, operator.add),
        (operator.add, operator.sub)
    ]
    for direction in directions:
        for i in range(1, 9):
            space = (direction[0](start[0], i), direction[1](start[1], i))
            if space[0] < 0 or space[1] < 0 or space[0] > 7 or space[1] > 7:
                break
            if not checkProtected:
                if piece in range(17, 33):
                    if board[space[0]][space[1]] in range(17, 33):
                        break
                    elif board[space[0]][space[1]] in range(1, 17):
                        moveList.append(space)     
                        break
                else:
                    if board[space[0]][space[1]] in range(1, 17):
                        break
                    elif board[space[0]][space[1]] in range(17, 33):
                        moveList.append(space)     
                        break
            else:
                if board[space[0]][space[1]] in range(1, 33):
                    moveList.append(space)     
                    break
            if board[space[0]][space[1]] == 0:
                moveList.append(space)
    
    return moveList



def valid_moves_rook(start, board, piece, checkProtected):
    moveList = []
    moveList = check_rook_direction(start[0], start[1], operator.sub, False, moveList, piece, board, checkProtected)
    moveList = check_rook_direction(start[0], start[1], operator.add, False, moveList, piece, board, checkProtected)
    moveList = check_rook_direction(start[1], start[0], operator.sub, True, moveList, piece, board, checkProtected)
    moveList = check_rook_direction(start[1], start[0], operator.add, True, moveList, piece, board, checkProtected)
    return moveList
            
def check_rook_direction(dynamic, static, operation, dynamic_column, moveList, piece, board, checkProtected):
    for i in range(1, 9):
        if dynamic_column:
            space = (static, operation(dynamic, i))
        else:
            space = (operation(dynamic, i), static)
        if space[0] < 0 or space[1] < 0 or space[0] > 7 or space[1] > 7:
            return moveList
        if not checkProtected:
            if piece in range(17, 33):
                if board[space[0]][space[1]] in range(17, 33):
                    return moveList
                elif board[space[0]][space[1]] in range(1, 17):
                    moveList.append(space)
                    return moveList
            else:
                if board[space[0]][space[1]] in range(1, 17):
                    return moveList
                elif board[space[0]][space[1]] in range(17, 33):
                    moveList.append(space)
                    return moveList
        else:
            if board[space[0]][space[1]] in range(1, 33):
                moveList.append(space)
                return moveList
        if board[space[0]][space[1]] == 0:
            moveList.append(space)
    return moveList



def valid_moves_queen(start, board, piece, checkProtected):
    moveList = []
    moveList += valid_moves_rook(start, board, piece, checkProtected)
    moveList += valid_moves_bishop(start, board, piece, checkProtected)
    return moveList



def valid_moves_king(start, board, piece, checkProtected):
    moveList = [
        (start[0], start[1] + 1),
        (start[0], start[1] - 1),
        (start[0] - 1, start[1]),
        (start[0] + 1, start[1]),
        (start[0] + 1, start[1] - 1),
        (start[0] + 1, start[1] + 1),
        (start[0] - 1, start[1] + 1),
        (start[0] - 1, start[1] - 1)
    ]
    invalidMoves = []

    if piece == 17:
        invalidMoves += attacked_spaces(board, True, checkProtected)
    else:
        invalidMoves += attacked_spaces(board, False, checkProtected)

    for move in moveList:
        if move[0] < 0 or move[1] < 0 or move[0] > 7 or move[1] > 7:
            invalidMoves.append(move)
            continue
        if piece == 17:
            if board[move[0]][move[1]] in range(18, 33):
                invalidMoves.append(move)
        else:
            if board[move[0]][move[1]] in range(2, 17):
                invalidMoves.append(move)

    for move in invalidMoves:
        if move in moveList:
            moveList.remove(move)

    return moveList

def pawn_attacks(start, white):
    if white:
        attackMoves = [(start[0] + 1, start[1] - 1), (start[0] - 1, start[1] - 1)]
    else:
        attackMoves = [(start[0] + 1, start[1] + 1), (start[0] - 1, start[1] + 1)]

    moves = []
    for move in attackMoves:
        if move[0] < 0 or move[1] < 0 or move[0] > 7 or move[1] > 7:
            continue
        moves.append(move)
    
    return moves

def attacked_spaces(board, white, checkProtected):
    invalidMoves = []
    for i in range(len(board)):
        for j in range(len(board)):
            if white:
                if board[i][j] in range(9, 17):
                    invalidMoves += pawn_attacks((i, j), True)
                elif board[i][j] in range(7, 9):
                    invalidMoves += valid_moves_rook((i, j), board, board[i][j], checkProtected)
                elif board[i][j] in range(5, 7):
                    invalidMoves += valid_moves_knight((i, j), board, board[i][j], checkProtected)
                elif board[i][j] in range(3, 5):
                    invalidMoves += valid_moves_bishop((i, j), board, board[i][j], checkProtected)
                elif board[i][j] == 2:
                    invalidMoves += valid_moves_queen((i, j), board, board[i][j], checkProtected)
                elif board[i][j] == 1:
                    invalidMoves += [(i, j + 1), (i, j - 1), (i - 1, j), (i + 1, j), (i + 1, j - 1), (i + 1, j + 1), (i - 1, j + 1), (i - 1, j - 1)]
            else:
                if board[i][j] in range(25, 33):
                    invalidMoves += pawn_attacks((i, j), False)
                elif board[i][j] in range(23, 25):
                    invalidMoves += valid_moves_rook((i, j), board, board[i][j], checkProtected)
                elif board[i][j] in range(21, 23):
                    invalidMoves += valid_moves_knight((i, j), board, board[i][j], checkProtected)
                elif board[i][j] in range(19, 21):
                    invalidMoves += valid_moves_bishop((i, j), board, board[i][j], checkProtected)
                elif board[i][j] == 18:
                    invalidMoves += valid_moves_queen((i, j), board, board[i][j], checkProtected)
                elif board[i][j] == 17:
                    invalidMoves += [(i, j + 1), (i, j - 1), (i - 1, j), (i + 1, j), (i + 1, j - 1), (i + 1, j + 1), (i - 1, j + 1), (i - 1, j - 1)]
    
    return invalidMoves