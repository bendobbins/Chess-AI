import pygame
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

UPGRADEPIECES = {pygame.K_q: 'q', pygame.K_r: 'r', pygame.K_b: 'b',
               pygame.K_k: 'k', 'Q': 2, 'B': 3, 'K': 5, 'R': 7, 'q': 18, 'b': 19, 'k': 21, 'r': 23}

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