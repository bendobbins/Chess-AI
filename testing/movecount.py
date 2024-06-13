import sys
import copy
sys.path.append("..")
sys.path.append("../board")
from board import board, processes, moves

DEPTH = 4

castles = 0
promotions = 0
enpassants = 0

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
P5 = [
    [27, 29, 0, 0, 0, 0, 9, 7],
    [25, 30, 0, 0, 0, 0, 10, 5],
    [23, 0, 31, 0, 4, 0, 11, 3],
    [22, 12, 0, 0, 0, 0, 0, 2],
    [0, 24, 0, 0, 0, 0, 6, 1],
    [21, 34, 0, 0, 0, 0, 26, 0],
    [0, 35, 0, 0, 0, 0, 15, 0],
    [28, 36, 0, 0, 0, 0, 16, 8]
]
P4 = [
    [27, 10, 0, 25, 4, 22, 9, 7],
    [0, 30, 24, 11, 3, 0, 29, 0],
    [0, 31, 0, 0, 13, 0, 0, 0],
    [0, 32, 0, 0, 0, 0, 12, 2],
    [21, 0, 0, 0, 14, 0, 0, 0],
    [0, 34, 26, 0, 0, 6, 0, 8],
    [0, 35, 23, 0, 0, 0, 15, 1],
    [28, 36, 5, 0, 0, 0, 16, 0]
]

movesperpos = {}


def move_count(depth, boardObj):
    global castles, promotions, enpassants
    board = boardObj.board
    if depth == 0:
        return 1
    
    for i in range(8):
        for j in range(8):
            if (boardObj.whiteTurn and board[i][j] in range(1, 21)) or (not boardObj.whiteTurn and board[i][j] in range(21, 41)):
                mvs, cmvs, epmv = boardObj.get_moves((i, j))

                for move in mvs:
                    # Make move
                    movePiece = board[move[0]][move[1]]
                    board[move[0]][move[1]] = board[i][j]
                    board[i][j] = 0

                    # Find attacked spaces by other color after move
                    attacked = boardObj.attacked_spaces(False)

                    # Check if king is in check, recurse if not
                    check = False
                    for space in attacked:
                        if (board[space[0]][space[1]] == 1 and boardObj.whiteTurn) or (board[space[0]][space[1]] == 21 and not boardObj.whiteTurn):
                            check = True
                            break

                    if not check:
                        # Check if move is pawn to last rank
                        if processes.check_pawn_upgrade_helper(white, board, move):
                            pawn = board[move[0]][move[1]]
                            pieces = range(17, 21) if white else range(37, 41)
                            for piece in pieces:
                                promotions += 1
                                board[move[0]][move[1]] = piece
                                mc = move_count(depth - 1, board, not white, [(i, j), move])
                                move_counter += mc

                                if depth == DEPTH:
                                    movesperpos[move_to_str((i, j), move) + strmaps[piece]] = mc
                            # Replace upgraded pawn with original pawn so that undoing the move works properly
                            board[move[0]][move[1]] = pawn
                        # If move is normal
                        else:
                            mc = move_count(depth - 1, board, not white, [(i, j), move])
                            if depth == DEPTH:
                                movesperpos[move_to_str((i, j), move)] = mc
                            move_counter += mc

                    # Undo move
                    board[i][j] = board[move[0]][move[1]]
                    board[move[0]][move[1]] = movePiece


                for move in cmvs:
                    castles += 1
                    newBoard = copy.deepcopy(board)
                    # White castle kingside
                    if move == (6, 7):
                        processes.make_castle_move([(6, 7), (5, 7), (4, 7), (7, 7)], [1, 8], newBoard, False)
                    # White castle queenside
                    elif move == (2, 7):
                        processes.make_castle_move([(2, 7), (3, 7), (4, 7), (0, 7)], [1, 7], newBoard, False)
                    # Black castle kingside
                    elif move == (6, 0):
                        processes.make_castle_move([(6, 0), (5, 0), (4, 0), (7, 0)], [21, 28], newBoard, False)
                    # Black castle kingside
                    else:
                        processes.make_castle_move([(2, 0), (3, 0), (4, 0), (0, 0)], [21, 27], newBoard, False)

                    mc = move_count(depth - 1, newBoard, not white, [(i, j), move])
                    if depth == DEPTH:
                        movesperpos[move_to_str((i, j), move)] = mc
                    move_counter += mc


                if epmv:
                    movePiece = board[lastMove[1][0]][lastMove[1][1]]
                    board[epmv[0]][epmv[1]] = board[i][j]
                    board[i][j] = 0
                    board[lastMove[1][0]][lastMove[1][1]] = 0

                    attacked = moves.attacked_spaces(board, not white, False)

                    check = False
                    for space in attacked:
                        if (board[space[0]][space[1]] == 1 and white) or (board[space[0]][space[1]] == 21 and not white):
                            check = True
                            break
                    
                    if not check:
                        enpassants += 1
                        mc = move_count(depth - 1, board, not white, [(i, j), epmv])
                        if depth == DEPTH:
                            movesperpos[move_to_str((i, j), epmv)] = mc
                        move_counter += mc

                    board[i][j] = board[epmv[0]][epmv[1]]
                    board[epmv[0]][epmv[1]] = 0
                    board[lastMove[1][0]][lastMove[1][1]] = movePiece

    return move_counter



def main():
    amt_moves = move_count(DEPTH, P5, True)
    print(amt_moves)
    print(castles, promotions, enpassants)
    print(movesperpos)


if __name__ == "__main__":
    main()