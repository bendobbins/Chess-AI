import pygame
import sys

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
    [10, 8, 9, 11, 12, 9, 8, 10],
    [7, 7, 7, 7, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [4, 2, 3, 5, 6, 3, 2, 4]
]

PIECES = {
    1: pygame.image.load("img/whitePawn.png").convert_alpha(),
    2: pygame.image.load("img/whiteKnight.png").convert_alpha(),
    3: pygame.image.load("img/whiteBishop.png").convert_alpha(),
    4: pygame.image.load("img/whiteRook.png").convert_alpha(),
    5: pygame.image.load("img/whiteQueen.png").convert_alpha(),
    6: pygame.image.load("img/whiteKing.png").convert_alpha(),
    7: pygame.image.load("img/blackPawn.png").convert_alpha(),
    8: pygame.image.load("img/blackKnight.png").convert_alpha(),
    9: pygame.image.load("img/blackBishop.png").convert_alpha(),
    10: pygame.image.load("img/blackRook.png").convert_alpha(),
    11: pygame.image.load("img/blackQueen.png").convert_alpha(),
    12: pygame.image.load("img/blackKing.png").convert_alpha()
}


def get_box_placement(x, y):
    """
    Finds and returns the window coordinates for box (x, y) in the grid.
    """
    left = MARGIN + BOXSIZE * x 
    top = MARGIN + BOXSIZE * y
    return left, top


class Board:
    def __init__(self, activeBoard):
        self.selected = None
        self.activeBoard = activeBoard

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
        if self.activeBoard[space[1]][space[0]]:
            return PIECES[self.activeBoard[space[1]][space[0]]]
        return None


def main():
    pygame.display.set_caption("Chess")
    board = Board(START)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        DISPLAY.fill(BLACK)
        board.draw_board()
        pygame.display.update()


if __name__ == "__main__":
    main()