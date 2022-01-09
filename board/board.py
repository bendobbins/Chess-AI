from constants import *
from helper import draw_text, select_square, get_box_placement, draw_buttons, start_page

pygame.init()


class Board:
    """
    Creates chess board with pieces and handles piece movement as well as win conditions.
    """
    
    def __init__(self, userTurn):
        self.selected = None
        self.board = START
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
                    # Outline selected square
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


    def reference_to_space(self, references):
        """
        Given a pointer to an array of integers created in C where every integer represents a unique space on a chess board (1-64),
        create a Python list of tuples where each tuple is the row & column values for the corresponding unique integer. Then free the 
        pointer from C and return the list of tuples.
        """
        moves = []
        # This will be 0 if there are no spaces
        if references[0]:
            for i in range(1, references[0] + 1):
                moves.append(REFERENCES[references[i]])

        engine.free_array(references)
        
        return moves


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

                # Create board as a C object
                for i in range(8):
                    for j in range(8):
                        cboard[i][j] = self.board[i][j]
                for i in range(2):
                    for j in range(2):
                        clast[i][j] = LASTMOVE[i][j]

                # Check if player is castling
                if self.castle(moveSpace):
                    LASTMOVE = [self.selected, moveSpace]
                    FIFTYMOVECOUNTER += 1
                    REPETITION.append(copy.deepcopy(self.board))
                    self.change_turn()

                # Check for en passant
                elif engine.en_passant(self.whiteTurn, clast, cboard, cmove(*self.selected), cmove(*moveSpace)):
                    self.board[moveSpace[0]][moveSpace[1]] = self.board[self.selected[0]][self.selected[1]]
                    self.board[self.selected[0]][self.selected[1]] = 0
                    self.board[LASTMOVE[1][0]][LASTMOVE[1][1]] = 0
                    LASTMOVE = [self.selected, moveSpace]
                    FIFTYMOVECOUNTER = 0
                    REPETITION.append(copy.deepcopy(self.board))
                    self.change_turn()

                else:
                    # Get the possible moves for the piece in the currently selected square
                    possibleMoves = self.reference_to_space(engine.get_moves(cboard, cmove(*self.selected), MOVECOUNTER[self.board[self.selected[0]][self.selected[1]]]))

                    if possibleMoves:
                        # If the moveSpace is a possible move for the piece in the currently selected square
                        if moveSpace in possibleMoves:
                            # If the moveSpace is not a king (kings cannot be taken)
                            if self.board[moveSpace[0]][moveSpace[1]] != 1 and self.board[moveSpace[0]][moveSpace[1]] != 21:

                                # Create a copy of the board and simulate the move to see if it will put (or keep) the player's king in check
                                newBoard = copy.deepcopy(self.board)
                                newBoard[moveSpace[0]][moveSpace[1]] = newBoard[self.selected[0]][self.selected[1]]
                                newBoard[self.selected[0]][self.selected[1]] = 0

                                # Create board object that can be passed to C
                                for i in range(8):
                                    for j in range(8):
                                        cboard[i][j] = newBoard[i][j]
                                # Get attacked spaces on new board
                                if self.whiteTurn:
                                    attacked = self.reference_to_space(engine.attacked_spaces(cboard, False, False))
                                    #attacked = attacked_spaces(newBoard, False, False)
                                else:
                                    attacked = self.reference_to_space(engine.attacked_spaces(cboard, True, False))
                                    #attacked = attacked_spaces(newBoard, True, False)
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

                                # Remove highlighting if move successful
                                self.selected = None                               
                                return                                              #
                    # Highlight clicked on piece if it is not a possible move       #
                    self.selected = moveSpace                                       # Handle highlighting of pieces
                    return                                                          #
                self.selected = None                                                #

            # If there is no square already selected
            else:
                # Only select a square if there is a piece on it
                selectedSquare = select_square(mouse)
                if selectedSquare:
                    if self.board[selectedSquare[0]][selectedSquare[1]]:
                        self.selected = selectedSquare
    

    def castle(self, moveSpace):
        """
        Given a space clicked on by a player, determine if the player is trying to castle, and if so,
        whether or not the castle is valid. If both are true, make the castle move and return True.
        Else return False.
        """
        for i in range(8):
            for j in range(8):
                cboard[i][j] = self.board[i][j]

        moveCount = []
        for key in MOVECOUNTER:
            moveCount.append(MOVECOUNTER[key])

        def make_castle_move(spaces, kingNRook):
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


        # castle()
        if engine.castle(self.whiteTurn, cmove(*self.selected), cmove(*moveSpace), cboard, ccounter(*moveCount)):
            # White castle kingside
            if moveSpace == (6, 7):
                make_castle_move([(6, 7), (5, 7), (4, 7), (7, 7)], [1, 8])

            # White castle queenside
            elif moveSpace == (2, 7):
                make_castle_move([(2, 7), (3, 7), (4, 7), (0, 7)], [1, 7])
        
            # Black castle kingside
            elif moveSpace == (6, 0):
                make_castle_move([(6, 0), (5, 0), (4, 0), (7, 0)], [21, 28])

            # Black castle kingside
            else:
                make_castle_move([(2, 0), (3, 0), (4, 0), (0, 0)], [21, 27])

            return True
        return False


    def check_pawn_upgrade(self, moveSpace):
        """
        Given a space that a piece is moving to, check if the piece is a pawn and the
        space is on the last rank. If both are true, prompt the user for which piece they
        would like to upgrade to and return the first letter of that piece, else None.
        """
        for i in range(8):
            for j in range(8):
                cboard[i][j] = self.board[i][j]

        def helper():
            """
            Draw a message prompting a user to click q, b, k or r and return the letter
            when it is clicked.
            """
            while True:
                for event in pygame.event.get():
                    draw_text([WIDTH / 2], [HEIGHT - 55], ["Press q for Queen, r for Rook, b for Bishop, or k for Knight"], [SMALLFONT], LIGHTGREY)
                    pygame.display.update()
                    if event.type == pygame.KEYDOWN:
                        for key in UPGRADEPIECES:
                            if event.key == key:
                                return UPGRADEPIECES[key]

        if engine.check_pawn_upgrade(self.whiteTurn, cboard, cmove(*self.selected), moveSpace[1]):
            return helper()
        return None


    def check_game_over(self):
        """
        Check if game ending conditions have been met (checkmate/stalemate).
        Return bools for each conditions.
        """
        originalSelected = self.selected
        for i in range(8):
            for j in range(8):
                cboard[i][j] = self.board[i][j]
        
        moveCount = []
        for key in MOVECOUNTER:
            moveCount.append(MOVECOUNTER[key])

        crepetitions = (c_int * 8 * 8 * len(REPETITION))()
        for i in range(len(REPETITION)):
            for j in range(8):
                for k in range(8):
                    crepetitions[i][j][k] = REPETITION[i][j][k]
        
        if self.whiteTurn:
            end = engine.checkmate(cboard, False, cmove(*[2, 21]), FIFTYMOVECOUNTER, ccounter(*moveCount), crepetitions, len(REPETITION))
        else:
            end = engine.checkmate(cboard, True, cmove(*[22, 41]), FIFTYMOVECOUNTER, ccounter(*moveCount), crepetitions, len(REPETITION))

        mate = True if end[0] else False
        draw = True if end[1] else False

        engine.free_array(end)

        self.selected = originalSelected
        return mate, draw


    def reset(self, userTurn):
        """
        Reset board and globals keeping track of moves.
        """
        global FIFTYMOVECOUNTER, REPETITION, LASTMOVE, MOVECOUNTER
        self.selected = None
        self.board = START
        self.userTurn = userTurn
        self.whiteTurn = True
        for i in range(1, 41):
            MOVECOUNTER[i] = 0
        FIFTYMOVECOUNTER = 0
        REPETITION = []
        LASTMOVE = [[0, 0], [0, 0]]





def main():
    """
    Main function for controlling the chess board and pieces.
    """
    pygame.display.set_caption("Chess")
    userTurn = True
    board = Board(userTurn)
    aiGame = None

    def game_over(checkmate):
        """
        For stopping gameplay and waiting for reset or quit when game end condition is met.
        """
        while True:
            for event in pygame.event.get():
                if checkmate:
                    draw_text([WIDTH / 2], [HEIGHT - 55], ["Checkmate!"], [NUMBERFONT], GREEN)
                else:
                    draw_text([WIDTH / 2], [HEIGHT - 55], ["Draw!"], [NUMBERFONT], RED)
                pygame.display.update()
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if reset.collidepoint(event.pos):
                        board.reset(userTurn)
                        return

    while True:
        # Display start page
        if aiGame is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            DISPLAY.fill(BLACK)

            # Wait for user to choose game mode
            gameButtons = start_page()
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if gameButtons[0].collidepoint(mouse):
                    aiGame = False
                elif gameButtons[1].collidepoint(mouse):
                    aiGame = True 

        # Display chess board
        else:
            # Check for moves or selections
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if reset.collidepoint(event.pos):
                        board.reset(userTurn)
                    mouse = pygame.mouse.get_pos()
                    board.move_piece(mouse)
                    # Check for ending conditions
                    checkmate, stalemate = board.check_game_over()
                    board.draw_board()
                    if checkmate:
                        game_over(True)
                    if stalemate:
                        game_over(False)

            # Draw board
            DISPLAY.fill(BLACK)
            draw_text(NUMBERWIDTHS, NUMBERHEIGHTS, BOARDNUMBERS, NUMBERFONTS, LIGHTGREY)
            draw_text(BOARDWIDTHS, BOARDHEIGHTS, BOARDLETTERS, NUMBERFONTS, LIGHTGREY)
            reset = draw_buttons([WIDTH / 2 - 30], [HEIGHT - 40], 60, 30, ["Reset"], LIGHTGREY, BLACK)[0]
            board.draw_board()

        pygame.display.update()


if __name__ == "__main__":
    main()