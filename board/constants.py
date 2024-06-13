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
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LARGEFONT = pygame.font.SysFont("Courier", 30)
SMALLFONT = pygame.font.SysFont("Courier", 13)
NUMBERFONT = pygame.font.SysFont("Helvetica", 20)

# Window
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

# Starting chess board
START = [
    [27, 29, 0, 0, 0, 0, 9, 7],
    [25, 30, 0, 0, 0, 0, 10, 5],
    [23, 31, 0, 0, 0, 0, 11, 3],
    [22, 32, 0, 0, 0, 0, 12, 2],
    [21, 33, 0, 0, 0, 0, 13, 1],
    [24, 34, 0, 0, 0, 0, 14, 4],
    [26, 35, 0, 0, 0, 0, 15, 6],
    [28, 36, 0, 0, 0, 0, 16, 8]
]


# Map pictures of pieces to their numerical equivalents on the START board
PIECES = {}
IMGPATH = "/Users/BenDobbins/Desktop/Programming/My Projects/Chess/board/img/"
PIECES[1] = pygame.image.load(IMGPATH + "whiteKing.png").convert_alpha() 
PIECES[2] = pygame.image.load(IMGPATH + "whiteQueen.png").convert_alpha()
for i in range(3, 5):
    PIECES[i] = pygame.image.load(IMGPATH + "whiteBishop.png").convert_alpha()
for i in range(5, 7):
    PIECES[i] = pygame.image.load(IMGPATH + "whiteKnight.png").convert_alpha()
for i in range(7, 9):
    PIECES[i] = pygame.image.load(IMGPATH + "whiteRook.png").convert_alpha()
for i in range(9, 17):
    PIECES[i] = pygame.image.load(IMGPATH + "whitePawn.png").convert_alpha()
PIECES[21] = pygame.image.load(IMGPATH + "blackKing.png").convert_alpha()
PIECES[22] = pygame.image.load(IMGPATH + "blackQueen.png").convert_alpha()
for i in range(23, 25):
    PIECES[i] = pygame.image.load(IMGPATH + "blackBishop.png").convert_alpha()
for i  in range(25, 27):
    PIECES[i] = pygame.image.load(IMGPATH + "blackKnight.png").convert_alpha()
for i in range(27, 29):
    PIECES[i] = pygame.image.load(IMGPATH + "blackRook.png").convert_alpha()
for i in range(29, 37):
    PIECES[i] = pygame.image.load(IMGPATH + "blackPawn.png").convert_alpha()
extraPieces = [2, 3, 5, 7, 22, 23, 25, 27]
for i in range(17, 21):
    PIECES[i] = PIECES[extraPieces.pop(0)]
for i in range(37, 41):
    PIECES[i] = PIECES[extraPieces.pop(0)]


# Dictionary to handle upgrading pawns when they reach the last rank
UPGRADEPIECES = {pygame.K_q: 'q', pygame.K_r: 'r', pygame.K_b: 'b', pygame.K_k: 'k', 
                'Q': 17, 'B': 18, 'K': 19, 'R': 20, 'q': 37, 'b': 38, 'k': 39, 'r': 40}

# Mappings for board cols and extra pieces
STRMAPS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 17: 'Q', 18: 'R', 19: 'B', 20: 'N', 37: 'q', 38: 'r', 39: 'b', 40: 'n'}

# Combinations of pieces where game will be a stalemate if they are the only pieces left on the board and both players play optimally
INSUFFICIENTMATERIAL = [
    [1, 21],
    [1, 21, 3],
    [1, 21, 4],
    [1, 21, 5],
    [1, 21, 6],
    [1, 21, 23],
    [1, 21, 24],
    [1, 21, 25],
    [1, 21, 26],
    [1, 21, 5, 6],
    [1, 21, 25, 26],
    [1, 21, 3, 23],
    [1, 21, 3, 24],
    [1, 21, 3, 25],
    [1, 21, 3, 26],
    [1, 21, 4, 23],
    [1, 21, 4, 24],
    [1, 21, 4, 25],
    [1, 21, 4, 26],
    [1, 21, 5, 23],
    [1, 21, 5, 24],
    [1, 21, 5, 25],
    [1, 21, 5, 26],
    [1, 21, 6, 23],
    [1, 21, 6, 24],
    [1, 21, 6, 25],
    [1, 21, 6, 26]
]

# For tracking repetition stalemate
TRACK_REPETITION = False

# For markings on side of board
BOARDNUMBERS = ['8', '7', '6', '5', '4', '3', '2', '1']
BOARDLETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
BOARDWIDTHS = [62.5, 137.5, 212.5, 287.5, 362.5, 437.5, 512.5, 587.5]
BOARDHEIGHTS = [12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5]
NUMBERWIDTHS = [12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5]
NUMBERHEIGHTS = [62.5, 137.5, 212.5, 287.5, 362.5, 437.5, 512.5, 587.5]
NUMBERFONTS = [NUMBERFONT, NUMBERFONT, NUMBERFONT, NUMBERFONT, NUMBERFONT, NUMBERFONT, NUMBERFONT, NUMBERFONT]