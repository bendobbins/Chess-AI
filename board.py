import pygame
import sys

from moves import valid_moves_pawn, valid_moves_knight, valid_moves_bishop, valid_moves_rook, valid_moves_queen

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


def get_box_placement(x, y):
    """
    Finds and returns the window coordinates for box (x, y) in the grid.
    """
    left = MARGIN + BOXSIZE * x 
    top = MARGIN + BOXSIZE * y
    return left, top


class Board:
    def __init__(self, activeBoard, userTurn):
        self.selected = None
        self.activeBoard = activeBoard
        self.userTurn = userTurn

    def change_turn(self):
        if self.userTurn:
            self.userTurn = False
        else:
            self.userTurn = True

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
        if self.activeBoard[space[0]][space[1]]:
            return PIECES[self.activeBoard[space[0]][space[1]]]
        return None

    def select_square(self, mouse):
        for box_x in range(FIELDSIZE):
            for box_y in range(FIELDSIZE):
                left, top = get_box_placement(box_x, box_y)
                box = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                if box.collidepoint(mouse):
                    return (box_x, box_y)
        return None

    def get_moves(self):
        if self.activeBoard[self.selected[0]][self.selected[1]] in range(9, 17) or self.activeBoard[self.selected[0]][self.selected[1]] in range(25, 33):
            return valid_moves_pawn(self.selected, self.activeBoard, self.activeBoard[self.selected[0]][self.selected[1]], MOVECOUNTER[self.activeBoard[self.selected[0]][self.selected[1]]])
        elif self.activeBoard[self.selected[0]][self.selected[1]] in range(5, 7) or self.activeBoard[self.selected[0]][self.selected[1]] in range(21, 23):
            return valid_moves_knight(self.selected, self.activeBoard, self.activeBoard[self.selected[0]][self.selected[1]])
        elif self.activeBoard[self.selected[0]][self.selected[1]] in range(3, 5) or self.activeBoard[self.selected[0]][self.selected[1]] in range(19, 21):
            return valid_moves_bishop(self.selected, self.activeBoard, self.activeBoard[self.selected[0]][self.selected[1]])
        elif self.activeBoard[self.selected[0]][self.selected[1]] in range(7, 9) or self.activeBoard[self.selected[0]][self.selected[1]] in range(23, 25):
            return valid_moves_rook(self.selected, self.activeBoard, self.activeBoard[self.selected[0]][self.selected[1]])
        elif self.activeBoard[self.selected[0]][self.selected[1]] == 2 or self.activeBoard[self.selected[0]][self.selected[1]] == 18:
            return valid_moves_queen(self.selected, self.activeBoard, self.activeBoard[self.selected[0]][self.selected[1]])

    def move_piece(self, mouse):
        if self.userTurn:
            if self.selected:
                if self.activeBoard[self.selected[0]][self.selected[1]]:
                    moveSpace = self.select_square(mouse)
                    if not moveSpace:
                        self.selected = None
                        return
                    possibleMoves = self.get_moves()
                    if possibleMoves:
                        if moveSpace in possibleMoves:
                            self.activeBoard[moveSpace[0]][moveSpace[1]] = self.activeBoard[self.selected[0]][self.selected[1]]
                            MOVECOUNTER[self.activeBoard[self.selected[0]][self.selected[1]]] += 1
                            self.activeBoard[self.selected[0]][self.selected[1]] = 0
                            # IMPORTANT self.change_turn()
                    self.selected = None
            else:
                selectedSquare = self.select_square(mouse)
                if self.activeBoard[selectedSquare[0]][selectedSquare[1]]:
                    self.selected = selectedSquare


def main():
    pygame.display.set_caption("Chess")
    userTurn = True
    board = Board(START, userTurn)

    while True:
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