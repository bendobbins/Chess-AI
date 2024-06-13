import sys
from pygame.constants import QUIT
from processes import *
from board import *
from helper import draw_text, select_square, get_box_placement, draw_buttons, start_page

pygame.init()


class Game:
    """
    Creates chess board with pieces and handles piece movement as well as win conditions.
    """
    
    def __init__(self, userTurn):
        self.selected = None
        self.boardObj = Board()
        self.board = self.boardObj.board
        self.userTurn = userTurn
        self.whiteTurn = True




    def change_turn(self):
        """
        Change user turn and white turn.
        """
        # if self.userTurn:
        #     self.userTurn = False
        # else:
        #     self.userTurn = True
        self.whiteTurn = not self.whiteTurn




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




    def change_selected(self, moveSpace):
        """
        Change highlighting if moveSpace cannot be a valid move for the player.
        """
        if self.whiteTurn:
            # Remove highlighting if click is outside grid, player tries to move piece for other color, or they click the same piece they have selected
            if (not moveSpace or 
                (self.board[self.selected[0]][self.selected[1]] in range(21, 41) and self.board[moveSpace[0]][moveSpace[1]] == 0) or 
                self.board[self.selected[0]][self.selected[1]] == self.board[moveSpace[0]][moveSpace[1]]):
                self.selected = None
                return True
            # If player clicks same color piece as they have already selected, change highlighting to new piece
            if (self.board[moveSpace[0]][moveSpace[1]] in range(1, 21) or 
                (self.board[self.selected[0]][self.selected[1]] in range(21, 41) and self.board[moveSpace[0]][moveSpace[1]] in range(21, 41))):
                self.selected = moveSpace
                return True

        else:
            # Same as for white, but for black
            if (not moveSpace or 
                (self.board[self.selected[0]][self.selected[1]] in range(1, 21) and self.board[moveSpace[0]][moveSpace[1]] == 0) or
                self.board[self.selected[0]][self.selected[1]] == self.board[moveSpace[0]][moveSpace[1]]):
                self.selected = None
                return True
            if (self.board[moveSpace[0]][moveSpace[1]] in range(21, 41) or 
                (self.board[self.selected[0]][self.selected[1]] in range(1, 21) and self.board[moveSpace[0]][moveSpace[1]] in range(1, 21))):
                self.selected = moveSpace
                return True
        
        return False






    def move_piece(self, mouse):
        """
        Given the position of a mouse click, select the square that was clicked on if self.selected is None, otherwise
        move the piece on the selected square to the clicked on square, if the move is valid.
        """
        if self.userTurn:
            if self.selected:
                # Clicked on square becomes moveSpace if a square is already selected
                moveSpace = select_square(mouse)

                # Only allow piece movement for the color whose turn it is and handle highlighting selected piece
                if self.change_selected(moveSpace):
                    return

                # Attempt to move piece to clicked on square
                moved = self.boardObj.move_piece(self.selected, moveSpace)

                if moved:
                    # Change turn if move was successful
                    self.change_turn()
                    print(self.boardObj.log)
                    self.selected = None
                    return

                # Highlight clicked on piece if it is not a possible move       #
                if moved is None:
                    self.selected = None
                self.selected = moveSpace                                       # Handle highlighting of pieces
                return                                                          #

            # If there is no square already selected
            else:
                # Only select a square if there is a piece on it
                selectedSquare = select_square(mouse)
                if selectedSquare:
                    if self.board[selectedSquare[0]][selectedSquare[1]]:
                        self.selected = selectedSquare
    


    def check_game_over(self):
        """
        Check if game ending conditions have been met (checkmate/stalemate).
        Return bools for each conditions.
        """
        originalSelected = self.selected
        
        if self.whiteTurn:
            # end = engine.checkmate(cboard, False, cmove(*[2, 21]), FIFTYMOVECOUNTER, ccounter(*moveCount), crepetitions, len(REPETITION))
            end = checkmate_draw(self.boardObj, False, range(2, 21))
        else:
            # end = engine.checkmate(cboard, True, cmove(*[22, 41]), FIFTYMOVECOUNTER, ccounter(*moveCount), crepetitions, len(REPETITION))
            end = checkmate_draw(self.boardObj, True, range(22, 41))

        mate = True if end[0] else False
        draw = True if end[1] else False

        # engine.free_array(end)

        self.selected = originalSelected
        return mate, draw



    def reset(self, userTurn):
        """
        Reset board and globals keeping track of moves.
        """
        self.__init__(userTurn)
        # self.selected = None
        # self.boardObj = Board()
        # self.board = self.boardObj.board
        # self.userTurn = userTurn
        # self.whiteTurn = True





def main():
    """
    Main function for controlling the chess board and pieces.
    """
    pygame.display.set_caption("Chess")
    userTurn = True
    game = Game(userTurn)
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
                        game.reset(userTurn)
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
            if game.userTurn:
                # Check for moves or selections
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if reset.collidepoint(event.pos):
                            game.reset(userTurn)
                        mouse = pygame.mouse.get_pos()
                        game.move_piece(mouse)
            else:
                game.ai_move_piece()
                game.draw_board()

            # Check for ending conditions
            checkmate, stalemate = game.check_game_over()
            game.draw_board()
            if checkmate:
                game_over(True)
            if stalemate:
                game_over(False)

            # Draw board
            DISPLAY.fill(BLACK)
            draw_text(NUMBERWIDTHS, NUMBERHEIGHTS, BOARDNUMBERS, NUMBERFONTS, LIGHTGREY)
            draw_text(BOARDWIDTHS, BOARDHEIGHTS, BOARDLETTERS, NUMBERFONTS, LIGHTGREY)
            reset = draw_buttons([WIDTH / 2 - 30], [HEIGHT - 40], 60, 30, ["Reset"], LIGHTGREY, BLACK)[0]
            game.draw_board()

        pygame.display.update()


if __name__ == "__main__":
    main()