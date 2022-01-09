#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "moves.h"


int* checkmate(int board[8][8], bool white, int range[2], int fifty, int moveCounter[40], int repetitions[][8][8], int repetitionLength) {
    // One int for draw, one for checkmate
    int* endings = calloc(2, sizeof(int));
    if (!endings) {
        printf("Memory allocation error\n");
        exit(1);
    }

    int* attacked = attacked_spaces(board, white, false);
    int king[2];
    bool kingFound = false;

    // Find the king of the color whose turn it is on the board
    int i, j;
    for (i = 0; i < 8; i++) {
        for (j = 0; j < 8; j++) {
            if ((board[i][j] == 1 && !white) || (board[i][j] == 21 && white)) {
                king[0] = i;
                king[1] = j;
                kingFound = true;
            }
            if (kingFound) {
                break;
            }
        }
        if (kingFound) {
            break;
        }
    }

    // Get valid moves for the king
    int* kingMoves = valid_king_moves(king, board, board[king[0]][king[1]], true);

    // Determine if the king is currently being attacked
    bool kingAttacked = false;
    for (int i = 1; i < attacked[0] + 1; i++) {
        if (attacked[i] == BOARDSPACES[king[0]][king[1]]) {
            kingAttacked = true;
            break;
        }
    }

    // If the king is currently being attacked and has no valid moves, check for checkmate
    bool mate = false;
    if (kingAttacked && !kingMoves[0]) {
        mate = check_checkmate(white, board, range, king, moveCounter);
    }

    // If there is a checkmate, first int in endings becomes 1
    if (mate) {
        endings[0] = 1;
    }
    // If there is not a checkmate, check for a draw
    else {
        bool draw = check_draw(board, range, kingMoves[0], fifty, moveCounter, repetitions, repetitionLength);
        // If there is a draw, second int in endings becomes 1
        if (draw) {
            endings[1] = 1;
        }
    }

    free(kingMoves);
    free(attacked);

    return endings;
}


bool check_checkmate(bool white, int board[8][8], int range[2], int king[2], int moveCounter[40]) {
    int i, j, k;
    // Range is all pieces of color whose turn it is, excluding king
    for (i = range[0]; i < range[1]; i++) {
        for (j = 0; j < 8; j++) {
            for (k = 0; k < 8; k++) {
                // If the piece is found on the board, get the possible moves for that piece
                if (board[j][k] == i) {
                    int space[2] = {j, k};
                    int* moves = get_moves(board, space, moveCounter[board[j][k] - 1]);

                    // Make each possible move on a temporary new board and see if any of them get the king out of check
                    for (int l = 1; l < moves[0] + 1; l++) {
                        // Create board and make move
                        int newboard[8][8];
                        memcpy(newboard, board, sizeof(int) * 8 * 8);
                        newboard[REFERENCES[moves[l] - 1][0]][REFERENCES[moves[l] - 1][1]] = i;
                        newboard[j][k] = 0;

                        // See if king is still attacked
                        int* attacked = attacked_spaces(newboard, white, false);
                        bool notAttacked = true;
                        for (int o = 1; o < attacked[0] + 1; o++) {
                            if (attacked[o] == BOARDSPACES[king[0]][king[1]]) {
                                notAttacked = false;
                                break;
                            }
                        }
                        free(attacked);

                        // If king is not attacked after some move, there is no checkmate, so return false
                        if (notAttacked) {
                            return false;
                        }
                    }
                    free(moves);
                }
            }
        }
    }
    // If all possible moves have been tried for every piece remaining (for the color whose turn it is) and none of them get the king out of check, checkmate
    return true;
}


bool check_draw(int board[8][8], int range[2], int amtKingMoves, int fifty, int moveCounter[40], int repetitions[][8][8], int repetitionLength) {
    // If there have been fifty moves with no pawn movement and no taken pieces, there is a draw
    if (fifty == 100) {
        return true;
    }

    int i, j, k;
    // If the king has no moves, check if any other pieces have moves
    if (!amtKingMoves) {
        bool noMoves = true;
        // Check each piece of the given color besides the king
        for (i = range[0]; i < range[1]; i++) {
            for (j = 0; j < 8; j++) {
                for (k = 0; k < 8; k++) {
                    // If piece is found on the board, get moves and determine if there are any possible for that piece
                    if (board[j][k] == i) {
                        int space[2] = {j, k};
                        int* moves = get_moves(board, space, moveCounter[board[j][k] - 1]);
                        int numMoves = moves[0];
                        free(moves);
                        // If there are moves, then there is no stalemate, so break loop and continue function
                        if (numMoves) {
                            noMoves = false;
                        }
                    }
                    if (!noMoves) {
                        break;
                    }
                }
                if (!noMoves) {
                    break;
                }
            }
            if (!noMoves) {
                break;
            }
        }
        // If there are no moves for the king or any other piece, there is a stalemate
        if (noMoves) {
            return true;
        }
    }

    // Create array of all pieces on the board
    int counter = 0;
    int* pieces = malloc(sizeof(int) * 40);
    if (!pieces) {
        printf("Memory allocation error\n");
        exit(1);
    }
    for (i = 0; i < 8; i++) {
        for (j = 0; j < 8; j++) {
            if (board[i][j]) {
                pieces[counter] = board[i][j];
                counter++;
            }
        }
    }

    // Realloc array for sorting if needed
    int* totalPieces = realloc(pieces, sizeof(int) * counter);
    bool insufficient = false;

    // If only two pieces left, they must be kings so draw
    if (counter == 2) {
        insufficient = true;
    }

    else if (counter == 3 || counter == 4) {
        selection_sort(totalPieces, counter);
        // If 3 pieces left, determine if those pieces classify as insufficient material
        if (counter == 3) {
            for (i = 0; i < 8; i++) {
                if (totalPieces[0] == INSUFFICIENT3[i][0] && totalPieces[1] == INSUFFICIENT3[i][1] &&
                    totalPieces[2] == INSUFFICIENT3[i][2]) {
                    insufficient = true;
                }
            }
        }

        // If 4 pieces left, determine if they classify as insufficient material
        else {
            for (i = 0; i < 42; i++) {
                if (totalPieces[0] == INSUFFICIENT4[i][0] && totalPieces[1] == INSUFFICIENT4[i][1] &&
                    totalPieces[2] == INSUFFICIENT4[i][2] && totalPieces[3] == INSUFFICIENT4[i][3]) {
                    insufficient = true;
                }
            }
        }
    }

    free(totalPieces);
    // If insufficient material, there is a draw
    if (insufficient) {
        return true;
    }

    // If threefold repetition is found, return true
    if (repetition_checker(repetitions, repetitionLength)) {
        return true;
    }

    // If no draw conditions are met, return false
    return false;
}


bool repetition_checker(int repetitions[][8][8], int repetitionLength) {
    int i, j, k, l;
    // To keep track of board states that repeat twice but not three times so that the second repetition is not checked
    bool repeated[repetitionLength];
    for (i = 0; i < repetitionLength; i++) {
        repeated[i] = false;
    }

    for (i = 0; i < repetitionLength; i++) {
        // Iterate through all boards in repetitions unless board is the same as an already checked board
        if (!repeated[i]) {
            // Counter is 1 because board being evaluated counts as a repetition
            int counter = 1;
            for (j = 0; j < repetitionLength; j++) {
                // Check for repetition on all boards except the one being evaluated and ones that have already been checked
                if (i != j && !repeated[j]) {
                    bool same = true;
                    for (k = 0; k < 8; k++) {
                        for (l = 0; l < 8; l++) {
                            // If anything is different about the two boards, break the loop because there is no repetition
                            if (repetitions[i][k][l] != repetitions[j][k][l]) {
                                same = false;
                            }
                            if (!same) {
                                break;
                            }
                        }
                        if (!same) {
                            break;
                        }
                    // If the boards are the same, add to counter
                    }
                    if (same) {
                        counter++;
                        repeated[j] = true;
                    }
                }
                // If there are 3 boards that are the same, there is a threefold repetition, so return true
                if (counter == 3) {
                    return true;
                }
            }
        }
    }

    // If there are no three boards that are the same, return false
    return false;
}


void selection_sort(int* pieces, int size) {
    int i, j, min;
    for (i = 0; i < size - 1; i++) {
        // Set min equal to lowest non-checked index in list
        min = i;
        // Iterate from 1 after lowest non-checked value to end of list
        for (j = i + 1; j < size; j++) {
            // Find the lowest number in the list after checked values
            if (pieces[j] < pieces[min]) {
                // Set index of lowest number = to min
                min = j;
            }
        }
        // Swap values of lowest number index and current index
        swap(&pieces[min], &pieces[i]);
    }
}


void swap(int* x, int* y) {
    // Swap 2 values in an array
    int tmp = *x;
    *x = *y;
    *y = tmp;
}