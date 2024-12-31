# Gather data
import time  # Import the time module for measuring execution time
# Start the timer
start_time = time.time()

import pandas as pd  # Import the pandas library for data manipulation
import numpy as np  # Import the numpy library for numerical operations
import matplotlib.pyplot as plt  # Import the matplotlib library for plotting
import matplotlib.image as mpimg  # Import the matplotlib image library for image processing
import seaborn as sns  # Import the seaborn library for creating advanced visualizations
import re  # Import the re library for regular expression operations
from pandas import ExcelWriter  # Import the ExcelWriter from pandas for writing Excel files
from math import pi  # Import pi for mathematical calculations
import statsmodels.api as sm
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
# import tensorflow as tf

# Prompt for the week number input
while True:
    try:
        week_number = int(input("Enter the week number (1 to 18): "))
        if 1 <= week_number <= 18:
            break
        else:
            print("Please enter a valid number between 1 and 18.")
    except ValueError:
        print("Invalid input. Please enter a numeric value between 1 and 18.")

# Load the Excel file for source data
file_path = "your/file/path/"
data = pd.ExcelFile(file_path)
# data

# Dynamically get all sheet names
sheets = data.sheet_names
# sheets

# Define the common columns
common_columns = [
    'season', 'Player', 'Tm', 'Age', 'Pos', 'G', 'GS', 'QBrec', 'Cmp', 'Att', 'Cmp%',
    'Yds', 'TD', 'TD%', 'Int', 'Int%', '1D', 'Lng', 'Y/A', 'AY/A', 'Y/C',
    'Y/G', 'Rate', 'QBR', 'Sk', 'Yds.1', 'Sk%', 'NY/A', 'ANY/A', '4QC', 'GWD'
]
#common_columns
# Combine the data from all sheets
combined_data = pd.DataFrame()

for sheet in sheets:
    df = data.parse(sheet)
    if not df.empty and len(df.columns) >= len(common_columns):  # Check if the sheet is not empty and has enough columns
        df = df.iloc[:, :len(common_columns)]
        df.columns = common_columns
        combined_data = pd.concat([combined_data, df], ignore_index=True)

# print("Combined DataFrame:")
# combined_data.head()

# Replace missing values with 0
combined_data.fillna(0, inplace=True)

# Verify that there are no more missing values
missing_values_count_after = combined_data.isnull().sum()
print("\nMissing values after filling with 0:")
print(missing_values_count_after[missing_values_count_after > 0])

# Display the first few rows of the modified DataFrame
print("\nModified DataFrame:")
print(combined_data.head())

# # Transform 'Sk' to 'Times Sacked'
# # Transform 'Yds.1' to 'Yds/Sack'
combined_data.rename(columns={'Sk':'Times Sacked',
                              'Yds.1': 'Yds/Sack'
                              }, inplace=True)

# Function to clean player names by removing non-letter characters
def clean_name(name):
    return re.sub(r'[^a-zA-Z\s]', '', name)

# Apply the cleaning function to the 'Player' column
combined_data['Player'] = combined_data['Player'].apply(clean_name)

# Ensure 'QBrec' values are strings
combined_data['QBrec'] = combined_data['QBrec'].astype(str)

def extract_wins(qbrec):
    if isinstance(qbrec, str):
        # Handle the date-like format (####-##-## 00:00:00)
        match_date_format = re.search(r'^\d{4}-(\d{2})-\d{2}', qbrec)
        if match_date_format:
            return int(match_date_format.group(1))
        # Handle the record format (##-##-0)
        match_record_format = re.search(r'^(\d{1,2})-\d{1,2}-\d{1,2}$', qbrec)
        if match_record_format:
            return int(match_record_format.group(1))
    return 0

# Apply the function to the 'QBrec' column to create a 'Wins' column
combined_data['Wins'] = combined_data['QBrec'].apply(extract_wins)

# Create new metric 'TD to Interception Ratio'
combined_data['TD_to_Int_Ratio'] = np.where(combined_data['Int'] > 0, combined_data['TD'] / combined_data['Int'], combined_data['TD'])

df_copy = combined_data.copy()

# Assuming df_copy is your DataFrame, round to 2 decimals
df_copy = df_copy.round(2)

# Rounding the 'GWD' column to zero decimal places and converting to integer
df_copy['GWD'] = df_copy['GWD'].round(0).astype(int)

# Filter the data to include only players who played in 2024.
filtered_data_2024 = df_copy[(df_copy['season'] == 2024)]
# Creating dataframes for top 5 players by different metrics in descending order
# 1. Top 5 players by TD
filtered_2024_top_5_td = filtered_data_2024.nlargest(5, 'TD')
# 2. Top 5 players by Yards
filtered_2024_top_5_yds = filtered_data_2024.nlargest(5, 'Yds')
# 3. Top 5 players by Completions (Cmp)
filtered_2024_top_5_cmp = filtered_data_2024.nlargest(5, 'Cmp')
# 4. Top 5 players by Attempts (Att)
filtered_2024_top_5_att = filtered_data_2024.nlargest(5, 'Att')
# 5. Top 5 players by Wins
filtered_2024_top_5_wins = filtered_data_2024.nlargest(5, 'Wins')
# 6. Top 5 players by TD%
filtered_2024_top_5_td_pct = filtered_data_2024.nlargest(5, 'TD%')
# 7. Top 5 players by Sk%
filtered_2024_top_5_sk_pct = filtered_data_2024.nlargest(5, 'Sk%')
# 8. Top 5 players by Net Yards per Attempt (NY/A)
filtered_2024_top_5_ny_a = filtered_data_2024.nlargest(5, 'NY/A')
# 9. Top 5 players by Adjusted Net Yards per Attempt (ANY/A)
filtered_2024_top_5_any_a = filtered_data_2024.nlargest(5, 'ANY/A')
# 10. Top 5 players by TD to Interception Ratio (TD_to_Int_Ratio)
filtered_2024_top_5_td_to_int_ratio = filtered_data_2024.nlargest(5, 'TD_to_Int_Ratio')

print("Now making charts.")

# Create a bar plot for top 5 players by TD
def create_bar_plot_top_5(data, y_col, title, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(data['Player'], data[y_col], color='skyblue', width=0.5)
    ax.set_title(title)
    ax.set_xlabel('Player')
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)

    # # Add value labels on bars
    # for bar in bars:
    #     yval = bar.get_height()
    #     ax.text(bar.get_x() + bar.get_width() / 2, yval, round(yval), ha='center', va='bottom', fontsize=10)
    # Add value labels on bars with conditional formatting for decimal places
    for bar in bars:
        yval = bar.get_height()
        if round(yval, 2) == round(yval):
            label = f"{int(yval)}"
        else:
            label = f"{round(yval, 1)}"
        ax.text(bar.get_x() + bar.get_width() / 2, yval, label, ha='center', va='bottom', fontsize=10)


    fig.tight_layout()
    # Save the plot as a PNG file
    plt.savefig(f"{title}.png")
    return fig

# Create and display the bar plot for top 5 players by TD
fig_td = create_bar_plot_top_5(filtered_2024_top_5_td, 'TD', f'2024 Top 5 Players by Touchdowns (TD) through Week {week_number}', 'Touchdowns')
# Create and display the bar plot for top 5 players by TD
fig_yds = create_bar_plot_top_5(filtered_2024_top_5_yds, 'Yds', f'2024 Top 5 Players by Passing Yards through Week {week_number}', 'Yards')
# Create and display the bar plot for top 5 players by TD
fig_cmp = create_bar_plot_top_5(filtered_2024_top_5_cmp, 'Cmp', f'2024 Top 5 Players by Completions through Week {week_number}', 'Completions')
# Create and display the bar plot for top 5 players by TD
fig_att = create_bar_plot_top_5(filtered_2024_top_5_att, 'Att', f'2024 Top 5 Players by Pass Attempts through Week {week_number}', 'Pass Attempts')
# Create and display the bar plot for top 5 players by TD
fig_wins = create_bar_plot_top_5(filtered_2024_top_5_wins, 'Wins', f'2024 Top 5 Players by Wins through Week {week_number}', 'Games Won')
# Create and display the bar plot for top 5 players by TD
fig_ny_a = create_bar_plot_top_5(filtered_2024_top_5_ny_a, 'NY/A', f'2024 Top 5 Players by Net Yards per Pass Attempt through Week {week_number}', 'NY/A')
# Create and display the bar plot for top 5 players by TD
fig_any_a = create_bar_plot_top_5(filtered_2024_top_5_any_a, 'ANY/A', f'2024 Top 5 Players by Adjusted Net Yards per Pass Attempt through Week {week_number}', 'ANY/A')
# Create and display the bar plot for top 5 players by TD
fig_td_to_int_ratio = create_bar_plot_top_5(filtered_2024_top_5_td_to_int_ratio, 'TD_to_Int_Ratio', f'2024 Top 5 Players by TD to Interception Ratio through Week {week_number}', 'TD/Int Ratio')


# End the timer
end_time = time.time()
# Calculate elapsed time
elapsed_time = end_time - start_time
# Convert to minutes and seconds
minutes, seconds = divmod(elapsed_time, 60)
# Display elapsed time
if minutes > 0:
    print(f"\nTime taken to run the script: {int(minutes)} min {seconds:.2f} sec")
else:
    print(f"\nTime taken to run the script: {seconds:.2f} seconds")

