#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "moves.h"


// Function has same logic as castle_valid implemented in processes.py, where a function description can be found
bool castle(bool white, int space[2], int moveSpace[2], int board[8][8], int moveCounts[40]) {
    bool queen;
    bool whiteAttacking;
    // Spaces that must be checked for attacks in each castle situation
    int kspacesw[3][2] = {{6, 7}, {5, 7}, {4, 7}};
    int qspacesw[4][2] = {{2, 7}, {3, 7}, {4, 7}, {0, 7}};
    int kspacesb[3][2] = {{6, 0}, {5, 0}, {4, 0}};
    int qspacesb[4][2] = {{2, 0}, {3, 0}, {4, 0}, {0, 0}};
    int i, j;
    // Allocate memory for passing info to castle_valid
    int* pieces = malloc(sizeof(int) * 2);
    if (!pieces) {
        printf("Memory allocation error\n"); 
        exit(1);
    }
    int* counts = malloc(sizeof(int) * 2);
    if (!counts) {
        printf("Memory allocation error\n"); 
        exit(1);
    }
    int** spaces = malloc(sizeof(int*) * 4);
    if (!spaces) {
        printf("Memory allocation error\n");
        exit(1);
    }
    for (i = 0; i < 4; i++) {
        spaces[i] = malloc(sizeof(int) * 2);
        if (!spaces[i]) {
            printf("Memory allocation error\n");
            exit(1);
        }
    }

    if (white) {
        whiteAttacking = false;
        // If king is selected
        if (board[space[0]][space[1]] == 1) {
            // If kingside white
            if (moveSpace[0] == 6 && moveSpace[1] == 7) {
                // If piece in corner is rook
                if (board[7][7] == 8) {
                    for (i = 0; i < 3; i++) {
                        for (j = 0; j < 2; j++) {
                            spaces[i][j] = kspacesw[i][j];
                        }
                    }
                    pieces[0] = 1;
                    pieces[1] = 8;
                    counts[0] = moveCounts[0];
                    counts[1] = moveCounts[7];
                    queen = false;
                    return castle_valid(spaces, board, pieces, queen, whiteAttacking, counts);
                }
            }

            // If queenside white
            else if (moveSpace[0] == 2 && moveSpace[1] == 7) {
                if (board[0][7] == 7) {
                    for (i = 0; i < 4; i++) {
                        for (j = 0; j < 2; j++) {
                            spaces[i][j] = qspacesw[i][j];
                        }
                    }
                    pieces[0] = 1;
                    pieces[1] = 7;
                    counts[0] = moveCounts[0];
                    counts[1] = moveCounts[6];
                    queen = true;
                    return castle_valid(spaces, board, pieces, queen, whiteAttacking, counts);
                }
            }
        }
    }

    else {
        whiteAttacking = true;
        if (board[space[0]][space[1]] == 21) {
            // If kingside black
            if (moveSpace[0] == 6 && moveSpace[1] == 0) {
                if (board[7][0] == 28) {
                    for (i = 0; i < 3; i++) {
                        for (j = 0; j < 2; j++) {
                            spaces[i][j] = kspacesb[i][j];
                        }
                    }
                    pieces[0] = 21;
                    pieces[1] = 28;
                    counts[0] = moveCounts[20];
                    counts[1] = moveCounts[27];
                    queen = false;
                    return castle_valid(spaces, board, pieces, queen, whiteAttacking, counts);
                }
            }

            // If queenside black
            else if (moveSpace[0] == 2 && moveSpace[1] == 0) {
                if (board[0][0] == 27) {
                    for (i = 0; i < 4; i++) {
                        for (j = 0; j < 2; j++) {
                            spaces[i][j] = qspacesb[i][j];
                        }
                    }
                    pieces[0] = 21;
                    pieces[1] = 27;
                    counts[0] = moveCounts[20];
                    counts[1] = moveCounts[26];
                    queen = true;
                    return castle_valid(spaces, board, pieces, queen, whiteAttacking, counts);
                }
            }
        }
    }

    free(pieces);
    free(counts);
    for (i = 0; i < 4; i++) {
        free(spaces[i]);
    }
    free(spaces);

    return false;
}


bool castle_valid(int** spaces, int board[8][8], int pieces[2], bool queen, bool whiteAttacking, int moveCounts[2]) {
    int i;
    // If king and rook have not moved
    if (moveCounts[0] == 0 && moveCounts[1] == 0) {
        // If kingside
        if (!queen) {
            // If spaces between king and rook are empty
            if (board[spaces[0][0]][spaces[0][1]] == 0 && board[spaces[1][0]][spaces[1][1]] == 0) {
                // Check if king or spaces king moves through are attacked
                int* attacked = attacked_spaces(board, whiteAttacking, false);
                bool valid = true;
                for (i = 1; i < attacked[0] + 1; i++) {
                    if (attacked[i] == BOARDSPACES[spaces[0][0]][spaces[0][1]] ||
                        attacked[i] == BOARDSPACES[spaces[1][0]][spaces[1][1]] ||
                        attacked[i] == BOARDSPACES[spaces[2][0]][spaces[2][1]]) {
                            valid = false;
                        }
                }
                free(attacked);
                // If king is not moving through check, castle is valid
                if (valid) {
                    return true;
                }
            }
        }

        else {
            // Same for queenside
            if (board[spaces[0][0]][spaces[0][1]] == 0 && board[spaces[1][0]][spaces[1][1]] == 0
                && board[spaces[2][0]][spaces[2][1]]) {
                int* attacked = attacked_spaces(board, whiteAttacking, false);
                bool valid = true;
                for (i = 1; i < attacked[0] + 1; i++) {
                    if (attacked[i] == BOARDSPACES[spaces[3][0]][spaces[3][1]] ||
                        attacked[i] == BOARDSPACES[spaces[2][0]][spaces[2][1]] ||
                        attacked[i] == BOARDSPACES[spaces[1][0]][spaces[1][1]]) {
                            valid = false;
                        }
                }
                free(attacked);
                if (valid) {
                    return true;
                }
            }
        }
    }

    return false;
}


bool en_passant(bool white, int lastMove[2][2], int board[8][8], int space[2], int moveSpace[2]) {
    // If the last move was made by a pawn
    if ((board[lastMove[1][0]][lastMove[1][1]] >= 9 && board[lastMove[1][0]][lastMove[1][1]] < 17) ||
        (board[lastMove[1][0]][lastMove[1][1]] >= 29 && board[lastMove[1][0]][lastMove[1][1]] < 37)) {

        // Spaces to the right and left of the last pawn to move
        int rightSpace[2] = {lastMove[1][0] + 1, lastMove[1][1]};
        int leftSpace[2] = {lastMove[1][0] - 1, lastMove[1][1]};
        int behindSpace[2], checkDoubleMove, pawnRange[2], kingSpot[2], i, j;

        if (white) {
            checkDoubleMove = lastMove[1][1] - lastMove[0][1];
            behindSpace[0] = lastMove[1][0];
            behindSpace[1] = lastMove[1][1] - 1;
            pawnRange[0] = 9;
            pawnRange[1] = 17;
        } else {
            checkDoubleMove = lastMove[0][1] - lastMove[1][1];
            behindSpace[0] = lastMove[1][0];
            behindSpace[1] = lastMove[1][1] + 1;
            pawnRange[0] = 29;
            pawnRange[1] = 37;
        }
        for (i = 0; i < 8; i++) {
            for (j = 0; j < 8; j++) {
                if ((board[i][j] == 1 && white) || (board[i][j] == 21 && !white)) {
                    kingSpot[0] = i;
                    kingSpot[1] = j;
                }
            }
        }

        // If the last move was 2 spaces forward
        if (checkDoubleMove == 2) {
            // If the piece attempting en passant is to the left or right of the opposing pawn and the piece is a pawn
            if (((space[0] == rightSpace[0] && space[1] == rightSpace[1]) || (space[0] == leftSpace[0] && space[1] == leftSpace[1])) &&
            (board[space[0]][space[1]] >= pawnRange[0] && board[space[0]][space[1]] < pawnRange[1])) {
                // If the piece is trying to move behind the pawn, the move is valid
                if (behindSpace[0] == moveSpace[0] && behindSpace[1] == moveSpace[1]) {
                    board[moveSpace[0]][moveSpace[1]] = board[space[0]][space[1]];
                    board[space[0]][space[1]] = 0;
                    board[lastMove[1][0]][lastMove[1][1]] = 0;
                    int* attacked = attacked_spaces(board, !white, false);
                    for (int i = 1; i < attacked[0] + 1; i++) {
                        if (attacked[i] == BOARDSPACES[kingSpot[0]][kingSpot[1]]) {
                            return false;
                        }
                    }
                    return true;
                }
            }
        }
    }

    return false;
}


bool check_pawn_upgrade(bool white, int board[8][8], int space[2], int moveCol) {
    if (white) {
        if (board[space[0]][space[1]] >= 9 && board[space[0]][space[1]] < 17) {
            if (moveCol == 0) {
                return true;
            }
        }
    }

    else {
        if (board[space[0]][space[1]] >= 29 && board[space[0]][space[1]] < 37) {
            if (moveCol == 7) {
                return true;
            }
        }
    }

    return false;
}    