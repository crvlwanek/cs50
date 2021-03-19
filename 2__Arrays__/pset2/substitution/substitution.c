#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

bool has_valid_arguments(int argc);
bool is_valid_key(string key);

int main(int argc, string argv[])
{
    if (!has_valid_arguments(argc) || !is_valid_key(argv[1]))
    {
        return 1;
    }

    string key = argv[1];
    string text = get_string("plaintext: ");
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if isalpha(text[i])
        {
            int idx = toupper(text[i]) - 65;
            int new_idx = toupper(key[idx]) - 65;
            text[i] = text[i] + new_idx - idx;
        }
    }
    printf("ciphertext: %s\n", text);
    return 0;
}

bool has_valid_arguments(int argc)
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key");
        return false;
    }
    return true;
}

bool is_valid_key(string key)
{
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.");
        return false;
    }
    return true;
}