#include <cs50.h>
#include <stdio.h>

#include <string.h>
#include <math.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    //int index; // added index
    string name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        //candidates[i].index = i;
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid
// The arguments are determining the location of the two-dimensional array (Voter = row, rank/preference = column)
bool vote(int voter, int rank, string name)
{
    // TODO

    // Loop though the candidate array
    for (int i = 0; i < candidate_count; i++)
        // If the candidates name == the name in the argv input, then 0 (exact match)
        if (strcmp(candidates[i].name, name) == 0)
        {
            preferences[voter][rank] = i;
            return true;
        }
    //
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    int x = 0;
    bool done = false;
    //Each voter
    for (int i = 0; i < voter_count; i++)
    {
        done = false;
        x = 0;
        while (!done)
        {
            // Each candidate in candidate array.
            for (int j = 0; j < candidate_count; j++)
            {
                if (preferences[i][x] == j && candidates[j].eliminated == false)
                {
                    done = true;
                    candidates[j].votes++;
                    break;
                }
            }
            x++;
        }
    }
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    // TODO

    // Variables
    // rounds decimals to highest number if half the votes is a decimal. Example half of 5 is 2.5 rounded to 3
    // Floor returns double which needs to be cast as int
    double x = floor((double) voter_count / 2);

    // Loop through the candidates
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > x)
        {
            printf("%s\n", candidates[i].name);
            return true;
        }
    }

    //
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    // TODO

    int minSoFar = 0;
    bool firstTime = true;
    // Loop through the candidates array to
    for (int i = 0; i < candidate_count; i++)
    {

        if (candidates[i].eliminated == false)
        {
            int count = candidates[i].votes;

            if (count < minSoFar && !firstTime)
            {
                minSoFar = count;
            }
            else if (firstTime)
            {
                minSoFar = count;
                firstTime = false;
            }

        }
    }
    //
    return minSoFar;
    //return 0;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    // TODO

    // Loop through the candidates array
    for (int i = 0; i < candidate_count; i++)
    {
        // If candidate[i] == minimum number of votes, && is not eliminated, return true then go to the next candidate
        if (min != candidates[i].votes && candidates[i].eliminated == false)
        {
            return false;
        }
    }

    //
    return true;
    //return false;
}

// Eliminate the candidate (or candidiates) in last place
void eliminate(int min)
{
    // TODO

    // Loop through the candidates
    for (int i = 0; i < candidate_count; i++)
    {
        if (min == candidates[i].votes && candidates[i].eliminated == false)
        {
            candidates[i].eliminated = true;
        }
    }
    //
    return;
}