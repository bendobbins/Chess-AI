import pygame
import sys
import copy

from moves import check_knight_move, valid_moves_pawn, valid_moves_knight, valid_moves_bishop, valid_moves_rook, valid_moves_queen, valid_moves_king, attacked_spaces

pygame.init()
pygame.font.init()

WIDTH = 650
HEIGHT = 700
BOXSIZE = 75
FIELDSIZE = 8
MARGIN = 25

WHITE = (255, 255, 255)
BROWN = (95, 50, 15)
LIGHTGREY = (225, 225, 225)
RED = (245, 87, 87)
BLACK = (0, 0, 0)
LARGEFONT = pygame.font.SysFont("Courier", 30)
BUTTONFONT = pygame.font.SysFont("Courier", 16)
SMALLFONT = pygame.font.SysFont("Courier", 13)
NUMBERFONT = pygame.font.SysFont("Helvetica", 30)

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

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

MOVECOUNTER = {}
for i in range(1, 33):
    MOVECOUNTER[i] = 0

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

FIFTYMOVECOUNTER = 0

REPITITION = []


def get_box_placement(x, y):
    """
    Finds and returns the window coordinates for box (x, y) in the grid.
    """
    left = MARGIN + BOXSIZE * x 
    top = MARGIN + BOXSIZE * y
    return left, top


def select_square(mouse):
    for box_x in range(FIELDSIZE):
        for box_y in range(FIELDSIZE):
            left, top = get_box_placement(box_x, box_y)
            box = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box.collidepoint(mouse):
                return (box_x, box_y)
    return None



class Board:
    def __init__(self, board, userTurn):
        self.selected = None
        self.board = board
        self.userTurn = userTurn
        self.whiteTurn = True

    def change_turn(self):
        #if self.userTurn:
        #    self.userTurn = False
        #else:
        #    self.userTurn = True
        if self.whiteTurn:
            self.whiteTurn = False
        else:
            self.whiteTurn = True

    def draw_board(self):
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
        if self.board[space[0]][space[1]]:
            return PIECES[self.board[space[0]][space[1]]]
        return None

    def get_moves(self):
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
        global FIFTYMOVECOUNTER, REPITITION
        if self.userTurn:
            if self.selected:
                if self.board[self.selected[0]][self.selected[1]]:
                    moveSpace = select_square(mouse)
                    if self.whiteTurn:
                        if not moveSpace or self.board[self.selected[0]][self.selected[1]] in range(17, 33):
                            self.selected = None
                            return
                    else:
                        if not moveSpace or self.board[self.selected[0]][self.selected[1]] in range(1, 17):
                            self.selected = None
                            return
                    possibleMoves = self.get_moves()
                    if possibleMoves:
                        if moveSpace in possibleMoves:
                            if self.board[moveSpace[0]][moveSpace[1]] != 1 and self.board[moveSpace[0]][moveSpace[1]] != 17:
                                newBoard = copy.deepcopy(self.board)
                                newBoard[moveSpace[0]][moveSpace[1]] = newBoard[self.selected[0]][self.selected[1]]
                                newBoard[self.selected[0]][self.selected[1]] = 0
                                if self.whiteTurn:
                                    checkForCheck = attacked_spaces(newBoard, False, False)
                                    for space in checkForCheck:
                                        if space[0] >= 0 and space[1] >= 0 and space[0] <= 7 and space[1] <= 7:
                                            if newBoard[space[0]][space[1]] == 1:
                                                self.selected = None
                                                return
                                else:
                                    checkForCheck = attacked_spaces(newBoard, True, False)
                                    for space in checkForCheck:
                                        if space[0] >= 0 and space[1] >= 0 and space[0] <= 7 and space[1] <= 7:
                                            if newBoard[space[0]][space[1]] == 17:
                                                self.selected = None
                                                return
                                if (self.board[self.selected[0]][self.selected[1]] not in range(9, 17)
                                        and self.board[self.selected[0]][self.selected[1]] not in range(25, 33)
                                            and self.board[moveSpace[0]][moveSpace[1]] == 0):
                                    FIFTYMOVECOUNTER += 1
                                else:
                                    FIFTYMOVECOUNTER = 0
                                self.board[moveSpace[0]][moveSpace[1]] = self.board[self.selected[0]][self.selected[1]]
                                MOVECOUNTER[self.board[self.selected[0]][self.selected[1]]] += 1
                                self.board[self.selected[0]][self.selected[1]] = 0
                                if len(REPITITION) < 6:
                                    REPITITION.append(moveSpace)
                                else:
                                    REPITITION.pop(0)
                                    REPITITION.append(moveSpace)
                                self.change_turn()
                    self.selected = None
            else:
                selectedSquare = select_square(mouse)
                if self.board[selectedSquare[0]][selectedSquare[1]]:
                    self.selected = selectedSquare

    def check_checkmate_draw(self):
        originalSelected = self.selected
        if self.whiteTurn:
            check, checkmate, draw = self.ccd_helper(False, range(2, 17))
        else:
            check, checkmate, draw = self.ccd_helper(True, range(18, 33))

        self.selected = originalSelected
        return check, checkmate, draw

    def ccd_helper(self, white, range_):
        check, checkmate, draw = False, False, False
        attackedSpaces = attacked_spaces(self.board, white, False)
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 1 and not white:
                    king = (i, j)
                if self.board[i][j] == 17 and white:
                    king = (i, j)
        kingMoves = valid_moves_king(king, self.board, self.board[king[0]][king[1]], True)
        if king in attackedSpaces:
            check = True
            if not kingMoves:
                checkmate = True
                return check, checkmate, draw
        draw = self.check_draw(range_, kingMoves)

        return check, checkmate, draw

    def check_draw(self, range_, kingMoves):
        totalMoves = []
        draw = False
        if FIFTYMOVECOUNTER == 100:
            draw = True
            return draw
        if len(REPITITION) == 6:
            if [REPITITION[0], REPITITION[1]] == [REPITITION[2], REPITITION[3]] == [REPITITION[4], REPITITION[5]]:
                draw = True
                return draw
        if not kingMoves:
            for i in range_:
                for j in range(len(self.board)):
                    for k in range(len(self.board)):
                        if self.board[j][k] == i:
                            self.selected = (j, k)
                            totalMoves += self.get_moves()
            if not totalMoves:
                draw = True
                return draw
        pieces = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j]:
                    pieces.append(self.board[i][j])
        pieces.sort()
        for scenario in INSUFFICIENTMATERIAL:
            scenario.sort()
            if pieces == scenario:
                draw = True
                return draw
        return draw



def main():
    pygame.display.set_caption("Chess")
    userTurn = True
    board = Board(START, userTurn)

    while True:
        check, checkmate, stalemate = board.check_checkmate_draw()
        if check:
            print("check")
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