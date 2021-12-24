import pygame
import sys
import copy

from moves import *
from constants import *
from helper import draw_text, select_square, get_box_placement

pygame.init()


class Board:
    """
    Creates chess board with pieces and handles piece movement as well as win conditions.
    """
    
    def __init__(self, board, userTurn):
        self.selected = None
        self.board = board
        self.userTurn = userTurn
        self.whiteTurn = True


    def change_turn(self):
        """
        Change user turn and white turn.
        """
        #if self.userTurn:
        #    self.userTurn = False
        #else:
        #    self.userTurn = True
        if self.whiteTurn:
            self.whiteTurn = False
        else:
            self.whiteTurn = True


    def draw_board(self):
        """
        Draw chess board and pieces where they should be according to the current state of self.board.
        """
        counter = 0
        for box_x in range(FIELDSIZE):
            for box_y in range(FIELDSIZE):
                left, top = get_box_placement(box_x, box_y)
                pygame.draw.rect(DISPLAY, BROWN if counter % 2 == 1 else WHITE, (left, top, BOXSIZE, BOXSIZE))
                if self.draw_piece((box_x, box_y)):
                    DISPLAY.blit(self.draw_piece((box_x, box_y)), (left + 7, top + 5))
                    if (box_x, box_y) == self.selected:
                        pygame.draw.rect(DISPLAY, GREEN, (left, top, BOXSIZE, BOXSIZE), 2)
                counter += 1
            counter += 1


    def draw_piece(self, space):
        """
        If the given space in the board has a piece on it, return the picture for that piece.
        """
        if self.board[space[0]][space[1]]:
            return PIECES[self.board[space[0]][space[1]]]
        return None


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


    def change_selected(self, moveSpace):
        """
        Change highlighting if moveSpace cannot be a valid move for the player.
        """
        if self.whiteTurn:
            # Remove highlighting if click is outside grid, player tries to move piece for other color, or they click the same piece they have selected
            if (not moveSpace or (self.board[self.selected[0]][self.selected[1]] in range(21, 41) and self.board[moveSpace[0]][moveSpace[1]] == 0) or
                self.board[self.selected[0]][self.selected[1]] == self.board[moveSpace[0]][moveSpace[1]]):
                self.selected = None
                return True
            # If player clicks same color piece as they have already selected, change highlighting to new piece
            if self.board[moveSpace[0]][moveSpace[1]] in range(1, 21) or (self.board[self.selected[0]][self.selected[1]] in range(21, 41)
                and self.board[moveSpace[0]][moveSpace[1]] in range(21, 41)):
                self.selected = moveSpace
                return True

        else:
            # Same as for white, but for black
            if (not moveSpace or (self.board[self.selected[0]][self.selected[1]] in range(1, 21) and self.board[moveSpace[0]][moveSpace[1]] == 0) or
                self.board[self.selected[0]][self.selected[1]] == self.board[moveSpace[0]][moveSpace[1]]):
                self.selected = None
                return True
            if self.board[moveSpace[0]][moveSpace[1]] in range(21, 41) or (self.board[self.selected[0]][self.selected[1]] in range(1, 21)
                and self.board[moveSpace[0]][moveSpace[1]] in range(1, 21)):
                self.selected = moveSpace
                return True
        
        return False


    def move_piece(self, mouse):
        """
        Given the position of a mouse click, select the square that was clicked on if self.selected is None, otherwise
        move the piece on the selected square to the clicked on square, if the move is valid.
        """
        global FIFTYMOVECOUNTER, REPETITION, LASTMOVE
        if self.userTurn:
            if self.selected:
                # Clicked on square becomes moveSpace if a square is already selected
                moveSpace = select_square(mouse)

                # Only allow piece movement for the color whose turn it is and handle highlighting selected piece
                if self.change_selected(moveSpace):
                    return

                # Check if player is castling
                castle = self.castle(moveSpace)
                
                # Check for en passant
                en_passant = False
                if LASTMOVE:
                    if self.board[LASTMOVE[1][0]][LASTMOVE[1][1]] in range(9, 17) or self.board[LASTMOVE[1][0]][LASTMOVE[1][1]] in range(29, 37):
                        en_passant = self.enpassant(moveSpace)

                if castle:
                    LASTMOVE = []
                    FIFTYMOVECOUNTER += 1
                    REPETITION.append(copy.deepcopy(self.board))
                    self.change_turn()

                elif en_passant:
                    LASTMOVE = [self.selected, moveSpace]
                    FIFTYMOVECOUNTER = 0
                    REPETITION.append(copy.deepcopy(self.board))
                    self.change_turn()

                else:
                    # Get the possible moves for the piece in the currently selected square
                    possibleMoves = self.get_moves()

                    if possibleMoves:
                        # If the moveSpace is a possible move for the piece in the currently selected square
                        if moveSpace in possibleMoves:
                            # If the moveSpace is not a king (kings cannot be taken)
                            if self.board[moveSpace[0]][moveSpace[1]] != 1 and self.board[moveSpace[0]][moveSpace[1]] != 21:

                                # Create a copy of the board and simulate the move to see if it will put (or keep) the player's king in check
                                newBoard = copy.deepcopy(self.board)
                                newBoard[moveSpace[0]][moveSpace[1]] = newBoard[self.selected[0]][self.selected[1]]
                                newBoard[self.selected[0]][self.selected[1]] = 0
                                # Get attacked spaces on new board
                                if self.whiteTurn:
                                    attacked = attacked_spaces(newBoard, False, False)
                                else:
                                    attacked = attacked_spaces(newBoard, True, False)
                                for space in attacked:
                                    if space[0] >= 0 and space[1] >= 0 and space[0] <= 7 and space[1] <= 7:
                                        if self.whiteTurn:
                                            # If king is attacked after move, cancel move and set selected to None
                                            if newBoard[space[0]][space[1]] == 1:
                                                self.selected = None
                                                return
                                        else:
                                            # Same as above
                                            if newBoard[space[0]][space[1]] == 21:
                                                self.selected = None
                                                return

                                # Check if a pawn is moving to the last rank
                                upgradePiece = self.check_pawn_upgrade(moveSpace)

                                # Fifty moves by each player without moving a pawn or taking a piece leads to draw
                                # Update FIFTYMOVECOUNTER accordingly
                                if (self.board[self.selected[0]][self.selected[1]] not in range(9, 17)
                                        and self.board[self.selected[0]][self.selected[1]] not in range(29, 37)
                                            and self.board[moveSpace[0]][moveSpace[1]] == 0):
                                    FIFTYMOVECOUNTER += 1
                                else:
                                    FIFTYMOVECOUNTER = 0

                                # Change pawn if it is moving to last rank
                                if upgradePiece:
                                    if self.whiteTurn:
                                        newBoard[moveSpace[0]][moveSpace[1]] = UPGRADEPIECES[upgradePiece.upper()]
                                    else:
                                        newBoard[moveSpace[0]][moveSpace[1]] = UPGRADEPIECES[upgradePiece]


                                # Execute move on real board
                                MOVECOUNTER[self.board[self.selected[0]][self.selected[1]]] += 1
                                self.board = newBoard

                                # Keep track of last move for en passant
                                LASTMOVE = [self.selected, moveSpace]

                                # Keep track of all board positions and how many times they have repeated
                                REPETITION.append(newBoard)

                                self.change_turn()

                                self.selected = None                                #
                                return                                              #
                    self.selected = moveSpace                                       # Handle highlighting of pieces
                    return                                                          #
                self.selected = None                                                #

            else:
                # Only select a square if there is a piece on it
                selectedSquare = select_square(mouse)
                if selectedSquare:
                    if self.board[selectedSquare[0]][selectedSquare[1]]:
                        self.selected = selectedSquare
    

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
        MOVECOUNTER[kingNRook[0]] += 1
        MOVECOUNTER[kingNRook[1]] += 1


    def castle(self, moveSpace):
        """
        Given a space clicked on by a player, determine if the player is trying to castle, and if so,
        whether or not the castle is valid. If both are true, make the castle move and return True.
        Else return False.
        """
        if self.whiteTurn:
            if self.board[self.selected[0]][self.selected[1]] == 1:

                # White castle kingside
                if moveSpace == (6, 7):
                    if self.castle_valid([(6, 7), (5, 7), (4, 7)], [1, 8], False, False):
                        self.make_castle_move([(6, 7), (5, 7), (4, 7), (7, 7)], [1, 8])
                        return True

                # White castle queenside
                if moveSpace == (2, 7):
                    if self.castle_valid([(1, 7), (2, 7), (3, 7), (4, 7)], [1, 7], True, False):
                        self.make_castle_move([(2, 7), (3, 7), (4, 7), (0, 7)], [1, 7])
                        return True
        
        else:
            if self.board[self.selected[0]][self.selected[1]] == 21:

                # Black castle kingside
                if moveSpace == (6, 0):
                    if self.castle_valid([(6, 0), (5, 0), (4, 0)], [21, 28], False, True):
                        self.make_castle_move([(6, 0), (5, 0), (4, 0), (7, 0)], [21, 28])
                        return True

                # Black castle kingside
                elif moveSpace == (2, 0):
                    if self.castle_valid([(1, 0), (2, 0), (3, 0), (4, 0)], [21, 27], True, True):
                        self.make_castle_move([(2, 0), (3, 0), (4, 0), (0, 0)], [21, 27])
                        return True
        
        return False


    def castle_valid(self, spaces, kingNRook, queen, whiteAttacking):
        """
        Given a series of variables that help analyze whether a castle is valid, return True if the castle is
        valid and False if not.

        spaces -- List of tuples representing spaces that either must be empty or not attacked for castle to be valid\n
        kingNRook -- List of 2 integers where one represents the appropriate king and the other represents the appropriate rook\n
        queen -- Bool representing whether the castle is queenside or kingside\n
        whiteAttacking -- Bool representing whether to find spaces attacked by white or black\n
        """
        if MOVECOUNTER[kingNRook[0]] == 0 and MOVECOUNTER[kingNRook[1]] == 0:

            if not queen:
                if self.board[spaces[0][0]][spaces[0][1]] == 0 and self.board[spaces[1][0]][spaces[1][1]] == 0:
                    attacked = attacked_spaces(self.board, whiteAttacking, False)
                    if spaces[0] not in attacked and spaces[1] not in attacked and spaces[2] not in attacked:
                        return True

            else:
                if (self.board[spaces[0][0]][spaces[0][1]] == 0 
                    and self.board[spaces[1][0]][spaces[1][1]] == 0 
                        and self.board[spaces[2][0]][spaces[2][1]] == 0):
                    attacked = attacked_spaces(self.board, whiteAttacking, False)
                    if spaces[3] not in attacked and spaces[2] not in attacked and spaces[1] not in attacked:
                        return True

        return False


    def check_pawn_upgrade(self, moveSpace):
        """
        Given a space that a piece is moving to, check if the piece is a pawn and the
        space is on the last rank. If both are true, prompt the user for which piece they
        would like to upgrade to and return the first letter of that piece, else None.
        """
        def helper():
            """
            Draw a message prompting a user to click q, b, k or r and return the letter
            when it is clicked.
            """
            while True:
                for event in pygame.event.get():
                    draw_text([WIDTH / 2], [HEIGHT - 40], ["Press q for Queen, r for Rook, b for Bishop, or k for Knight"], [SMALLFONT], LIGHTGREY)
                    pygame.display.update()
                    if event.type == pygame.KEYDOWN:
                        for key in UPGRADEPIECES:
                            if event.key == key:
                                return UPGRADEPIECES[key]

        # If white pawn is on last rank
        if self.whiteTurn:
            if self.board[self.selected[0]][self.selected[1]] in range(9, 17):
                if moveSpace[1] == 0:
                    return helper()

        # If black pawn is on last rank
        else:
            if self.board[self.selected[0]][self.selected[1]] in range(29, 37):
                if moveSpace[1] == 7:
                    return helper()

        return None


    def check_game_over(self):
        """
        Check if game ending conditions have been met (checkmate/stalemate).
        Return bools for each conditions.
        """
        originalSelected = self.selected

        if self.whiteTurn:
            checkmate, draw = self.checkmate_draw(False, range(2, 21))
        else:
            checkmate, draw = self.checkmate_draw(True, range(22, 41))

        self.selected = originalSelected
        return checkmate, draw


    def checkmate_draw(self, white, range_):
        """
        Given a bool indicating which color to get attacked spaces for and a range of pieces for the color whose turn it is,
        return bools for checkmate or stalemate against the color whose turn it is.
        """
        checkmate, draw = False, False
        # Get spaces being attacked by white if white is true, else get spaces attacked by black
        attacked = attacked_spaces(self.board, white, False)

        # Find king for color whose turn it is
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 1 and not white:
                    king = (i, j)
                if self.board[i][j] == 21 and white:
                    king = (i, j)

        kingMoves = valid_moves_king(king, self.board, self.board[king[0]][king[1]], True)

        # If the king is being attacked and has no valid moves, check for checkmate
        if king in attacked and not kingMoves:
            checkmate = self.check_checkmate(white, range_, king)

        # Check for draw
        draw = self.check_draw(range_, kingMoves)

        return checkmate, draw


    def check_checkmate(self, white, range_, king):
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

                            # Check if the king is still being attacked after the move
                            attacked = attacked_spaces(newBoard, white, False)

                            # If the king is not being attacked after some move, then there is a possible move and no checkmate
                            if king not in attacked:
                                return False

        # If all possible moves for all possible pieces are checked and the king is never not attacked, checkmate
        return True


    def check_draw(self, range_, kingMoves):
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



def main():
    """
    Main function for controlling the chess board and pieces.
    """
    pygame.display.set_caption("Chess")
    userTurn = True
    board = Board(START, userTurn)

    while True:
        checkmate, stalemate = board.check_game_over()
        if checkmate:
            print("checkmate")
        if stalemate:
            print("stalemate")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                board.move_piece(mouse)
        DISPLAY.fill(BLACK)
        board.draw_board()
        pygame.display.update()


if __name__ == "__main__":
    main()