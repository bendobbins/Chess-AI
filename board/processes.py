from moves import *
from constants import *

def checkmate_draw(board, whiteAttacking, range_):
    """
    Given a bool indicating which color to get attacked spaces for and a range of pieces for the color whose turn it is,
    return bools for checkmate or stalemate against the color whose turn it is.
    """
    checkmate, draw = False, False

    # Get spaces being attacked by white if white is true, else get spaces attacked by black
    attacked = board.attacked_spaces(False)

    # Find king for color whose turn it is
    for i in range(len(board.board)):
        for j in range(len(board.board)):
            if (board.board[i][j] == 1 and not whiteAttacking) or (board.board[i][j] == 21 and whiteAttacking):
                king = (i, j)

    kingMoves = valid_moves_king(king, board, board.board[king[0]][king[1]], True)

    # If the king is being attacked and has no valid moves, check for checkmate
    if king in attacked and not kingMoves:
        checkmate = check_checkmate(board, whiteAttacking, range_, king)

    # Check for draw
    draw = check_draw(board, range_, kingMoves)

    return checkmate, draw




def check_checkmate(board, range_, king):
    """
    Given a bool indicating which color to get attacked spaces for, a range of pieces for the color whose turn it is and
    the square of the king for the color whose turn it is, return True if the king is in checkmate, and False if not.
    """
    # Check each piece that isn't the king for the color whose turn it is
    for i in range_:
        for j in range(len(board.board)):
            for k in range(len(board.board)):

                # If the piece is found on the board, select its square
                if board.board[j][k] == i:
                    selected = (j, k)

                    # Get possible moves for the piece
                    moves, _, epMove = board.get_moves(selected)

                    for move in moves:
                        # Simulate each move
                        movePiece = board.board[move[0]][move[1]]
                        board.board[move[0]][move[1]] = board.board[selected[0]][selected[1]]
                        board.board[selected[0]][selected[1]] = 0

                        # Check if the king is still being attacked after the move
                        attacked = board.attacked_spaces(False)

                        # Undo the move
                        board.board[selected[0]][selected[1]] = board.board[move[0]][move[1]]
                        board.board[move[0]][move[1]] = movePiece

                        # If the king is not being attacked after some move, then there is a possible move and no checkmate
                        if king not in attacked:
                            return False

                    # Do same for en passant move
                    if epMove:
                        movePiece = board.board[board.lastMove[1][0]][board.lastMove[1][1]]
                        board.board[epMove[0]][epMove[1]] = board.board[selected[0]][selected[1]]
                        board.board[selected[0]][selected[1]] = 0
                        board.board[board.lastMove[1][0]][board.lastMove[1][1]] = 0

                        # Check if the king is still being attacked after the move
                        attacked = board.attacked_spaces(False)

                        # Undo the move
                        board.board[selected[0]][selected[1]] = board.board[epMove[0]][epMove[1]]
                        board.board[epMove[0]][epMove[1]] = 0
                        board.board[board.lastMove[1][0]][board.lastMove[1][1]] = movePiece

                        # If the king is not being attacked after some move, then there is a possible move and no checkmate
                        if king not in attacked:
                            return False

    # If all possible moves for all possible pieces are checked and the king is never not attacked, checkmate
    return True




def check_draw(board, range_, kingMoves):
    """
    Given a range of pieces for the color whose turn it is and the possible moves for the king whose turn it is,
    return True if there is a draw and False otherwise.
    """
    totalMoves = []

    # If each player has gone 50 moves without moving a pawn or taking a piece there is a draw
    if board.fiftyMoveCounter == 100:
        return True

    # If a board state is repeated 3 times, there is a draw
    if TRACK_REPETITION:
        for b in board.repetition:
            if board.repetition.count(b) == 3:
                return True

    if not kingMoves:
        for i in range_:
            for j in range(len(board.board)):
                for k in range(len(board.board)):
                    if board.board[j][k] == i:
                        # Get possible moves for all non-king pieces
                        tMoves, castleMoves, epMove = board.get_moves((j, k))
                        if epMove:
                            totalMoves += tMoves + castleMoves + [epMove]
                        else:
                            totalMoves += tMoves + castleMoves
        # If the king has no moves and the rest of the pieces have no moves, there is a draw
        if not totalMoves:
            return True

    # List all pieces on the board
    pieces = []
    for i in range(len(board.board)):
        for j in range(len(board.board)):
            if board.board[i][j]:
                pieces.append(board.board[i][j])
    pieces.sort()
    # If the pieces on the board cannot produce a checkmate if both players play optimally, there is a draw
    for scenario in INSUFFICIENTMATERIAL:
        scenario.sort()
        if pieces == scenario:
            return True

    return False