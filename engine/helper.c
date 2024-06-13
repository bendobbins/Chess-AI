#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include "moves.h"

// Unique integers representing spaces on a chess board
const int BOARDSPACES[8][8] = {
    {1, 2, 3, 4, 5, 6, 7, 8},
    {9, 10, 11, 12, 13, 14, 15, 16},
    {17, 18, 19, 20, 21, 22, 23, 24},
    {25, 26, 27, 28, 29, 30, 31, 32},
    {33, 34, 35, 36, 37, 38, 39, 40},
    {41, 42, 43, 44, 45, 46, 47, 48},
    {49, 50, 51, 52, 53, 54, 55, 56},
    {57, 58, 59, 60, 61, 62, 63, 64}
};

// Row, column values that correspond to boardspaces 
const int REFERENCES[64][2] = {
    {0, 0}, {0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7},
    {1, 0}, {1, 1}, {1, 2}, {1, 3}, {1, 4}, {1, 5}, {1, 6}, {1, 7},
    {2, 0}, {2, 1}, {2, 2}, {2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7},
    {3, 0}, {3, 1}, {3, 2}, {3, 3}, {3, 4}, {3, 5}, {3, 6}, {3, 7},
    {4, 0}, {4, 1}, {4, 2}, {4, 3}, {4, 4}, {4, 5}, {4, 6}, {4, 7},
    {5, 0}, {5, 1}, {5, 2}, {5, 3}, {5, 4}, {5, 5}, {5, 6}, {5, 7},
    {6, 0}, {6, 1}, {6, 2}, {6, 3}, {6, 4}, {6, 5}, {6, 6}, {6, 7},
    {7, 0}, {7, 1}, {7, 2}, {7, 3}, {7, 4}, {7, 5}, {7, 6}, {7, 7}
};

// Values of pieces
const int PIECEVALUES[20] = {
    0, 9, 3, 3, 3, 3, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 9, 3, 3, 5
};

// Insufficient material situations if there are 3 pieces on the board
const int INSUFFICIENT3[12][3] = {
    {1, 3, 21},
    {1, 4, 21},
    {1, 5, 21},
    {1, 6, 21},
    {1, 18, 21},
    {1, 19, 21},
    {1, 21, 23},
    {1, 21, 24},
    {1, 21, 25},
    {1, 21, 26},
    {1, 21, 38},
    {1, 21, 39}
};

// Insufficient material situations if there are 4 pieces on the board
const int INSUFFICIENT4[42][4] = {
    {1, 5, 6, 21},
    {1, 5, 19, 21},
    {1, 6, 19, 21},
    {1, 21, 25, 26},
    {1, 21, 25, 39},
    {1, 21, 26, 39},
    {1, 3, 21, 23},
    {1, 3, 21, 24},
    {1, 3, 21, 25},
    {1, 3, 21, 26},
    {1, 3, 21, 38},
    {1, 3, 21, 39},
    {1, 4, 21, 23},
    {1, 4, 21, 24},
    {1, 4, 21, 25},
    {1, 4, 21, 26},
    {1, 4, 21, 38},
    {1, 4, 21, 39},
    {1, 5, 21, 23},
    {1, 5, 21, 24},
    {1, 5, 21, 25},
    {1, 5, 21, 26},
    {1, 5, 21, 38},
    {1, 5, 21, 39},
    {1, 6, 21, 23},
    {1, 6, 21, 24},
    {1, 6, 21, 25},
    {1, 6, 21, 26},
    {1, 6, 21, 38},
    {1, 6, 21, 39},
    {1, 18, 21, 23},
    {1, 18, 21, 24},
    {1, 18, 21, 25},
    {1, 18, 21, 26},
    {1, 18, 21, 38},
    {1, 18, 21, 39},
    {1, 19, 21, 23},
    {1, 19, 21, 24},
    {1, 19, 21, 25},
    {1, 19, 21, 26},
    {1, 19, 21, 38},
    {1, 19, 21, 39},
};


int check_pawn_move(int board[8][8], int space[2], bool white) {
    // Check if attack space is occupied by the opposite color
    if (white) {
        if (board[space[0]][space[1]] >= 21 && board[space[0]][space[1]] <= 40) {
            return BOARDSPACES[space[0]][space[1]];
        }
    }

    else {
        if (board[space[0]][space[1]] >= 1 && board[space[0]][space[1]] <= 20) {
            return BOARDSPACES[space[0]][space[1]];
        }
    }

    return 0;
}


int check_knight_move(int board[8][8], int space[2], bool white, bool checkProtected) {
    // If space not on board
    if (space[0] < 0 || space[1] < 0 || space[0] > 7 || space[1] > 7) {
        return 0;
    }

    if (!checkProtected) {
        // Only add empty spaces or those occupied by enemies
        if (white) {
            if (board[space[0]][space[1]] == 0 || (board[space[0]][space[1]] >= 21 && board[space[0]][space[1]] <= 40)) {
                return BOARDSPACES[space[0]][space[1]];
            }
        }
        else {
            if (board[space[0]][space[1]] >= 0 && board[space[0]][space[1]] <= 20) {
                return BOARDSPACES[space[0]][space[1]];
            }
        }
    }

    // Add all spaces
    else {
        return BOARDSPACES[space[0]][space[1]];
    }

    return 0;
}


int attacked_helper(int* attacked, int* pieceAttacks, int counter, bool* counted) {
    // Add all valid moves for a piece to attacked if not already in attacked
    for (int i = 1; i < pieceAttacks[0] + 1; i++) {
        if (!counted[pieceAttacks[i] - 1]) {
            counter++;
            attacked[counter] = pieceAttacks[i];
            counted[pieceAttacks[i] - 1] = true; 
        }
    }

    // Free moves for piece
    free(pieceAttacks);
    return counter;
}


int* pawn_attacks(int start[2], bool white) {
    // Spaces that a white pawn attacks
    int attackspaces[2][2] = {{start[0] + 1, start[1] - 1}, {start[0] - 1, start[1] - 1}};

    // For black
    if (!white) {
        attackspaces[0][0] = start[0] + 1;
        attackspaces[0][1] = start[1] + 1;
        attackspaces[1][0] = start[0] - 1;
        attackspaces[1][1] = start[1] + 1;
    }

    // 2 possible moves
    int* moves = calloc(2, sizeof(int));
    if (!moves) {
        printf("Memory allocation error\n");
        exit(1);
    }

    // Add move if in board
    for (int i = 0; i < 2; i++) {
        if (attackspaces[i][0] < 0 || attackspaces[i][1] < 0 || attackspaces[i][0] > 7 || attackspaces[i][1] > 7) {
            continue;
        }
        moves[i] = BOARDSPACES[attackspaces[i][0]][attackspaces[i][1]];
    }

    return moves;
}


int pawn_helper(int* attacked, int counter, bool* counted, int space[2], bool white) {
    // Get attacked spaces for a pawn and add to attacked
    int* pawnAttacked = pawn_attacks(space, white);
    for (int i = 0; i < 2; i++) {
        if (pawnAttacked[i]) {
            if (!counted[pawnAttacked[i] - 1]) {
                counter++;
                attacked[counter] = pawnAttacked[i];
                counted[pawnAttacked[i] - 1] = true;
            }
        }
    }

    free(pawnAttacked);
    return counter;
}


int king_helper(int space[2], int* attacked, int counter, bool* counted) {
    // All possible spaces for king to move
    int moves[8][2] = {{space[0], space[1] + 1}, {space[0], space[1] - 1}, {space[0] - 1, space[1]}, {space[0] + 1, space[1]}, 
        {space[0] + 1, space[1] - 1}, {space[0] + 1, space[1] + 1}, {space[0] - 1, space[1] + 1}, {space[0] - 1, space[1] - 1}};
    for (int i = 0; i < 8; i++) {
        // Add to attacked if not outside of board
        if (moves[i][0] >= 0 && moves[i][1] >= 0 && moves[i][0] <= 7 && moves[i][1] <= 7) {
            if (!counted[BOARDSPACES[moves[i][0]][moves[i][1]] - 1]) {
                counter++;
                attacked[counter] = BOARDSPACES[moves[i][0]][moves[i][1]];
                counted[BOARDSPACES[moves[i][0]][moves[i][1]] - 1] = true;
            }
        }
    }

    return counter;
}


int add_move(int* moveList, int counter, int move) {
    // Move will be 0 if not possible
    if (move) {
        counter++;
        moveList[counter] = move;
        moveList[0] = counter;
    }
    return counter;
}

int add_or_subtract(int base, int change, bool adding) {
    // Based on adding, add/subtract base & change
    if (adding) {
        return base + change;
    }
    return base - change;
}

void free_array(int* moves) {
    free(moves);
}