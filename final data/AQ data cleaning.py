import pandas as pd

# Load your data
data = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily/cleaned_air_quality.csv")

# Select relevant columns
columns_to_keep = [
    'Date', 'County', 'Pollutant', 'Year',
    'Daily Max 1-hour SO2 Concentration',
    'Daily Max 8-hour Ozone Concentration',
    'Daily Max 8-hour CO Concentration',
    'Daily Mean PM2.5 Concentration',
    'Daily Mean PM10 Concentration'
]

data = data[columns_to_keep]

# Ensure 'Date' is in datetime format (if not already)
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# List of pollutants
pollutant_columns = [
    'Daily Max 1-hour SO2 Concentration',
    'Daily Max 8-hour Ozone Concentration',
    'Daily Max 8-hour CO Concentration',
    'Daily Mean PM2.5 Concentration',
    'Daily Mean PM10 Concentration'
]

# Group by County, Pollutant, and Year to calculate statistics for each year
statistics = data.groupby(['County', 'Pollutant', 'Year'])[pollutant_columns].agg(
    mean='mean',
    median='median',
    percentile_25=lambda x: x.quantile(0.25),
    percentile_50=lambda x: x.quantile(0.50),
    percentile_75=lambda x: x.quantile(0.75)
).reset_index()

# Save the statistics to a CSV file
statistics.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/air_quality_statistics_by_year.csv', index=False)

# Display the resulting statistics
print(statistics.head())
