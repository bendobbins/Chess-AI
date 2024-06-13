#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "moves.h"

int board[8][8] = {
    {27, 29, 0, 0, 0, 0, 9, 7},
    {25, 30, 0, 0, 0, 0, 10, 0},
    {23, 31, 0, 24, 4, 5, 11, 3},
    {22, 32, 0, 0, 0, 0, 12, 2},
    {21, 0, 0, 33, 13, 0, 0, 1},
    {0, 34, 26, 0, 0, 0, 14, 0},
    {0, 35, 0, 0, 0, 0, 15, 6},
    {28, 36, 0, 0, 0, 0, 16, 8}
};
#define IMAX_BITS(m) ((m)/((m)%255+1) / 255%255*8 + 7-86/((m)%255+12))
#define RAND_MAX_WIDTH IMAX_BITS(RAND_MAX)
_Static_assert((RAND_MAX & (RAND_MAX + 1u)) == 0, "RAND_MAX not a Mersenne number");


typedef struct evaluation {
    unsigned long long int hash;
    int bestMove[2];
    int depth;
    int evalType;
    int eval;
    int age;
} evaluation;

typedef struct evaluations {
    evaluation a;
    evaluation b;
    evaluation c;
    evaluation d;
} evaluations;

evaluations transpositions[1048583];

unsigned long long int zobristHashes[8][8][16];


uint64_t rand64(void) {
  uint64_t r = 0;
  for (int i = 0; i < 64; i += RAND_MAX_WIDTH) {
    r <<= RAND_MAX_WIDTH;
    r ^= (unsigned) rand();
  }
  return r;
}
    

void load_zobrist(void) {
    int i, j, k;
    for (i = 0; i < 8; i++) {
        for (j = 0; j < 8; j++) {
            for (k = 0; k < 16; k++) {
                zobristHashes[i][j][k] = rand64();
            }
        }
    }
}


int get_board_value(int board[8][8], bool white) {
    int i, j, boardValue = 0;
    for (i = 0; i < 8; i++) {
        for (j = 0; j < 8; j++) {
            if (white) {
                if (board[i][j] >= 1 && board[i][j] < 21) {
                    boardValue += PIECEVALUES[board[i][j] - 1];
                }
                else if (board[i][j] >= 21 && board[i][j] < 41) {
                    boardValue -= PIECEVALUES[board[i][j] - 21];
                }
            }

            else {
                if (board[i][j] >= 1 && board[i][j] < 21) {
                    boardValue -= PIECEVALUES[board[i][j] - 1];
                }
                else if (board[i][j] >= 21 && board[i][j] < 41) {
                    boardValue += PIECEVALUES[board[i][j] - 21];
                }
            }
        }
    }

    return boardValue;
}


int* make_move(int board[8][8], bool white, int moveCounter[40], int lastMove[2][2]) {
    int numPossiblePieces = 0, possiblePieces[20], *possibleMoves[20], *spaces[20], i, j, currentValue;
    currentValue = get_board_value(board, white);
    for (i = 0; i < 8; i++) {
        for (j = 0; j < 8; j++) {
            if ((white && board[i][j] >= 1 && board[i][j] < 21) || (!white && board[i][j] >= 21 && board[i][j] < 41)) {
                possiblePieces[numPossiblePieces] = board[i][j];
                int* space = malloc(sizeof(int) * 2);
                space[0] = i;
                space[1] = j;
                int* moves = get_moves(board, space, moveCounter[board[i][j] - 1]);
                possibleMoves[numPossiblePieces] = moves;
                spaces[numPossiblePieces] = space;
                numPossiblePieces++;
            }
        }
    }

    int boardsCount = 0;
    for (i = 0; i < numPossiblePieces; i++) {
        boardsCount += possibleMoves[i][0];
    }
    int boardValues[boardsCount][3], counter = 0;

    for (i = 0; i < numPossiblePieces; i++) {
        int newBoard[8][8], value;
        memcpy(newBoard, board, sizeof(int) * 8 * 8);
        newBoard[spaces[i][0]][spaces[i][1]] = 0;
        for (j = 1; j < possibleMoves[i][0] + 1; j++) {
            newBoard[REFERENCES[possibleMoves[i][j] - 1][0]][REFERENCES[possibleMoves[i][j] - 1][1]] = possiblePieces[i];
            value = get_board_value(newBoard, white);
            boardValues[counter][0] = value;
            boardValues[counter][1] = possiblePieces[i];
            boardValues[counter][2] = possibleMoves[i][j];
            counter++;
            newBoard[REFERENCES[possibleMoves[i][j] - 1][0]][REFERENCES[possibleMoves[i][j] - 1][1]] = 0;
        }
    }

    int bestMove = 0;
    for (i = 0; i < counter; i++) {
        if (boardValues[i][0] > bestMove) {
            bestMove = i;
        }
    }

    int* moveInfo = malloc(sizeof(int) * 2);
    if (!moveInfo) {
        printf("Memory allocation error\n");
        exit(1);
    }

    moveInfo[0] = boardValues[bestMove][1];
    moveInfo[1] = boardValues[bestMove][2];

    for (i = 0; i < numPossiblePieces; i++) {
        free(possibleMoves[i]);
        free(spaces[i]);
    }

    return moveInfo;
}


int main(void) {
    int lastMove[2][2] = {{0, 0}, {0, 0}};
    int moves[40];
    for (int i = 0; i < 40; i++) {
        if (i == 12 || i == 32 || i == 4 || i == 3 || i == 23 || i == 25) {
            moves[i] = 1;
        }
        else {
            moves[i] = 0;
        }
    }
    int* move = make_move(board, false, moves, lastMove);
    free(move);
    
    return 0;
}