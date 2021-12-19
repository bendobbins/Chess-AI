import pygame.image

class Pieces:
    def __init__(self):
        self.pieces = {
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

    def piece(self, type):
        return self.pieces[type]