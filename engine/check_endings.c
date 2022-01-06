#include <stdbool.h>

int boardSpaces[8][8] = {
    {1, 2, 3, 4, 5, 6, 7, 8},
    {9, 10, 11, 12, 13, 14, 15, 16},
    {17, 18, 19, 20, 21, 22, 23, 24},
    {25, 26, 27, 28, 29, 30, 31, 32},
    {33, 34, 35, 36, 37, 38, 39, 40},
    {41, 42, 43, 44, 45, 46, 47, 48},
    {49, 50, 51, 52, 53, 54, 55, 56},
    {57, 58, 59, 60, 61, 62, 63, 64}
};


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


int* reference_to_space(int* moves) {
    int counter = 0;
    int* spaces = malloc(sizeof(int) * moves[0] * 2);
    if (!spaces) {
        printf("Memory allocation error\n");
        exit(1);
    }
    for (int i=1; i<moves[0]+1; i++) {
        for (int j=0; j<8; j++) {
            for (int k=0; k<8; k++) {
                if (moves[i] == boardSpaces[j][k]) {
                    spaces[counter] = j;
                    counter++;
                    spaces[counter] = k;
                    counter++;
                    break;
                }
            }
        }
    }

    free(moves);
    return spaces;
}


bool checkmate(int board[8][8], bool white, int range[2], int moveCounter[40]) {
    //bool* endings = malloc(sizeof(int) * 2);
    //if (!endings) {
    //    printf("Memory allocation error\n");
    //    exit(1);
    //}
    bool ending = false;

    int* attacked = attacked_spaces(board, white, false);
    int king[2];

    int i, j = 0;
    for (; i<8; i++) {
        for (; j<8; j++) {
            if ((board[i][j] == 1 && !white) || (board[i][j] == 21 && white)) {
                king[0] = i;
                king[1] = j;
            }
        }
    }


    int* kingMoves = valid_king_moves(king, board, board[king[0]][king[1]], true);

    bool kingAttacked = false;
    for (int i=1; i<attacked[0]+1; i++) {
        if (attacked[i] == boardSpaces[king[0]][king[1]]) {
            kingAttacked = true;
        }
    }

    if (kingAttacked && !kingMoves[0]) {
        ending = check_checkmate(white, board, range, king, moveCounter);
    }
    free(kingMoves);
    free(attacked);

    return ending;
}


bool check_checkmate(bool white, int board[8][8], int range[2], int king[2], int moveCounter[40]) {
    for (int i=range[0]; i<range[1]; i++) {
        for (int j=0; j<8; j++) {
            for (int k=0; k<8; k++) {
                if (board[j][k] == i) {
                    int space[2] = {j, k};
                    int* moves = reference_to_space(get_moves(board, space, moveCounter[board[j][k] + 1]));

                    for (int l=0; l<moves[0]; l+2) {
                        int newboard[8][8];
                        memcpy(newboard, board, sizeof(int) * 8 * 8);
                        newboard[moves[l]][moves[l+1]] = i;
                        newboard[j][k] = 0;

                        int* attacked = attacked_spaces(newboard, white, false);

                        bool notAttacked = false;
                        for (int o=1; o<attacked[0]+1; o++) {
                            if (attacked[o] == boardSpaces[king[0]][king[1]]) {
                                notAttacked = true;
                            }
                        }
                        free(attacked);
                        if (notAttacked) {
                            return false;
                        }
                    }
                    free(moves);
                }
            }
        }
    }
    return true;
}
