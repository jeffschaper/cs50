#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// 8-bit unsigned integer
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Checking commandline argument for exactly one argument
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open memory card file
    FILE *file = fopen(argv[1], "r");

    // Error check
    if (file == NULL)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Array of bytes
    // An array is a pointer
    BYTE buffer[512];

    // Generic counter to track number of JPEG's found
    int counter = 0;

    // File to write new img to
    FILE *img = NULL;

    // Can't read the file here becuase it needs to reasses in the while loop
    //int x = fread(buffer, 512, 1, file);

    // The array to store the data
    // Size of each element to read
    // Number of elements to read
    // File to read them from
    // Should return 1 if all bytes were read
    // Loop through the entire file
    while (fread(buffer, 512, 1, file) == 1)
    {
        // Is this the start of a new JPEG file?
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If yes, do this
            // Is this the first JPEG file?
            if (img == NULL)
            {
                char filename[8];
                // String to write to
                // Format string
                // Number to substitute
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "w");
                counter++;
                fwrite(buffer, 512, 1, img);

            }
            else if (img != NULL)
            {
                // If not the first JPEG file, and the start of a new JPEG. Close current file and open new file to write to
                fclose(img);
                char filename[8];

                // Create next JPEG file
                sprintf(filename, "%03i.jpg", counter);

                // Open next JPEG file
                img = fopen(filename, "w");
                counter++;

                // pointer to bytes to be written to file
                // Size of each element
                // Number of elements to write
                // write data to 000.jpg
                fwrite(buffer, 512, 1, img);
            }
        }
        else
        {
            // Continue writing
            if (img != NULL)
            {
                fwrite(buffer, 512, 1, img);
            }

        }
    }
    fclose(img);
    fclose(file);
}