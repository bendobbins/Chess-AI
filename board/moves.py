import operator

def valid_moves_pawn(start, board, piece):
    """
    Given a starting space, a chess board, the type of piece and the amount of times that piece has moved,
    return a list of tuples where each tuple is a possible space for a pawn to move.

    start -- Tuple of the space the piece starts from\n
    board -- List of lists representing a chess board and its pieces\n
    piece -- Integer representing a type of chess piece\n
    moveCounter -- Integer representing how many times a piece has moved\n
    """
    moveList = []
    # Black piece
    if piece in range(21, 41):
        # Check pawn attack moves
        moveList = check_pawn_move(board, (start[0] + 1, start[1] + 1), moveList, False)
        if start[0] != 0:
            moveList = check_pawn_move(board, (start[0] - 1, start[1] + 1), moveList, False)
        
        # If there is not a piece in front of the pawn
        if not board[start[0]][start[1] + 1]:
            # If pawn has not moved yet (it should still be in the 1st column, which is the starting column for black pawns)
            # If there is not a piece 2 spaces in front of the pawn
            if start[1] == 1 and not board[start[0]][start[1] + 2]:
                # Add possible moves
                moveList.append((start[0], start[1] + 2))
            moveList.append((start[0], start[1] + 1))

    # White piece
    else:
        # Same as above
        moveList = check_pawn_move(board, (start[0] + 1, start[1] - 1), moveList, True)
        if start[0] != 0:
            moveList = check_pawn_move(board, (start[0] - 1, start[1] - 1), moveList, True)
        if not board[start[0]][start[1] - 1]:
            if start[1] == 6 and not board[start[0]][start[1] - 2]:
                moveList.append((start[0], start[1] - 2))
            moveList.append((start[0], start[1] - 1))

    return moveList


def check_pawn_move(board, space, moveList, white):
    """
    Given a list of lists representing a chess board, a space to move to, a list of possible moves, and
    a bool representing the color of the piece being checked, return the list of possible moves with any new possible moves added.
    """
    try:
        # If there is a piece to attack in the space, add the space to the list
        if white:
            if board[space[0]][space[1]] in range(21, 41):
                moveList.append((space[0], space[1]))
        else:
            if board[space[0]][space[1]] in range(1, 21):
                moveList.append((space[0], space[1]))
    
    # If move is out of board
    except IndexError:
        pass

    return moveList




def valid_moves_knight(start, board, piece, checkProtected):
    """
    Given a starting space, a chess board, the type of piece and a bool for whether to include squares with 
    friendly pieces, return a list of tuples where each tuple is a possible space for a knight to move.

    start -- Tuple of the space the piece starts from\n
    board -- List of lists representing a chess board and its pieces\n
    piece -- Integer representing a type of chess piece\n
    checkProtected -- Bool for whether to include spaces occupied by friendly pieces\n
    """
    moveList = []
    # List of all possible moves for a knight
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
        # Black
        if piece in range(21, 41):
            moveList = check_knight_move(board, move, moveList, False, checkProtected)
        # White
        else:
            moveList = check_knight_move(board, move, moveList, True, checkProtected)

    return moveList


def check_knight_move(board, space, moveList, white, checkProtected):
    """
    Check if a space on a board is a possible move for a knight, add it to moveList if it is.
    Return moveList.
    """
    # If space is not on board
    if space[0] < 0 or space[1] < 0 or space[0] > 7 or space[1] > 7:
        return moveList

    # Only add empty spaces and spaces with enemies
    if not checkProtected:
        if white:
            if board[space[0]][space[1]] == 0 or board[space[0]][space[1]] in range(21, 41):
                moveList.append((space[0], space[1]))
        else:
            if board[space[0]][space[1]] in range(0, 21):
                moveList.append((space[0], space[1]))

    # Add any valid space
    else:
        moveList.append(space)

    return moveList




def valid_moves_bishop(start, board, piece, checkProtected):
    """
    Given a starting space, a chess board, the type of piece and a bool for whether to include squares with 
    friendly pieces, return a list of tuples where each tuple is a possible space for a bishop to move.

    start -- Tuple of the space the piece starts from\n
    board -- List of lists representing a chess board and its pieces\n
    piece -- Integer representing a type of chess piece\n
    checkProtected -- Bool for whether to include spaces occupied by friendly pieces\n
    """
    moveList = []
    # Directions that a bishop can move in
    directions = [
        (operator.sub, operator.add),
        (operator.sub, operator.sub),
        (operator.add, operator.add),
        (operator.add, operator.sub)
    ]

    for direction in directions:
        for i in range(1, 9):
            # Bishop always moves +1 square NS and +1 square EW, so use operators and incrementation to check
            # all possible moves in each direction
            space = (direction[0](start[0], i), direction[1](start[1], i))

            # If a space is outside the board, there are no more possible spaces in that direction, so move to next direction
            if space[0] < 0 or space[1] < 0 or space[0] > 7 or space[1] > 7:
                break

            # Only consider spaces with enemies
            if not checkProtected:
                # Black
                if piece in range(21, 41):
                    # If piece is friendly, don't add to list and move to next direction since bishop can't move further
                    if board[space[0]][space[1]] in range(21, 41):
                        break
                    # If piece is enemy, add to list and move to next direction since bishop can't move further
                    elif board[space[0]][space[1]] in range(1, 21):
                        moveList.append(space)     
                        break
                # White
                else:
                    # Same as above
                    if board[space[0]][space[1]] in range(1, 21):
                        break
                    elif board[space[0]][space[1]] in range(21, 41):
                        moveList.append(space)     
                        break

            # Consider spaces with friendlies and enemies
            else:
                if board[space[0]][space[1]] in range(1, 41):
                    moveList.append(space)     
                    break

            # Always add empty spaces
            if board[space[0]][space[1]] == 0:
                moveList.append(space)
    
    return moveList




def valid_moves_rook(start, board, piece, checkProtected):
    """
    Given a starting space, a chess board, the type of piece and a bool for whether to include squares with 
    friendly pieces, return a list of tuples where each tuple is a possible space for a rook to move.

    start -- Tuple of the space the piece starts from\n
    board -- List of lists representing a chess board and its pieces\n
    piece -- Integer representing a type of chess piece\n
    checkProtected -- Bool for whether to include spaces occupied by friendly pieces\n
    """
    moveList = []
    # Start[0]: starting row
    # Start[1]: starting column
    moveList = check_rook_direction(start[0], start[1], operator.sub, False, moveList, piece, board, checkProtected)
    moveList = check_rook_direction(start[0], start[1], operator.add, False, moveList, piece, board, checkProtected)
    moveList = check_rook_direction(start[1], start[0], operator.sub, True, moveList, piece, board, checkProtected)
    moveList = check_rook_direction(start[1], start[0], operator.add, True, moveList, piece, board, checkProtected)
    return moveList

            
def check_rook_direction(dynamic, static, operation, dynamic_column, moveList, piece, board, checkProtected):
    """
    Add all possible spaces to move to in a column or row to a list and return the list.

    dynamic -- Integer representing row or column to be changed to check for valid spaces\n
    static -- Integer representing row or column to stay the same while dynamic is being changed (so that only movements in one NSEW direction are checked)\n
    operation -- Operator that will be used to change dynamic\n
    dynamic_column -- Bool representing whether dynamic is a column or row\n
    moveList -- List of possible moves for piece\n
    piece -- Integer representing a type of chess piece\n
    board -- List of lists representing a chess board\n
    checkProtected -- Bool for whether to include spaces with friendly pieces as possible moves\n
    """
    for i in range(1, 9):

        # Add/subtract from column or row 1 at a time to check all possible spaces in a column/row
        if dynamic_column:
            space = (static, operation(dynamic, i))
        else:
            space = (operation(dynamic, i), static)

        # If space is out of board, no more moves are possible in that direction, so return list
        if space[0] < 0 or space[1] < 0 or space[0] > 7 or space[1] > 7:
            return moveList

        # Only consider enemy spaces
        if not checkProtected:
            # Black
            if piece in range(21, 41):
                # Same idea as bishop
                if board[space[0]][space[1]] in range(21, 41):
                    return moveList
                elif board[space[0]][space[1]] in range(1, 21):
                    moveList.append(space)
                    return moveList
            # White
            else:
                # Same idea as bishop
                if board[space[0]][space[1]] in range(1, 21):
                    return moveList
                elif board[space[0]][space[1]] in range(21, 41):
                    moveList.append(space)
                    return moveList
        
        # Consider all occupied spaces
        else:
            if board[space[0]][space[1]] in range(1, 41):
                moveList.append(space)
                return moveList
    
        # Always add empty spaces
        if board[space[0]][space[1]] == 0:
            moveList.append(space)

    return moveList




def valid_moves_queen(start, board, piece, checkProtected):
    """
    Given a starting space, a chess board, the type of piece and a bool for whether to include squares with 
    friendly pieces, return a list of tuples where each tuple is a possible space for a queen to move.

    start -- Tuple of the space the piece starts from\n
    board -- List of lists representing a chess board and its pieces\n
    piece -- Integer representing a type of chess piece\n
    checkProtected -- Bool for whether to include spaces occupied by friendly pieces\n
    """
    moveList = []
    # Queen is just bishop + rook
    moveList += valid_moves_rook(start, board, piece, checkProtected)
    moveList += valid_moves_bishop(start, board, piece, checkProtected)
    return moveList




def valid_moves_king(start, board, piece, checkProtected):
    """
    Given a starting space, a chess board, the type of piece and a bool for whether to include squares with 
    friendly pieces, return a list of tuples where each tuple is a possible space for a king to move.

    start -- Tuple of the space the piece starts from\n
    board -- List of lists representing a chess board and its pieces\n
    piece -- Integer representing a type of chess piece\n
    checkProtected -- Bool for whether to include spaces occupied by friendly pieces\n
    """
    # All possible moves for a king
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

    # All spaces attacked by the other color are invalid moves for a king
    if piece == 21:
        invalidMoves += board.attacked_spaces(checkProtected)
    else:
        invalidMoves += board.attacked_spaces(checkProtected)

    for move in moveList:
        # If the move is out of the board, it is invalid
        if move[0] < 0 or move[1] < 0 or move[0] > 7 or move[1] > 7:
            invalidMoves.append(move)
            continue

        # Squares with black pieces are invalid for black king, vice versa for white
        if piece == 21:
            if board.board[move[0]][move[1]] in range(22, 41):
                invalidMoves.append(move)
        else:
            if board.board[move[0]][move[1]] in range(2, 21):
                invalidMoves.append(move)

    # Remove all possible moves that are invalid
    for move in invalidMoves:
        if move in moveList:
            moveList.remove(move)

    return moveList




def pawn_attacks(start, white):
    """
    Given a tuple start space and a bool for color, return possible squares that a pawn can attack.
    """
    # Attacking moves for a pawn of either color
    if white:
        attackMoves = [(start[0] + 1, start[1] - 1), (start[0] - 1, start[1] - 1)]
    else:
        attackMoves = [(start[0] + 1, start[1] + 1), (start[0] - 1, start[1] + 1)]

    moves = []
    # Remove invalid moves
    for move in attackMoves:
        if move[0] < 0 or move[1] < 0 or move[0] > 7 or move[1] > 7:
            continue
        moves.append(move)
    
    return moves




def parse_attacked(attacked):
    # Remove attacks outside of board range
    removes = []
    for attack in attacked:
        if attack[0] < 0 or attack[1] < 0 or attack[0] > 7 or attack[1] > 7:
            removes.append(attack)
    for attack in removes:
        attacked.remove(attack)
    return attacked