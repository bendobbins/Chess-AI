#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include "moves.h"

/* NOTE
Almost all of the functions implemented in this file use the same parameters, return types and logic used in the python implementation 
of moves (Chess/board/moves.py). Therefore, function descriptions will not be included in this file, only comments that apply to
specific C-related logic. To learn what each function does and what the parameters represent, take a look at moves.py.
*/

int* get_moves(int board[8][8], int selected[2], int moveCount) {
    if ((board[selected[0]][selected[1]] >= 9 && board[selected[0]][selected[1]] < 17) || 
        (board[selected[0]][selected[1]] >= 29 && board[selected[0]][selected[1]] < 37)) {
        return valid_pawn_moves(selected, board, board[selected[0]][selected[1]], moveCount);
    }
    else if ((board[selected[0]][selected[1]] >= 5 && board[selected[0]][selected[1]] < 7) || 
        (board[selected[0]][selected[1]] >= 25 && board[selected[0]][selected[1]] < 27) ||
        board[selected[0]][selected[1]] == 19 || board[selected[0]][selected[1]] == 39) {
            return valid_knight_moves(selected, board, board[selected[0]][selected[1]], false);
        }
    else if ((board[selected[0]][selected[1]] >= 3 && board[selected[0]][selected[1]] < 5) || 
        (board[selected[0]][selected[1]] >= 23 && board[selected[0]][selected[1]] < 25) ||
        board[selected[0]][selected[1]] == 18 || board[selected[0]][selected[1]] == 38) {
            return valid_bishop_moves(selected, board, board[selected[0]][selected[1]], false);
        }
    else if ((board[selected[0]][selected[1]] >= 7 && board[selected[0]][selected[1]] < 9) || 
        (board[selected[0]][selected[1]] >= 27 && board[selected[0]][selected[1]] < 29) ||
        board[selected[0]][selected[1]] == 20 || board[selected[0]][selected[1]] == 40) {
            return valid_rook_moves(selected, board, board[selected[0]][selected[1]], false);
        }
    else if (board[selected[0]][selected[1]] == 2 || board[selected[0]][selected[1]] == 22 || 
        board[selected[0]][selected[1]] == 17 || board[selected[0]][selected[1]] == 37) {
            return valid_queen_moves(selected, board, board[selected[0]][selected[1]], false);
        }
    else {
        return valid_king_moves(selected, board, board[selected[0]][selected[1]], true);
    }
}


int* valid_pawn_moves(int start[2], int board[8][8], int piece, int moveCounter) {
    int counter = 0;
    int move = 0;
    // Pawn has 4 maximum possible moves, add 1 for counter
    int* moves = malloc(sizeof(int) * 5);
    if (!moves) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    // Keep track of amount of possible moves
    moves[0] = counter;
    
    // Black
    if (piece >= 21 && piece <= 40) {
        // Check attack moves
        if (start[0] != 7) {
            int space[2] = {start[0] + 1, start[1] + 1};
            move = check_pawn_move(board, space, false); 
            counter = add_move(moves, counter, move);
        }
        if (start[0] != 0) {
            int space[2] = {start[0] - 1, start[1] + 1};
            move = check_pawn_move(board, space, false);
            counter = add_move(moves, counter, move);
        }
    
        // Check regular moves
        if (!board[start[0]][start[1] + 1]) {
            if (!moveCounter) {
                if (!board[start[0]][start[1] + 2]) {
                    counter = add_move(moves, counter, BOARDSPACES[start[0]][start[1] + 2]);
                }
            }
            counter = add_move(moves, counter, BOARDSPACES[start[0]][start[1] + 1]);
        }
    }

    // White
    else {
        if (start[0] != 7) {
            int space[2] = {start[0] + 1, start[1] - 1};
            move = check_pawn_move(board, space, true); 
            counter = add_move(moves, counter, move);
        }
        if (start[0] != 0) {
            int space[2] = {start[0] - 1, start[1] - 1};
            move = check_pawn_move(board, space, true);
            counter = add_move(moves, counter, move);
        }
        if (!board[start[0]][start[1] - 1]) {
            if (!moveCounter) {
                if (!board[start[0]][start[1] - 2]) {
                    counter = add_move(moves, counter, BOARDSPACES[start[0]][start[1] - 2]);
                }
            }
            counter = add_move(moves, counter, BOARDSPACES[start[0]][start[1] - 1]);
        }
    }

    return moves;
}


int* valid_knight_moves(int start[2], int board[8][8], int piece, bool checkProtected) {
    int counter = 0;
    int move = 0;
    // Knight has 8 maximum possible moves, add 1 for counter
    int* moves = malloc(sizeof(int) * 9);
    if (!moves) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    // Keep track of amount of possible moves
    moves[0] = counter;

    int possibleMoves[8][2] = {
        {start[0] - 1, start[1] + 2},
        {start[0] + 1, start[1] + 2},
        {start[0] + 1, start[1] - 2},
        {start[0] - 1, start[1] - 2},
        {start[0] + 2, start[1] + 1},
        {start[0] - 2, start[1] + 1},
        {start[0] - 2, start[1] - 1},
        {start[0] + 2, start[1] - 1}
    };

    for (int i = 0; i < 8; i++) {
        if (piece >= 21 && piece <= 40) {
            move = check_knight_move(board, possibleMoves[i], false, checkProtected);
        }
        else {
            move = check_knight_move(board, possibleMoves[i], true, checkProtected);
        }
        counter = add_move(moves, counter, move);
    }

    return moves;
}


int* valid_bishop_moves(int start[2], int board[8][8], int piece, bool checkProtected) {
    int counter = 0;
    // Bishop has maximum of 13 possible moves, add 1 for counter
    int* moves = malloc(sizeof(int) * 14);
    if (!moves) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    moves[0] = counter;

    // Directions that a bishop can move
    bool directions[4][2] = {
        {false, true},      // NE
        {false, false},     // NW
        {true, true},       // SE
        {true, false}       // SW
    };

    int i, j;
    for (i = 0; i < 4; i++) {
        for (j = 1; j < 9; j++) {
            int space[2] = {add_or_subtract(start[0], j, directions[i][0]), add_or_subtract(start[1], j, directions[i][1])};

            if (space[0] < 0 || space[1] < 0 || space[0] > 7 || space[1] > 7) {
                break;
            }

            if (!checkProtected) {
                // Only add spaces that are empty or occupied by enemies
                if (piece >= 21 && piece <= 40) {
                    if (board[space[0]][space[1]] >= 21 && board[space[0]][space[1]] <= 40) {
                        break;
                    }
                    else if (board[space[0]][space[1]] >= 1 && board[space[0]][space[1]] <= 20) {
                        counter = add_move(moves, counter, BOARDSPACES[space[0]][space[1]]);
                        // Break so that spaces behind occupied spaces are not checked
                        break;
                    }
                }
                else {
                    if (board[space[0]][space[1]] >= 1 && board[space[0]][space[1]] <= 20) {
                        break;
                    }
                    else if (board[space[0]][space[1]] >= 21 && board[space[0]][space[1]] <= 40) {
                        counter = add_move(moves, counter, BOARDSPACES[space[0]][space[1]]);
                        break;
                    }
                }
            }

            // Add all spaces, break if space is occupied
            else {
                if (board[space[0]][space[1]] >= 1 && board[space[0]][space[1]] <= 40) {
                    counter = add_move(moves, counter, BOARDSPACES[space[0]][space[1]]);
                    break;
                }
            }

            if (board[space[0]][space[1]] == 0) {
                counter = add_move(moves, counter, BOARDSPACES[space[0]][space[1]]);
            }
        }
    }

    return moves;
}



int* valid_rook_moves(int start[2], int board[8][8], int piece, bool checkProtected) {
    int counter = 0;
    // Rook has 14 maximum possible moves, add 1 for counter
    int* moves = malloc(sizeof(int) * 15);
    if (!moves) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    moves[0] = counter;
    
    // [x][0] represents whether column or row is changing, [x][1] represents direction
    bool directions[4][2] = {
        {false, true},      // Row changes positively, direction is E
        {false, false},     // Row changes negatively, direction is W
        {true, true},       // Column changes positively, direction is N
        {true, false}       // Column changes negatively, direction is S
    };

    int i, j;
    for (i = 0; i < 4; i++) {
        for (j = 1; j < 9; j++) {
            int space[2] = {add_or_subtract(start[0], j, directions[i][1]), start[1]};
            if (directions[i][0]) {
                space[0] = start[0];
                space[1] = add_or_subtract(start[1], j, directions[i][1]);
            }

            if (space[0] < 0 || space[1] < 0 || space[0] > 7 || space[1] > 7) {
                break;
            }

            // Basically same as bishop
            if (!checkProtected) {
                if (piece >= 21 && piece <= 40) {
                    if (board[space[0]][space[1]] >= 21 && board[space[0]][space[1]] <= 40) {
                        break;
                    }
                    else if (board[space[0]][space[1]] >= 1 && board[space[0]][space[1]] <= 20) {
                        counter = add_move(moves, counter, BOARDSPACES[space[0]][space[1]]);
                        break;
                    }
                }
                else {
                    if (board[space[0]][space[1]] >= 1 && board[space[0]][space[1]] <= 20) {
                        break;
                    }
                    else if (board[space[0]][space[1]] >= 21 && board[space[0]][space[1]] <= 40) {
                        counter = add_move(moves, counter, BOARDSPACES[space[0]][space[1]]);
                        break;
                    }
                }
            }
            else {
                if (board[space[0]][space[1]] >= 1 && board[space[0]][space[1]] <= 40) {
                    counter = add_move(moves, counter, BOARDSPACES[space[0]][space[1]]);
                    break;
                }
            }
            if (board[space[0]][space[1]] == 0) {
                counter = add_move(moves, counter, BOARDSPACES[space[0]][space[1]]);
            }
        }
    }

    return moves;
}



int* valid_queen_moves(int start[2], int board[8][8], int piece, bool checkProtected) {
    int counter = 1;

    // Queen moves is just a combination of rook and bishop
    int* rookMoves = valid_rook_moves(start, board, piece, checkProtected);
    int* bishopMoves = valid_bishop_moves(start, board, piece, checkProtected);

    // Allocate memory for amount of possible rook moves + amount of possible bishop moves + 1 for counter
    int* moves = malloc(sizeof(int) * (rookMoves[0] + bishopMoves[0] + 1));
    if (!moves) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    // Amount of possible moves
    moves[0] = rookMoves[0] + bishopMoves[0];

    // Add rook and bishop moves
    for (; counter < rookMoves[0] + 1; counter++) {
        moves[counter] = rookMoves[counter];
    }

    for (int counter2 = 1; counter2 < bishopMoves[0] + 1; counter2++) {
        moves[counter] = bishopMoves[counter2];
        counter++;
    }

    free(rookMoves);
    free(bishopMoves);

    return moves;
}



int* valid_king_moves(int start[2], int board[8][8], int piece, bool checkProtected) {
    int counter = 0;

    // Keep track of spaces that are in check or occupied by a friendly
    bool invalidMoves[64];
    for (int i = 0; i < 64; i++) {
        invalidMoves[i] = false;
    }

    int* attacked;

    // All spaces attacked by opposite color are invalid
    if (piece == 21) {
        attacked = attacked_spaces(board, true, checkProtected);
        for (int i = 1; i < attacked[0] + 1; i++) {
            invalidMoves[attacked[i] - 1] = true;
        }
    }
    else {
        attacked = attacked_spaces(board, false, checkProtected);
        for (int i = 1; i < attacked[0] + 1; i++) {
            invalidMoves[attacked[i] - 1] = true;
        }
    }

    free(attacked);

    // All possible moves for a king
    int possibleMoves[8][2] = {
        {start[0], start[1] + 1},
        {start[0], start[1] - 1},
        {start[0] - 1, start[1]},
        {start[0] + 1, start[1]},
        {start[0] + 1, start[1] + 1},
        {start[0] + 1, start[1] - 1},
        {start[0] - 1, start[1] + 1},
        {start[0] - 1, start[1] - 1}
    };

    // Spaces outside the board or occupied by friendlies are invalid
    for (int i = 0; i < 8; i++) {
        if (possibleMoves[i][0] < 0 || possibleMoves[i][1] < 0 || 
            possibleMoves[i][0] > 7 || possibleMoves[i][1] > 7) {
                continue;
        }

        if (piece == 21) {
            if (board[possibleMoves[i][0]][possibleMoves[i][1]] >= 22 &&
                board[possibleMoves[i][0]][possibleMoves[i][1]] <= 40) {
                    invalidMoves[BOARDSPACES[possibleMoves[i][0]][possibleMoves[i][1]] - 1] = true;
            }
        }
        else {
            if (board[possibleMoves[i][0]][possibleMoves[i][1]] >= 2 &&
                board[possibleMoves[i][0]][possibleMoves[i][1]] <= 20) {
                    invalidMoves[BOARDSPACES[possibleMoves[i][0]][possibleMoves[i][1]] - 1] = true;
            }
        }
    }

    // King has max 8 possible moves, add 1 for counter
    int* moves = malloc(sizeof(int) * 9);
    if (!moves) {
        printf("Memory allocation error\n");
        exit(1);
    }

    // Only add valid moves, keep track of amount
    int moveCount = 0;
    for (int i = 0; i < 8; i++) {
        bool invalid = false;
        // If move is out of board or otherwise invalid, don't add to moves
        if ((possibleMoves[i][0] < 0 || possibleMoves[i][1] < 0 || 
            possibleMoves[i][0] > 7 || possibleMoves[i][1] > 7) || 
            invalidMoves[BOARDSPACES[possibleMoves[i][0]][possibleMoves[i][1]] - 1]) {
            invalid = true;
        }
        if (!invalid) {
            moveCount++;
            moves[moveCount] = BOARDSPACES[possibleMoves[i][0]][possibleMoves[i][1]];
        }
    }
    moves[0] = moveCount;

    return moves;
}



int* attacked_spaces(int board[8][8], bool white, bool checkProtected) {
    int counter = 0;

    // Keep track of attacked spaces that have already been added to array
    bool* counted = calloc(64, sizeof(bool));
    if (!counted) {
        printf("Memory allocation error\n");
        exit(1);
    }
    int i, j;
    for (i = 0; i < 64; i++) {
        counted[i] = false;
    }

    // If every square is attacked, max will be 64
    int* attacked = malloc(sizeof(int) * 65);
    if (!attacked) {
        printf("Memory allocation error\n");
        exit(1);
    }

    for (i = 0; i < 8; i++) {
        for (j = 0; j < 8; j++) {

            // Go through every space on the board
            int space[2] = {i, j};

            // Only get attacked spaces for opposite color
            if (white) {
                if (board[i][j] >= 9 && board[i][j] < 17) {
                    // For pawns, only consider squares they can attack
                    counter = pawn_helper(attacked, counter, counted, space, true);
                }
                // Get valid moves for pieces, add all to attacked if not already added
                else if ((board[i][j] >= 7 && board[i][j] < 9) || board[i][j] == 20) {
                    int* rookAttacked = valid_rook_moves(space, board, board[i][j], checkProtected);
                    counter = attacked_helper(attacked, rookAttacked, counter, counted);
                }
                else if ((board[i][j] >= 5 && board[i][j] < 7) || board[i][j] == 19) {
                    int* knightAttacked = valid_knight_moves(space, board, board[i][j], checkProtected);
                    counter = attacked_helper(attacked, knightAttacked, counter, counted);
                }
                else if ((board[i][j] >= 3 && board[i][j] < 5) || board[i][j] == 18) {
                    int* bishopAttacked = valid_bishop_moves(space, board, board[i][j], checkProtected);
                    counter = attacked_helper(attacked, bishopAttacked, counter, counted);
                }
                else if (board[i][j] == 2 || board[i][j] == 17) {
                    int* queenAttacked = valid_queen_moves(space, board, board[i][j], checkProtected);
                    counter = attacked_helper(attacked, queenAttacked, counter, counted);
                }
                else if (board[i][j] == 1) {
                    counter = king_helper(space, attacked, counter, counted);
                }
            }

            // Same as above
            else {
                if (board[i][j] >= 29 && board[i][j] < 37) {
                    counter = pawn_helper(attacked, counter, counted, space, false);
                }
                else if ((board[i][j] >= 27 && board[i][j] < 29) || board[i][j] == 40) {
                    int* rookAttacked = valid_rook_moves(space, board, board[i][j], checkProtected);
                    counter = attacked_helper(attacked, rookAttacked, counter, counted);
                }
                else if ((board[i][j] >= 25 && board[i][j] < 27) || board[i][j] == 39) {
                    int* knightAttacked = valid_knight_moves(space, board, board[i][j], checkProtected);
                    counter = attacked_helper(attacked, knightAttacked, counter, counted);
                }
                else if ((board[i][j] >= 23 && board[i][j] < 25) || board[i][j] == 38) {
                    int* bishopAttacked = valid_bishop_moves(space, board, board[i][j], checkProtected);
                    counter = attacked_helper(attacked, bishopAttacked, counter, counted);
                }
                else if (board[i][j] == 22 || board[i][j] == 37) {
                    int* queenAttacked = valid_queen_moves(space, board, board[i][j], checkProtected);
                    counter = attacked_helper(attacked, queenAttacked, counter, counted);
                }
                else if (board[i][j] == 21) {
                    counter = king_helper(space, attacked, counter, counted);
                }
            }
        }
    }

    attacked[0] = counter;
    free(counted);
    return attacked;
}