#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    // index = 0.0588 * L - 0.296 * S - 15.8
    // L = letters per 100 words, S = sentances per 100 words

    // Prompt user for input string
    string input = get_string("Text: ");

    // Counter letters, words, and sentences
    int letters = 0;
    int words = 1;
    int sentences = 0;
    for (int i = 0; input[i] != 0; i++)
    {
        if (isalpha(input[i]))
        {
            letters++;
        }
        if (isspace(input[i]))
        {
            words++;
        }
        if (input[i] == '.' || input[i] == '!' || input[i] == '?')
        {
            sentences++;
        }
    }

    // Output grade level
    // printf("%i letter(s)\n", letters);
    // printf("%i words(s)\n", words);
    // printf("%i sentence(s)\n", sentences);

    float L = 100 * letters / words;
    float S = 100 * sentences / words;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        int num = round(index);
        printf("Grade %i\n", num);
    }
}