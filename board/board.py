import copy
from constants import *
from moves import *
from helper import display_pawn_upgrade_choice



class Board:
    """
    Creates chess board with pieces and handles piece movement as well as win conditions.
    """
    
    def __init__(self, board=copy.deepcopy(START), realBoard=True, white=True):
        self.board = board
        self.whiteTurn = white
        self.lastMove = [(0, 0), (0, 0)]
        self.moveCounter = {i: 0 for i in range(1, 41)}
        self.fiftyMoveCounter = 0
        self.repetition = []
        self.realBoard = realBoard
        self.log = {}
        self.move = 1





    
    def change_turn(self):
        self.whiteTurn = not self.whiteTurn






    def move_piece(self, selected, moveSpace):
        """
        # TODO
        """
        castle = False
        upgradePiece = None
        # Get the possible moves for the piece in the currently selected square
        possibleMoves, castleMoves, enPassantMove = self.get_moves(selected)

        # If the moveSpace is a possible move for the piece in the currently selected square and the moveSpace is not a king (kings cannot be taken)
        validMove = ((possibleMoves or castleMoves or enPassantMove) and 
                     (moveSpace in possibleMoves or moveSpace in castleMoves or moveSpace == enPassantMove) and 
                     (self.board[moveSpace[0]][moveSpace[1]] != 1 and self.board[moveSpace[0]][moveSpace[1]] != 21))

        if validMove:
            # Logic for if the move is a castle
            if moveSpace in castleMoves:
                # White castle kingside
                if moveSpace == (6, 7):
                    self.make_castle_move([(6, 7), (5, 7), (4, 7), (7, 7)], [1, 8])

                # White castle queenside
                elif moveSpace == (2, 7):
                    self.make_castle_move([(2, 7), (3, 7), (4, 7), (0, 7)], [1, 7])
            
                # Black castle kingside
                elif moveSpace == (6, 0):
                    self.make_castle_move([(6, 0), (5, 0), (4, 0), (7, 0)], [21, 28])

                # Black castle kingside
                else:
                    self.make_castle_move([(2, 0), (3, 0), (4, 0), (0, 0)], [21, 27])

                self.lastMove = [selected, moveSpace]
                self.fiftyMoveCounter += 1
                if TRACK_REPETITION:
                    self.repetition.append(copy.deepcopy(self.board))
                castle = True

            # moveSpace is not a castle move (normal or en passant)
            else:
                # If the move is normal
                if moveSpace in possibleMoves:
                    # Make the move but keep the value of the spot that was moved to so that it can be replaced if the move is invalid
                    movePiece = self.board[moveSpace[0]][moveSpace[1]]
                    self.board[moveSpace[0]][moveSpace[1]] = self.board[selected[0]][selected[1]]
                    self.board[selected[0]][selected[1]] = 0
                else:
                    # Make en passant move but keep the value of the spot that was moved to so that it can be replaced if the move is invalid
                    movePiece = self.board[self.lastMove[1][0]][self.lastMove[1][1]]
                    self.board[moveSpace[0]][moveSpace[1]] = self.board[selected[0]][selected[1]]
                    self.board[selected[0]][selected[1]] = 0
                    self.board[self.lastMove[1][0]][self.lastMove[1][1]] = 0


                # Get attacked spaces on new board
                attacked = self.attacked_spaces(False)

                for space in attacked:
                    # If king is attacked after move, cancel move and set selected to None
                    kingAttacked = ((self.whiteTurn and self.board[space[0]][space[1]] == 1) or 
                                    (not self.whiteTurn and self.board[space[0]][space[1]] == 21))
                    
                    if kingAttacked:
                        # Restore board to previous state for normal move
                        if moveSpace in possibleMoves:
                            self.board[selected[0]][selected[1]] = self.board[moveSpace[0]][moveSpace[1]]
                            self.board[moveSpace[0]][moveSpace[1]] = movePiece
                        # Restore board to previous state for en passant move
                        else:
                            self.board[selected[0]][selected[1]] = self.board[moveSpace[0]][moveSpace[1]]
                            self.board[moveSpace[0]][moveSpace[1]] = 0
                            self.board[self.lastMove[1][0]][self.lastMove[1][1]] = movePiece
                        # Return None instead of False here to distinguish between a move that is invalid 
                        # and a move that would be valid but would put the king in check
                        return None

                # Fifty moves by each player without moving a pawn or taking a piece leads to draw
                # Update self.fiftyMoveCounter accordingly
                checkFifty = (self.board[moveSpace[0]][moveSpace[1]] not in range(9, 17) and 
                              self.board[moveSpace[0]][moveSpace[1]] not in range(29, 37) and 
                              movePiece == 0)
                
                if checkFifty:
                    self.fiftyMoveCounter += 1
                else:
                    self.fiftyMoveCounter = 0

                # Check if a pawn is moving to the last rank
                upgrade = self.check_pawn_upgrade(moveSpace)

                # Change pawn if it is moving to last rank
                if upgrade:
                    # Get the piece the player wants to upgrade to
                    if self.realBoard:
                        upgradePiece = display_pawn_upgrade_choice()
                    else:
                        # TODO for AI/Testing
                        # Probably add a new function specifically for testing/AI to move piece
                        pass

                    # Change pawn to upgraded piece
                    if self.whiteTurn:
                        self.board[moveSpace[0]][moveSpace[1]] = UPGRADEPIECES[upgradePiece.upper()]
                    else:
                        self.board[moveSpace[0]][moveSpace[1]] = UPGRADEPIECES[upgradePiece]


                # Add move to move counter
                self.moveCounter[self.board[moveSpace[0]][moveSpace[1]]] += 1

                # Keep track of last move for en passant
                self.lastMove = [selected, moveSpace]

                # Keep track of all board positions and how many times they have repeated
                if TRACK_REPETITION:
                    self.repetition.append(copy.deepcopy(self.board))

            # Return True and change turn if move is valid and has been made
            self.update_log(selected, moveSpace, castle, upgradePiece)
            self.change_turn()
            return True
        # Return False if not valid
        return False






    def get_moves(self, selected):
        """
        Returns all possible moves for the piece that is on the currently selected square in the form of a list of tuples where each
        tuple is a possible square to move to.
        """
        castleMoves = []
        enPassantMove = None

        # Get the piece being moved
        piece = self.board[selected[0]][selected[1]]

        # If a pawn is being moved
        if piece in range(9, 17) or piece in range(29, 37):
            moves = valid_moves_pawn(selected, self.board, piece)
            enPassantMove = self.en_passant(selected)

        # If a knight is being moved
        elif piece in range(5, 7) or piece in range(25, 27) or piece == 19 or piece == 39:
            moves = valid_moves_knight(selected, self.board, piece, False)

        # If a bishop is being moved
        elif piece in range(3, 5) or piece in range(23, 25) or piece == 18 or piece == 38:
            moves = valid_moves_bishop(selected, self.board, piece, False)

        # If a rook is being moved
        elif piece in range(7, 9) or piece in range(27, 29) or piece == 20 or piece == 40:
            moves = valid_moves_rook(selected, self.board, piece, False)

        # If a queen is being moved
        elif piece == 2 or piece == 22 or piece == 17 or piece == 37:
            moves = valid_moves_queen(selected, self.board, piece, False)

        # If a king is being moved
        else:
            moves = valid_moves_king(selected, self, piece, True)
            castleMoves = self.valid_moves_castle(selected)

        return [moves, castleMoves, enPassantMove]






    def attacked_spaces(self, checkProtected):
        """
        Given a list of lists representing a chess board, a bool for the color of the pieces to check attacked squares for and
        a bool for whether or not to include squares with friendly pieces as attacked squares, return a list of all squares attacked
        by all pieces of the indicated color.
        """
        attacked = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):

                currentSpace = self.board[i][j]

                # Find all squares attacked by white
                if not self.whiteTurn:
                    if currentSpace in range(9, 17):
                        attacked += pawn_attacks((i, j), True)
                    elif currentSpace in range(7, 9) or currentSpace == 20:
                        attacked += valid_moves_rook((i, j), self.board, currentSpace, checkProtected)
                    elif currentSpace in range(5, 7) or currentSpace == 19:
                        attacked += valid_moves_knight((i, j), self.board, currentSpace, checkProtected)
                    elif currentSpace in range(3, 5) or currentSpace == 18:
                        attacked += valid_moves_bishop((i, j), self.board, currentSpace, checkProtected)
                    elif currentSpace == 2 or currentSpace == 17:
                        attacked += valid_moves_queen((i, j), self.board, currentSpace, checkProtected)
                    # Append all possible king moves since invalid boundaries will be removed
                    elif currentSpace == 1:
                        attacked += [(i, j + 1), (i, j - 1), (i - 1, j), (i + 1, j), (i + 1, j - 1),
                                        (i + 1, j + 1), (i - 1, j + 1), (i - 1, j - 1)]

                # Find all squares attacked by black
                else:
                    if currentSpace in range(29, 37):
                        attacked += pawn_attacks((i, j), False)
                    elif currentSpace in range(27, 29) or currentSpace == 40:
                        attacked += valid_moves_rook((i, j), self.board, currentSpace, checkProtected)
                    elif currentSpace in range(25, 27) or currentSpace == 39:
                        attacked += valid_moves_knight((i, j), self.board, currentSpace, checkProtected)
                    elif currentSpace in range(23, 25) or currentSpace == 38:
                        attacked += valid_moves_bishop((i, j), self.board, currentSpace, checkProtected)
                    elif currentSpace == 22 or currentSpace == 37:
                        attacked += valid_moves_queen((i, j), self.board, currentSpace, checkProtected)
                    elif currentSpace == 21:
                        attacked += [(i, j + 1), (i, j - 1), (i - 1, j), (i + 1, j), (i + 1, j - 1),
                                        (i + 1, j + 1), (i - 1, j + 1), (i - 1, j - 1)]
        
        return list(set(parse_attacked(attacked)))






    def make_castle_move(self, spaces, kingNRook):
        """
        Given a list of spaces and a list of integers representing king and rook, move the pieces so that
        the player castles. First two tuples in spaces should be squares king and rook are moving to respectively,
        and last two should be spaces they are moving from. First value in kingNRook should be king, second should be rook.
        """
        self.board[spaces[0][0]][spaces[0][1]] = kingNRook[0]
        self.board[spaces[1][0]][spaces[1][1]] = kingNRook[1]
        self.board[spaces[2][0]][spaces[2][1]] = 0
        self.board[spaces[3][0]][spaces[3][1]] = 0
        self.moveCounter[kingNRook[0]] += 1
        self.moveCounter[kingNRook[1]] += 1






    def valid_moves_castle(self, space):
        """
        Check if the player is trying to castle and if the conditions are correct for one.
        If both are true, return True. Else return False.

        -- white -- Bool representing whose turn it is\n
        -- space -- Tuple representing the space the player is trying to move from\n
        -- moveSpace -- Tuple representing the space the player is trying to move to\n
        -- board -- 2D list representing the board
        """
        moves = []
        if self.whiteTurn:
            # Check if the player is trying to move the king
            if self.board[space[0]][space[1]] == 1:
                # Check that the player is trying to castle and that the rook is in the correct spot
                if self.board[4][7] == 1:
                    if self.board[7][7] == 8 and self.castle_valid([(6, 7), (5, 7), (4, 7)], (1, 8), False):
                        moves.append((6, 7))
                    if self.board[0][7] == 7 and self.castle_valid([(1, 7), (2, 7), (3, 7), (4, 7)], (1, 7), True):
                        moves.append((2, 7))
        else:
            if self.board[space[0]][space[1]] == 21:
                if self.board[4][0] == 21:
                    if self.board[7][0] == 28 and self.castle_valid([(6, 0), (5, 0), (4, 0)], (21, 28), False):
                        moves.append((6, 0))
                    if self.board[0][0] == 27 and self.castle_valid([(1, 0), (2, 0), (3, 0), (4, 0)], (21, 27), True):
                        moves.append((2, 0))

        return moves






    def castle_valid(self, spaces, kingNRook, queen):
        """
        Given a series of variables that help analyze whether a castle is valid, return True if the castle is
        valid and False if not.

        spaces -- List of tuples representing spaces that either must be empty or not attacked for castle to be valid\n
        kingNRook -- List of 2 integers where one represents the appropriate king and the other represents the appropriate rook\n
        queen -- Bool representing whether the castle is queenside or kingside\n
        whiteAttacking -- Bool representing whether to find spaces attacked by white or black\n
        """
        # Check if king and rook have not moved
        if self.moveCounter[kingNRook[0]] == 0 and self.moveCounter[kingNRook[1]] == 0:

            if not queen:
                # Check if spaces between king and rook are empty
                spacesEmpty = (self.board[spaces[0][0]][spaces[0][1]] == 0 and 
                               self.board[spaces[1][0]][spaces[1][1]] == 0)

                if spacesEmpty:
                    attacked = self.attacked_spaces(False)

                    # If king and spaces where king moves through are not attacked, castle is valid
                    if spaces[0] not in attacked and spaces[1] not in attacked and spaces[2] not in attacked:
                        return True

            else:
                # Check if spaces between king and rook are empty
                spacesEmpty = (self.board[spaces[0][0]][spaces[0][1]] == 0 and 
                               self.board[spaces[1][0]][spaces[1][1]] == 0 and 
                               self.board[spaces[2][0]][spaces[2][1]] == 0)

                if spacesEmpty:
                    attacked = self.attacked_spaces(False)
                    # Check if king and spaces where king moves through are not attacked
                    if spaces[1] not in attacked and spaces[2] not in attacked and spaces[3] not in attacked:
                        return True

        return False






    def en_passant(self, space):
        """
        Check if the player is trying to do an en passant and if the conditions are correct for one.
        If both are true, return the possible en passant move. Else return None.

        -- whiteTurn -- Bool representing whose turn it is\n
        -- space -- Tuple representing the space the player is trying to move from\n
        """
        if self.whiteTurn:
            # Check if last move was 2 spaces forward
            move2 = self.lastMove[1][1] - self.lastMove[0][1]
            pawnRange = range(9, 17)
            oppoPawnRange = range(29, 37)
            moveSpace = (self.lastMove[1][0], self.lastMove[1][1] - 1)
        else:
            move2 = self.lastMove[0][1] - self.lastMove[1][1]
            pawnRange = range(29, 37)
            oppoPawnRange = range(9, 17)
            moveSpace = (self.lastMove[1][0], self.lastMove[1][1] + 1)

        # Check if last piece moved two spaces, if selected piece is next to pawn that just moved, and if selected piece is a pawn
        validEnPassant = ((move2 == 2) and 
                          (space == (self.lastMove[1][0] + 1, self.lastMove[1][1]) or space == (self.lastMove[1][0] - 1, self.lastMove[1][1])) and 
                          self.board[space[0]][space[1]] in pawnRange and 
                          self.board[self.lastMove[1][0]][self.lastMove[1][1]] in oppoPawnRange)

        return moveSpace if validEnPassant else None






    def check_pawn_upgrade(self, moveSpace):
        """
        Given a bool indicating whose turn it is, the board, the selected space and the column the piece is moving to,
        return True if the piece is a pawn and is on the last rank, else False.
        """
        if self.whiteTurn:
            if self.board[moveSpace[0]][moveSpace[1]] in range(9, 17) and moveSpace[1] == 0:
                return True
        else:
            if self.board[moveSpace[0]][moveSpace[1]] in range(29, 37) and moveSpace[1] == 7:
                return True
        return False






    def move_to_str(self, start, end, upgrade):
        baseStr = STRMAPS[start[0]] + str(8 - start[1]) + STRMAPS[end[0]] + str(8 - end[1])
        baseStr = baseStr + STRMAPS[upgrade] if upgrade else baseStr
        return baseStr






    def update_log(self, selected, moveSpace, castle, upgrade):
        # Add next set of moves if new move
        if self.whiteTurn:
            self.log[self.move] = []

        # Add moves
        if castle:
            self.log[self.move].append('0-0' if moveSpace[0] == 6 else '0-0-0')
        else:
            self.log[self.move].append(self.move_to_str(selected, moveSpace, upgrade))

        # Increment move after black move to be ready for next call
        if not self.whiteTurn:
            self.move += 1