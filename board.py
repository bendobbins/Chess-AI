import pygame
import sys
import copy

from moves import valid_moves_pawn, valid_moves_knight, valid_moves_bishop, valid_moves_rook, valid_moves_queen, valid_moves_king, attacked_spaces

pygame.init()
pygame.font.init()

# Window constants
WIDTH = 650
HEIGHT = 700
BOXSIZE = 75
FIELDSIZE = 8
MARGIN = 25

# Style constants
WHITE = (255, 255, 255)
BROWN = (95, 50, 15)
LIGHTGREY = (225, 225, 225)
RED = (245, 87, 87)
BLACK = (0, 0, 0)
LARGEFONT = pygame.font.SysFont("Courier", 30)
BUTTONFONT = pygame.font.SysFont("Courier", 16)
SMALLFONT = pygame.font.SysFont("Courier", 13)
NUMBERFONT = pygame.font.SysFont("Helvetica", 30)

# Window
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

# Starting chess board
START = [
    [23, 25, 0, 0, 0, 0, 9, 7],
    [21, 26, 0, 0, 0, 0, 10, 5],
    [19, 27, 0, 0, 0, 0, 11, 3],
    [18, 28, 0, 0, 0, 0, 12, 2],
    [17, 29, 0, 0, 0, 0, 13, 1],
    [20, 30, 0, 0, 0, 0, 14, 4],
    [22, 31, 0, 0, 0, 0, 15, 6],
    [24, 32, 0, 0, 0, 0, 16, 8]
]

# Map pictures of pieces to their numerical equivalents on the START board
PIECES = {}
PIECES[1] = pygame.image.load("img/whiteKing.png").convert_alpha() 
PIECES[2] = pygame.image.load("img/whiteQueen.png").convert_alpha()
for i in range(3, 5):
    PIECES[i] = pygame.image.load("img/whiteBishop.png").convert_alpha()
for i in range(5, 7):
    PIECES[i] = pygame.image.load("img/whiteKnight.png").convert_alpha()
for i in range(7, 9):
    PIECES[i] = pygame.image.load("img/whiteRook.png").convert_alpha()
for i in range(9, 17):
    PIECES[i] = pygame.image.load("img/whitePawn.png").convert_alpha()
PIECES[17] = pygame.image.load("img/blackKing.png").convert_alpha()
PIECES[18] = pygame.image.load("img/blackQueen.png").convert_alpha()
for i in range(19, 21):
    PIECES[i] = pygame.image.load("img/blackBishop.png").convert_alpha()
for i  in range(21, 23):
    PIECES[i] = pygame.image.load("img/blackKnight.png").convert_alpha()
for i in range(23, 25):
    PIECES[i] = pygame.image.load("img/blackRook.png").convert_alpha()
for i in range(25, 33):
    PIECES[i] = pygame.image.load("img/blackPawn.png").convert_alpha()

# Mainly for telling whether pawns can move 2 spaces or not
MOVECOUNTER = {}
for i in range(1, 33):
    MOVECOUNTER[i] = 0

# Combinations of pieces where game will be a stalemate if they are the only pieces left on the board and both players play optimally
INSUFFICIENTMATERIAL = [
    [1, 17],
    [1, 17, 5],
    [1, 17, 6],
    [1, 17, 3],
    [1, 17, 4],
    [1, 17, 19],
    [1, 17, 20],
    [1, 17, 21],
    [1, 17, 22],
    [1, 17, 21, 22],
    [1, 17, 5, 6],
    [1, 17, 3, 19],
    [1, 17, 3, 20],
    [1, 17, 3, 21],
    [1, 17, 3, 22],
    [1, 17, 4, 19],
    [1, 17, 4, 20],
    [1, 17, 4, 21],
    [1, 17, 4, 22],
    [1, 17, 5, 19],
    [1, 17, 5, 20],
    [1, 17, 5, 21],
    [1, 17, 5, 22],
    [1, 17, 6, 19],
    [1, 17, 6, 20],
    [1, 17, 6, 21],
    [1, 17, 6, 22]
]

# For tracking 50 move rule stalemate
FIFTYMOVECOUNTER = 0

# For tracking repetition stalemate
REPETITION = []


def get_box_placement(x, y):
    """
    Finds and returns the window coordinates for box (x, y) in the grid.
    """
    left = MARGIN + BOXSIZE * x 
    top = MARGIN + BOXSIZE * y
    return left, top


def select_square(mouse):
    """
    Given the position of a mouse click, return a tuple of the square on the grid that was clicked, or None if no square was clicked.
    """
    for box_x in range(FIELDSIZE):
        for box_y in range(FIELDSIZE):
            left, top = get_box_placement(box_x, box_y)
            box = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box.collidepoint(mouse):
                return (box_x, box_y)
    return None



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
        if self.board[self.selected[0]][self.selected[1]] in range(9, 17) or self.board[self.selected[0]][self.selected[1]] in range(25, 33):
            return valid_moves_pawn(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], MOVECOUNTER[self.board[self.selected[0]][self.selected[1]]])
        elif self.board[self.selected[0]][self.selected[1]] in range(5, 7) or self.board[self.selected[0]][self.selected[1]] in range(21, 23):
            return valid_moves_knight(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], False)
        elif self.board[self.selected[0]][self.selected[1]] in range(3, 5) or self.board[self.selected[0]][self.selected[1]] in range(19, 21):
            return valid_moves_bishop(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], False)
        elif self.board[self.selected[0]][self.selected[1]] in range(7, 9) or self.board[self.selected[0]][self.selected[1]] in range(23, 25):
            return valid_moves_rook(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], False)
        elif self.board[self.selected[0]][self.selected[1]] == 2 or self.board[self.selected[0]][self.selected[1]] == 18:
            return valid_moves_queen(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], False)
        else:
            return valid_moves_king(self.selected, self.board, self.board[self.selected[0]][self.selected[1]], True)

    def move_piece(self, mouse):
        """
        Given the position of a mouse click, select the square that was clicked on if self.selected is None, otherwise
        move the piece on the selected square to the clicked on square, if the move is valid.
        """
        global FIFTYMOVECOUNTER, REPETITION
        if self.userTurn:
            if self.selected:
                # Clicked on square becomes moveSpace if a square is already selected
                moveSpace = select_square(mouse)

                # Only allow piece movement for the color whose turn it is
                if self.whiteTurn:
                    if not moveSpace or self.board[self.selected[0]][self.selected[1]] in range(17, 33):
                        self.selected = None
                        return
                else:
                    if not moveSpace or self.board[self.selected[0]][self.selected[1]] in range(1, 17):
                        self.selected = None
                        return

                # Get the possible moves for the piece in the currently selected square
                possibleMoves = self.get_moves()

                if possibleMoves:
                    # If the moveSpace is a possible move for the piece in the currently selected square
                    if moveSpace in possibleMoves:
                        # If the moveSpace is not a king (kings cannot be taken)
                        if self.board[moveSpace[0]][moveSpace[1]] != 1 and self.board[moveSpace[0]][moveSpace[1]] != 17:
                            # Create a copy of the board and simulate the move to see if it will put (or keep) the player's king in check
                            newBoard = copy.deepcopy(self.board)
                            newBoard[moveSpace[0]][moveSpace[1]] = newBoard[self.selected[0]][self.selected[1]]
                            newBoard[self.selected[0]][self.selected[1]] = 0
                            if self.whiteTurn:
                                attackedSpaces = attacked_spaces(newBoard, False, False)
                            else:
                                attackedSpaces = attacked_spaces(newBoard, True, False)
                            for space in attackedSpaces:
                                if space[0] >= 0 and space[1] >= 0 and space[0] <= 7 and space[1] <= 7:
                                    if self.whiteTurn:
                                        # If king is attacked after move, cancel move and set selected to None
                                        if newBoard[space[0]][space[1]] == 1:
                                            self.selected = None
                                            return
                                    else:
                                        # Same as above
                                        if newBoard[space[0]][space[1]] == 17:
                                            self.selected = None
                                            return

                            # Fifty moves by each player without moving a pawn or taking a piece leads to draw
                            # Update FIFTYMOVECOUNTER accordingly
                            if (self.board[self.selected[0]][self.selected[1]] not in range(9, 17)
                                    and self.board[self.selected[0]][self.selected[1]] not in range(25, 33)
                                        and self.board[moveSpace[0]][moveSpace[1]] == 0):
                                FIFTYMOVECOUNTER += 1
                            else:
                                FIFTYMOVECOUNTER = 0

                            # Move is valid if function gets to this point, so execute move on real board
                            MOVECOUNTER[self.board[self.selected[0]][self.selected[1]]] += 1
                            self.board = newBoard

                            # Keep track of all board positions and how many times they have repeated
                            REPETITION.append(newBoard)

                            self.change_turn()
                self.selected = None

            else:
                # Only select a square if there is a piece on it
                selectedSquare = select_square(mouse)
                if self.board[selectedSquare[0]][selectedSquare[1]]:
                    self.selected = selectedSquare

    def check_game_over(self):
        """
        Check if game ending conditions have been met (checkmate/stalemate).
        Return bools for each conditions.
        """
        originalSelected = self.selected

        if self.whiteTurn:
            checkmate, draw = self.checkmate_draw(False, range(2, 17))
        else:
            checkmate, draw = self.checkmate_draw(True, range(18, 33))

        self.selected = originalSelected
        return checkmate, draw

    def checkmate_draw(self, white, range_):
        """
        Given a bool indicating which color to get attacked spaces for and a range of pieces for the color whose turn it is,
        return bools for checkmate or stalemate against the color whose turn it is.
        """
        checkmate, draw = False, False
        # Get spaces being attacked by white if white is true, else get spaces attacked by black
        attackedSpaces = attacked_spaces(self.board, white, False)

        # Find king for color whose turn it is
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 1 and not white:
                    king = (i, j)
                if self.board[i][j] == 17 and white:
                    king = (i, j)

        kingMoves = valid_moves_king(king, self.board, self.board[king[0]][king[1]], True)

        # If the king is being attacked and has no valid moves, check for checkmate
        if king in attackedSpaces and not kingMoves:
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
                            attackedSpaces = attacked_spaces(newBoard, white, False)

                            # If the king is not being attacked after some move, then there is a possible move and no checkmate
                            if king not in attackedSpaces:
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