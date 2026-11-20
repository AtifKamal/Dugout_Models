# Dugout

Name: Atif Kamal
Batch: Advanced Python for AI, LiveX Nano Degree, Batch 3

This is my Deliverable 1 for Week 1. Dugout is a small fantasy cricket program that uses PSL 2026 data. It reads the player list and some fantasy teams from CSV files, checks each team against the league rules and then ranks the teams by credits.

## Running it

Only Python 3 is needed, nothing to install.

    python main.py

The data files are found from the location of main.py, so it can be run from any folder.

## Files

- dugout/models.py has the Player, FantasyTeam and League classes
- dugout/rules.py has the limits (11 players, 100 credits, 7 per franchise, role limits) and the check functions
- dugout/loader.py reads the CSV files
- data/players.csv is the 142 players
- data/sample_teams.csv has the 6 teams from class plus my 2 test teams
- data/my_team.csv is my own XI

Every check function returns a list of error messages. An empty list means the team passed that rule, and check_rules in FantasyTeam collects all of them.

## Part B

B1: check_no_duplicates in rules.py keeps the IDs it has already seen while going through the team. If it meets an ID again it adds a message with the player's name. Each repeated player is reported once even if picked three times. It is added to check_rules so it actually runs.

B2: I added two teams at the end of sample_teams.csv. Double Trouble (Kamran) has Naseem Shah twice and nothing else wrong. No Gloves XI (Hira) has no wicket-keeper and nothing else wrong.

B3: my team is Kamal Strikers in my_team.csv. main.py loads it with load_team, prints it with show_team, then prints the credits left and LEGAL or the problems. It costs 97.5 so 2.5 are left.

B4: all the sample teams and my team go into one League and rank_teams() gives them cheapest first. I also made a reverse option so the table can be printed the other way round too.

## What to expect

- pool of 142 players: WK 15, BAT 47, AR 22, BOWL 58
- the 6 class teams give 2 legal and 4 illegal
- with my 2 test teams it is 2 legal and 6 illegal out of 8
- my team is LEGAL with 2.5 credits left

Some of the output:

    Team Double Trouble by Kamran:
    ...
    ILLEGAL:
      - Naseem Shah is picked more than once

    Summary: 2 legal, 6 illegal out of 8 teams

    --- My team ---
    Credits left: 2.5
    LEGAL

    --- League table (cheapest first) ---
    Ten Men             Fatima        84.5   ILLEGAL
    Bowling Machine     Usman         87.5   ILLEGAL
    Gully Strikers      Bilal         97.5   LEGAL
    Double Trouble      Kamran        97.5   ILLEGAL
    Kamal Strikers      Atif Kamal    97.5   LEGAL
    Qalandar Fans       Zainab        98.5   ILLEGAL
    No Gloves XI        Hira          99.0   ILLEGAL
    Lahore Lions        Ayesha       100.0   LEGAL
    Big Spenders        Hamza        112.0   ILLEGAL

Gully Strikers, Double Trouble and my team all cost 97.5, so they stay in the order they were added.

Match data is from Cricsheet (cricsheet.org), used under the Open Data Commons Attribution License.
