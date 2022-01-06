
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

bool castle_valid(int spaces[][2], int board[8][8], int pieces[2], bool queen, bool whiteAttacking, int moveCounts[2]) {
    if (moveCounts[0] == 0 && moveCounts[1] == 0) {
        if (!queen) {
            if (board[spaces[0][0]][spaces[0][1]] == 0 && board[spaces[1][0]][spaces[1][1]] == 0) {
                int* attacked = attacked_spaces(board, whiteAttacking, false);
                bool valid = true;
                for (int i=1; i<attacked[0]+1; i++) {
                    if (attacked[i] == boardSpaces[spaces[0][0]][spaces[0][1]] ||
                        attacked[i] == boardSpaces[spaces[1][0]][spaces[1][1]] ||
                        attacked[i] == boardSpaces[spaces[2][0]][spaces[2][1]]) {
                            valid = false;
                        }
                }
                free(attacked);
                if (valid) {
                    return true;
                }
            }
        }

        else {
            if (board[spaces[0][0]][spaces[0][1]] == 0 && board[spaces[1][0]][spaces[1][1]] == 0
                && board[spaces[2][0]][spaces[2][1]]) {
                    int* attacked = attacked_spaces(board, whiteAttacking, false);
                    bool valid = true;
                    for (int i=1; i<attacked[0]+1; i++) {
                        if (attacked[i] == boardSpaces[spaces[3][0]][spaces[3][1]] ||
                            attacked[i] == boardSpaces[spaces[2][0]][spaces[2][1]] ||
                            attacked[i] == boardSpaces[spaces[1][0]][spaces[1][1]]) {
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