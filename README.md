# NFL-2024-Top5-Stats-Charts
This project analyzes NFL quarterback stats from historical data and visualizes the top players' performance metrics for a given week in the 2024 season. The data is loaded from an Excel file containing player statistics, and the script generates dynamic bar plots based on user input for the week number.

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
