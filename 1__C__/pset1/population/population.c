#include <cs50.h>
#include <stdio.h>

int how_many_years();
int one_year();

int main(void)
{
    int start_size = 0;
    int end_size = 0;
    while (start_size < 9) {
        start_size = get_int("Start size: ");
    }
    while (end_size < start_size) {
        end_size = get_int("End size: ");
    }

    int years = how_many_years(start_size, end_size);
    printf("Years: %d\n", years);
}

int one_year(int population) {
        return population + (population / 3) - (population / 4);
    }

int how_many_years(int start_size, int end_size) {
    int years = 0;
    while (start_size < end_size) {
        start_size = one_year(start_size);
        years++;
    }
    return years;
}