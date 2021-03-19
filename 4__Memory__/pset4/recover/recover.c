#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
 if (argc != 2)
 {
     printf("Usage: ./recover card.raw");
     return 1;
 }
    char *file_name = argv[1];
    FILE *file = fopen(file_name, "r");
    if (file == NULL)
    {
        printf("File %s not found.\n", file_name);
        return 2;
    }
    unsigned char *buffer = malloc(512);
    int num = 0;
    FILE *img;
    while (fread(buffer, 512, 1, file))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (num > 0)
            {
                fclose(img);
            }
            char new_file_name[7];
            sprintf(new_file_name, "%03i.jpg", num);
            img = fopen(new_file_name, "w");
            if (img == NULL)
            {
                fclose(file);
                free(buffer);
                return 3;
            }
            num++;
        }
        if (!num)
        {
            continue;
        }
        fwrite(buffer, 512, 1, img);
    }
    fclose(file);
    fclose(img);
    free(buffer);
    return 0;
}