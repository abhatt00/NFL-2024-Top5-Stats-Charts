# NFL-2024-Top5-Stats-Charts
This project leverages Python to analyze NFL quarterback statistics from historical and current data, focusing on visualizing the top-performing players for a user-specified week of the 2024 season. The Python script dynamically processes data from an Excel file containing detailed player performance metrics, such as touchdowns (TD), passing yards, completions, and more.
The script allows users to input a specific week (1–18) to filter and analyze player statistics up to and including that week. It generates bar charts for "Top 5" players across various key metrics, such as touchdowns, passing yards, completions, pass attempts, and other advanced efficiency measures like Net Yards per Attempt (NY/A) and Adjusted Net Yards per Attempt (ANY/A).
These metrics are chosen to highlight individual excellence and consistency in quarterback performance, providing insights into the most impactful players of the season. By focusing on these "Top 5" charts, the analysis aims to identify and visualize key contributors to their teams, making the data both meaningful and actionable for fans, analysts, and fantasy football enthusiasts.
Datasets included are gathered and updated in Excel file manually, and cover the 2001 regular season to Present.

I started running this code and receiving accurate resulting charts from Week 5 of the 2024 onwards. I will include all created charts that I've gathered for the season once the 2024 NFL regular season is over.

## Features
- Aggregates quarterback statistics across seasons.
- Filters data for players with significant game-time contributions (8 or more games played).
- Dynamically generates bar plots for metrics like:
  - Passing Yards
  - Touchdowns
  - Completion Percentage
  - Adjusted Net Yards per Attempt
  - Touchdown-to-Interception Ratio
- User-friendly input for selecting statistics up to and including that week of the NFL season (1–18).
- Execution time tracking for performance optimization.

## Prerequisites
- Python 3.8+
- Libraries:
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - scikit-learn
  - statsmodels

This repository contains code in a Python file that is run to obtain the resulting chart files, which are also included. 
The charts included are an example of what I receive when I run the code weekly.
I post all charts for each week at the end of each week of games to my personal TIkTok account (@galaxyace_12) for fun and user engagement.
