from moves import *
from constants import *
import copy

def get_moves(self):
    """
    Returns all possible moves for the piece that is on the currently selected square in the form of a list of tuples where each
    tuple is a possible square to move to.
    """
    if (self.board[self.selected[0]][self.selected[1]] in range(9, 17)
        or self.board[self.selected[0]][self.selected[1]] in range(29, 37)):
        return valid_moves_pawn(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], MOVECOUNTER[self.board[self.selected[0]][self.selected[1]]])

    elif (self.board[self.selected[0]][self.selected[1]] in range(5, 7)
        or self.board[self.selected[0]][self.selected[1]] in range(25, 27)
            or self.board[self.selected[0]][self.selected[1]] == 19
                or self.board[self.selected[0]][self.selected[1]] == 39):
        return valid_moves_knight(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], False)

    elif (self.board[self.selected[0]][self.selected[1]] in range(3, 5)
        or self.board[self.selected[0]][self.selected[1]] in range(23, 25)
            or self.board[self.selected[0]][self.selected[1]] == 18
                or self.board[self.selected[0]][self.selected[1]] == 38):
        return valid_moves_bishop(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], False)

    elif (self.board[self.selected[0]][self.selected[1]] in range(7, 9)
        or self.board[self.selected[0]][self.selected[1]] in range(27, 29)
            or self.board[self.selected[0]][self.selected[1]] == 20
                or self.board[self.selected[0]][self.selected[1]] == 40):
        return valid_moves_rook(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], False)

    elif (self.board[self.selected[0]][self.selected[1]] == 2
        or self.board[self.selected[0]][self.selected[1]] == 22
            or self.board[self.selected[0]][self.selected[1]] == 17
                or self.board[self.selected[0]][self.selected[1]] == 37):
        return valid_moves_queen(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], False)

    else:
        return valid_moves_king(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], True)


def castle_valid(self, spaces, kingNRook, queen, whiteAttacking):
    """
    Given a series of variables that help analyze whether a castle is valid, return True if the castle is
    valid and False if not.

    spaces -- List of tuples representing spaces that either must be empty or not attacked for castle to be valid\n
    kingNRook -- List of 2 integers where one represents the appropriate king and the other represents the appropriate rook\n
    queen -- Bool representing whether the castle is queenside or kingside\n
    whiteAttacking -- Bool representing whether to find spaces attacked by white or black\n
    """
    # Check if king and rook have not moved
    if MOVECOUNTER[kingNRook[0]] == 0 and MOVECOUNTER[kingNRook[1]] == 0:
        for i in range(8):
            for j in range(8):
                cboard[i][j] = self.board[i][j]

        if not queen:
            # Check if spaces between king and rook are empty
            if self.board[spaces[0][0]][spaces[0][1]] == 0 and self.board[spaces[1][0]][spaces[1][1]] == 0:
                attacked = attacked_spaces(self.board, whiteAttacking, False)

                # If king and spaces where king moves through are not attacked, castle is valid
                if spaces[0] not in attacked and spaces[1] not in attacked and spaces[2] not in attacked:
                    return True

        else:
            # Same as above, just for different spaces
            if (self.board[spaces[0][0]][spaces[0][1]] == 0 
                and self.board[spaces[1][0]][spaces[1][1]] == 0 
                    and self.board[spaces[2][0]][spaces[2][1]] == 0):
                attacked = attacked_spaces(self.board, whiteAttacking, False)
                if spaces[3] not in attacked and spaces[2] not in attacked and spaces[1] not in attacked:
                    return True

    return False


def _checkmate_draw(self, whiteAttacking, range_):
    """
    Given a bool indicating which color to get attacked spaces for and a range of pieces for the color whose turn it is,
    return bools for checkmate or stalemate against the color whose turn it is.
    """
    checkmate, draw = False, False

    for i in range(8):
        for j in range(8):
            cboard[i][j] = self.board[i][j]
    # Get spaces being attacked by white if white is true, else get spaces attacked by black
    attacked = attacked_spaces(self.board, whiteAttacking, False)

    # Find king for color whose turn it is
    for i in range(len(self.board)):
        for j in range(len(self.board)):
            if (self.board[i][j] == 1 and not whiteAttacking) or (self.board[i][j] == 21 and whiteAttacking):
                king = (i, j)

    kingMoves = valid_moves_king(king, self.board, self.board[king[0]][king[1]], True)

    # If the king is being attacked and has no valid moves, check for checkmate
    if king in attacked and not kingMoves:
        checkmate = self._check_checkmate(whiteAttacking, range_, king)

    # Check for draw
    draw = self._check_draw(range_, kingMoves)

    return checkmate, draw


def _check_checkmate(self, white, range_, king):
    """
    Given a bool indicating which color to get attacked spaces for, a range of pieces for the color whose turn it is and
    the square of the king for the color whose turn it is, return True if the king is in checkmate, and False if not.
    """
    # Check each piece that isn't the king for the color whose turn it is
    for i in range_:
        for j in range(len(self.board)):
            for k in range(len(self.board)):

                # If the piece is found on the board, select its square
                if self.board[j][k] == i:
                    self.selected = (j, k)

                    # Get possible moves for the piece
                    moves = self.get_moves()

                    for move in moves:
                        # Simulate each move
                        newBoard = copy.deepcopy(self.board)
                        newBoard[move[0]][move[1]] = newBoard[self.selected[0]][self.selected[1]]
                        newBoard[self.selected[0]][self.selected[1]] = 0

                        for l in range(8):
                            for o in range(8):
                                cboard[l][o] = newBoard[l][o]

                        # Check if the king is still being attacked after the move
                        attacked = attacked_spaces(newBoard, white, False)

                        # If the king is not being attacked after some move, then there is a possible move and no checkmate
                        if king not in attacked:
                            return False

    # If all possible moves for all possible pieces are checked and the king is never not attacked, checkmate
    return True


def _check_draw(self, range_, kingMoves):
    """
    Given a range of pieces for the color whose turn it is and the possible moves for the king whose turn it is,
    return True if there is a draw and False otherwise.
    """
    totalMoves = []

    # If each player has gone 50 moves without moving a pawn or taking a piece there is a draw
    if FIFTYMOVECOUNTER == 100:
        return True

    # If a board state is repeated 3 times, there is a draw
    for board in REPETITION:
        if REPETITION.count(board) == 3:
            return True

    if not kingMoves:
        for i in range_:
            for j in range(len(self.board)):
                for k in range(len(self.board)):
                    if self.board[j][k] == i:
                        # Get possible moves for all non-king pieces
                        self.selected = (j, k)
                        totalMoves += self.get_moves()
        # If the king has no moves and the rest of the pieces have no moves, there is a draw
        if not totalMoves:
            return True

    # List all pieces on the board
    pieces = []
    for i in range(len(self.board)):
        for j in range(len(self.board)):
            if self.board[i][j]:
                pieces.append(self.board[i][j])
    pieces.sort()
    # If the pieces on the board cannot produce a checkmate if both players play optimally, there is a draw
    for scenario in INSUFFICIENTMATERIAL:
        scenario.sort()
        if pieces == scenario:
            return True

    return False


def enpassant(self, moveSpace):
    """
    Check if the player is trying to do an en passant and if the conditions are correct for one.
    If both are true, execute the move and return True. Else return False.
    """
    if self.whiteTurn:
        # Check if last move was 2 spaces forward
        if LASTMOVE[1][1] - LASTMOVE[0][1] == 2:
            # Check if selected piece is next to pawn that just moved, and if selected piece is a pawn
            if (self.selected == (LASTMOVE[1][0] + 1, LASTMOVE[1][1]) or self.selected == (LASTMOVE[1][0] - 1, LASTMOVE[1][1])
                and self.board[self.selected[0]][self.selected[1]] in range(9, 17)):
                # Check if the player is trying to en passant
                if moveSpace == (LASTMOVE[1][0], LASTMOVE[1][1] - 1):
                    # Execute move
                    self.board[moveSpace[0]][moveSpace[1]] = self.board[self.selected[0]][self.selected[1]]
                    self.board[self.selected[0]][self.selected[1]] = 0
                    self.board[LASTMOVE[1][0]][LASTMOVE[1][1]] = 0
                    return True
                    
    else:
        # Same as above
        if LASTMOVE[0][1] - LASTMOVE[1][1] == 2:
            if (self.selected == (LASTMOVE[1][0] + 1, LASTMOVE[1][1]) or self.selected == (LASTMOVE[1][0] - 1, LASTMOVE[1][1])
                and self.board[self.selected[0]][self.selected[1]] in range(29, 37)):
                if moveSpace == (LASTMOVE[1][0], LASTMOVE[1][1] + 1):
                    self.board[moveSpace[0]][moveSpace[1]] = self.board[self.selected[0]][self.selected[1]]
                    self.board[self.selected[0]][self.selected[1]] = 0
                    self.board[LASTMOVE[1][0]][LASTMOVE[1][1]] = 0
                    return True
    
    return False