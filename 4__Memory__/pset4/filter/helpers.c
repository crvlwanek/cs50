#include "helpers.h"
#include <stdbool.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float temp = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0;
            int avg = round(temp);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            int originalBlue = image[i][j].rgbtBlue;
            int originalGreen = image[i][j].rgbtGreen;
            int originalRed = image[i][j].rgbtRed;
            int sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            int sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            int red = image[i][j].rgbtRed;
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1].rgbtRed = red;
            image[i][width - j - 1].rgbtBlue = blue;
            image[i][width - j - 1].rgbtGreen = green;
        }
    }
    return;
}

RGBTRIPLE average_values(int height, int width, int i, int j, RGBTRIPLE image[height][width]);
bool in_bounds(int height, int width, int i, int j, int di, int dj);

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = average_values(height, width, i, j, image);
        }
    }
    return;
}

RGBTRIPLE average_values(int height, int width, int i, int j, RGBTRIPLE image[height][width])
{
    int count = 0;
    int red = 0;
    int green = 0;
    int blue = 0;
    for (int di = -1; di < 2; di++)
    {
        for (int dj = -1; dj < 2; dj++)
        {
            if (in_bounds(height, width, i, j, di, dj))
            {
                red += image[i + di][j + dj].rgbtRed;
                blue += image[i + di][j + dj].rgbtBlue;
                green += image[i + di][j + dj].rgbtGreen;
                count++;
            }
        }
    }
    RGBTRIPLE temp;
    temp.rgbtBlue = blue / count;
    temp.rgbtGreen = green / count;
    temp.rgbtRed = red / count;
    return temp;
}

bool in_bounds(int height, int width, int i, int j, int di, int dj)
{
    return i + di >= 0 && i + di < height && j + dj >= 0 && j + dj < width;
}