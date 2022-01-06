#include <stdio.h>
#include <stdlib.h>

int* printarray(int moves[][2]) {
    int *a = malloc(sizeof(int) * 4);
    for (int i=0; i<4; i++) {
        for (int j=0; j<2; j++) {
            // printf("%i\n", moves[i][j]);
        }
        a[i] = i;
    }
    return a;
}