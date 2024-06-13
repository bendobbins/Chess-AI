#include <stdbool.h>
/* NOTE
Was much easier to pass a pointer from C to Python than a pointer to a list of pointers, so
spaces on the board will be represented by one of the numbers in the 2d array below instead of a 
tuple/array with row and column values. The switch from this number representation to row & column
values will be made after possible moves/attacked spaces are found.
*/

#ifndef BOARDSPACES_H
#define BOARDSPACES_H
extern const int BOARDSPACES[8][8];
#endif // BOARDSPACES_H

#ifndef REFERENCES_H
#define REFERENCES_H
extern const int REFERENCES[64][2];
#endif // REFERENCES_H

#ifndef INSUFFICIENT3_H
#define INSUFFICIENT3_H
extern const int INSUFFICIENT3[12][3];
#endif // INSUFFICIENT3_H

#ifndef INSUFFICIENT4_H
#define INSUFFICIENT4_H
extern const int INSUFFICIENT4[42][4];
#endif // INSUFFICIENT4_H

#ifndef PIECEVALUES_H
#define PIECEVALUES_H
extern const int PIECEVALUES[20];
#endif // PIECEVALUES_H

// moves.c prototypes
int* get_moves(int board[8][8], int selected[2], int moveCount);
int* valid_pawn_moves(int start[2], int board[8][8], int piece, int moveCounter);
int* valid_knight_moves(int start[2], int board[8][8], int piece, bool checkProtected);
int* valid_bishop_moves(int start[2], int board[8][8], int piece, bool checkProtected);
int* valid_rook_moves(int start[2], int board[8][8], int piece, bool checkProtected);
int* valid_queen_moves(int start[2], int board[8][8], int piece, bool checkProtected);
int* valid_king_moves(int start[2], int board[8][8], int piece, bool checkProtected);
int* attacked_spaces(int board[8][8], bool white, bool checkProtected);

// helper.c prototypes
int check_pawn_move(int board[8][8], int space[2], bool white);
int check_knight_move(int board[8][8], int space[2], bool white, bool checkProtected);
int attacked_helper(int* attacked, int* pieceAttacks, int counter, bool* counted);
int* pawn_attacks(int start[2], bool white);
int king_helper(int space[2], int* attacked, int counter, bool* counted);
int pawn_helper(int* attacked, int counter, bool* counted, int space[2], bool white);
int add_move(int* moveList, int counter, int move);
int add_or_subtract(int base, int change, bool operation);
void free_array(int* moves);

// special_moves.c prototypes
bool castle(bool white, int space[2], int moveSpace[2], int board[8][8], int moveCounts[40]);
bool castle_valid(int** spaces, int board[8][8], int pieces[2], bool queen, bool whiteAttacking, int moveCounts[2]);
bool en_passant(bool white, int lastMove[2][2], int board[8][8], int space[2], int moveSpace[2]);
bool check_pawn_upgrade(bool white, int board[8][8], int space[2], int moveCol);

// check_endings.c prototypes
int* checkmate(int board[8][8], bool white, int range[2], int fifty, int moveCounter[40], int repetitions[][8][8], int repetitionLength);
bool check_checkmate(bool white, int board[8][8], int range[2], int king[2], int moveCounter[40]);
bool check_draw(int board[8][8], int range[2], int amtKingMoves, int fifty, int moveCounter[40], int repetitions[][8][8], int repetitionLength);
bool repetition_checker(int repetitions[][8][8], int repetitionLength);
void selection_sort(int* pieces, int size);
void swap(int* x, int* y);