#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

float letter_count(string t);
float word_count(string t);
float sentence_count(string t);
 
int main(void)
{
    string text = get_string("Text: ");
    
     printf("Letter: %f\n",letter_count(text));
     printf("Word: %f\n",word_count(text));
     printf("Sentence: %f\n",sentence_count(text));
    
    float S = (sentence_count(text) / word_count(text)) * 100;
    float L = (letter_count(text) / word_count(text)) * 100;
    float index = 0.0588 *  L - 0.296 *  S - 15.8;
    int grade = round(index);
    
    
    
    printf("S: %f\n", S);
    printf("L: %f\n", L);
    // printf("index %f\n", index);
    // printf("grade: %i\n", grade);
    
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else 
    {
        printf("Grade %i\n", grade);    
    }
    
}

// Counts letters
float letter_count(string t)
{
    int alphaCount = 0;
    int l = 0;
    int n = strlen(t);
    while (l < n)
    {
        if (isalpha(t[l]))
        {
            alphaCount++;
        }
        l++;
    }
    return (float) alphaCount;
}
 
// Counts words
float word_count(string t)
{
    int w_count = 0;
    int w = 0;
    //int n = strlen(t);
    while (t[w] != '\0')
    {
        if (w == 0)
        {
            w_count++;
        }
        // if t[w] is a space or is a new line or tab
        //else if(isspace(t[w + 1]) == isalpha(t[w]))
        //else if(t[w] == '\0' && t[w + 1] == isalpha(t[w]))
        else if (t[w] == ' ' || t[w] == '\t' || t[w] == '\n')
        {
            w_count++;
        }
        w++;
    } 
    return (float) w_count;
}
 
// Count sentences
// . ! ?
float sentence_count(string t)
{
    int s_count = 0;
    int s = 0;
    while (t[s] != '\0')
    {
        if (t[s] == '!' || t[s] == '.' || t[s] == '?')
        {
            s_count++;
        }
        s++;
    }
    return (float) s_count;
}