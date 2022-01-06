import pygame
pygame.font.init()

import ctypes
import pathlib

libname = pathlib.Path().absolute() / ".." / "engine" / "enginelib.so"
engine = ctypes.CDLL(libname)
cboard = (ctypes.c_int * 8 * 8)()
cmove = ctypes.c_int * 2
ccounter = ctypes.c_int * 40
engine.free_array.restype = None
engine.valid_pawn_moves.restype = ctypes.POINTER(ctypes.c_int)
engine.valid_knight_moves.restype = ctypes.POINTER(ctypes.c_int)
engine.valid_bishop_moves.restype = ctypes.POINTER(ctypes.c_int)
engine.valid_rook_moves.restype = ctypes.POINTER(ctypes.c_int)
engine.valid_queen_moves.restype = ctypes.POINTER(ctypes.c_int)
engine.valid_king_moves.restype = ctypes.POINTER(ctypes.c_int)
engine.attacked_spaces.restype = ctypes.POINTER(ctypes.c_int)
#engine.castle_valid.restype = ctypes.c_bool
#engine.checkmate.restype = ctypes.c_bool

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

# Functions in the c file for moves return lists of integers where each integer corresponds to a unique space on the board
# This constant dictionary maps those unique integers to their corresponding spaces on the board
REFERENCES = {}
row = 0
column = 0
for i in range(1, 65):
    REFERENCES[i] = (row, column)
    if column == 7:
        column = 0
        row += 1
    else:
        column += 1

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
PIECES[21] = pygame.image.load("img/blackKing.png").convert_alpha()
PIECES[22] = pygame.image.load("img/blackQueen.png").convert_alpha()
for i in range(23, 25):
    PIECES[i] = pygame.image.load("img/blackBishop.png").convert_alpha()
for i  in range(25, 27):
    PIECES[i] = pygame.image.load("img/blackKnight.png").convert_alpha()
for i in range(27, 29):
    PIECES[i] = pygame.image.load("img/blackRook.png").convert_alpha()
for i in range(29, 37):
    PIECES[i] = pygame.image.load("img/blackPawn.png").convert_alpha()
extraPieces = [2, 3, 5, 7, 22, 23, 25, 27]
for i in range(17, 21):
    PIECES[i] = PIECES[extraPieces.pop(0)]
for i in range(37, 41):
    PIECES[i] = PIECES[extraPieces.pop(0)]

# Mainly for telling whether pawns can move 2 spaces or not
MOVECOUNTER = {}
for i in range(1, 41):
    MOVECOUNTER[i] = 0

# Dictionary to handle upgrading pawns when they reach the last rank
UPGRADEPIECES = {pygame.K_q: 'q', pygame.K_r: 'r', pygame.K_b: 'b', pygame.K_k: 'k', 
                'Q': 17, 'B': 18, 'K': 19, 'R': 20, 'q': 37, 'b': 38, 'k': 39, 'r': 40}

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

# For tracking 50 move rule stalemate
FIFTYMOVECOUNTER = 0

# For tracking repetition stalemate
REPETITION = []

# For enpassant
LASTMOVE = []

# For markings on side of board
BOARDNUMBERS = ['8', '7', '6', '5', '4', '3', '2', '1']
BOARDLETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
BOARDWIDTHS = [62.5, 137.5, 212.5, 287.5, 362.5, 437.5, 512.5, 587.5]
BOARDHEIGHTS = [12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5]
NUMBERWIDTHS = [12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5]
NUMBERHEIGHTS = [62.5, 137.5, 212.5, 287.5, 362.5, 437.5, 512.5, 587.5]
NUMBERFONTS = [NUMBERFONT, NUMBERFONT, NUMBERFONT, NUMBERFONT, NUMBERFONT, NUMBERFONT, NUMBERFONT, NUMBERFONT]