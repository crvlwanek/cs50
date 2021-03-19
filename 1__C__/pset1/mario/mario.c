#include <stdio.h>
#include <cs50.h>

int main(void){
    int height = 0;
    while (height < 1 || height > 8){
        height = get_int("Height: ");
    }
    for(int i = 1; i <= height; i++){
        int spaces = height - i;
        for(int j = 0; j < spaces; j++){
            printf(" ");
        }
        for(int j = 0; j < i; j++){
            printf("#");
        }
        printf("  ");
        for(int j = 0; j < i; j++){
            printf("#");
        }
        printf("\n");
    }

}