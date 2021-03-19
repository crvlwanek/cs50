#include <stdio.h>
#include <cs50.h>

int main(void){
    // AMEX 34, 37
    // MASTERCARD 51, 52, 53, 53, 54, 55
    // VISA 4
    long num = get_long("Number: ");
    int total = 0;
    string type = "INVALID\n";
    while (num > 0)
    {
        if (num < 100)
        {
            if (num == 34 || num == 37)
            {
                type = "AMEX\n";
            }
            else if (num > 50 && num < 56)
            {
                type = "MASTERCARD\n";
            }
            else if (num == 4 || num / 10 == 4)
            {
                type = "VISA\n";
            }
        }
        total += num % 10;
        num /= 10;
        if (num < 100)
        {
            if (num == 34 || num == 37)
            {
                type = "AMEX\n";
            }
            else if (num > 50 && num < 56)
            {
                type = "MASTERCARD\n";
            }
            else if (num == 4 || num/10 == 4)
            {
                type = "VISA\n";
            }
        }
        int curr = (num % 10) * 2;
        while (curr > 0)
        {
            total += curr % 10;
            curr /= 10;
        }
        num /= 10;
    }
    if (total % 10 == 0)
    {
        printf("%s", type);
    }
    else
    {
        printf("INVALID\n");
    }
}