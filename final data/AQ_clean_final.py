import pandas as pd 

df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/air_quality_statistics_by_year.csv')

import pandas as pd

# Assuming you have your dataframe loaded in `df`
# For example: df = pd.read_csv('your_data.csv')

# List of columns to keep: each pollutant will have 'Mean' and 'Median' columns only
columns_to_keep = [
    'County_',
    'Year_',
    'Daily Max 1-hour SO2 Concentration_mean',
    'Daily Max 1-hour SO2 Concentration_median',
    'Daily Max 8-hour Ozone Concentration_mean',
    'Daily Max 8-hour Ozone Concentration_median',
    'Daily Max 8-hour CO Concentration_mean',
    'Daily Max 8-hour CO Concentration_median',
    'Daily Mean PM2.5 Concentration_mean',
    'Daily Mean PM2.5 Concentration_median',
    'Daily Mean PM10 Concentration_mean',
    'Daily Mean PM10 Concentration_median'
]

# Select only the relevant columns
df_cleaned = df[columns_to_keep]

# Drop duplicate rows based on County_ and Year_ columns, keeping the first occurrence
df_cleaned = df_cleaned.drop_duplicates(subset=['County_', 'Year_'], keep='first')
df_cleaned = df_cleaned.round(3)
# Optionally, you can rename columns to remove spaces or make them easier to work with
df_cleaned.columns = [
    'County', 'Year', 'SO2 Mean', 'SO2 Median', 
    'Ozone Mean', 'Ozone Median', 'CO Mean', 'CO Median', 
    'PM2.5 Mean', 'PM2.5 Median', 'PM10 Mean', 'PM10 Median'
]

# Save the cleaned dataframe to a new CSV file
df_cleaned.to_csv('cleaned_data_no_duplicates.csv', index=False)

# Display the cleaned dataframe
print(df_cleaned.head())
