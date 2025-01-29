import pandas as pd

# Load your data
data = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily/cleaned_air_quality.csv")

# Select relevant columns
columns_to_keep = [
    'Date', 'State', 'Pollutant', 'Year',
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

# Define the aggregation functions
agg_funcs = {
    'Daily Max 1-hour SO2 Concentration': ['mean', 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.50), lambda x: x.quantile(0.75)],
    'Daily Max 8-hour Ozone Concentration': ['mean', 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.50), lambda x: x.quantile(0.75)],
    'Daily Max 8-hour CO Concentration': ['mean', 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.50), lambda x: x.quantile(0.75)],
    'Daily Mean PM2.5 Concentration': ['mean', 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.50), lambda x: x.quantile(0.75)],
    'Daily Mean PM10 Concentration': ['mean', 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.50), lambda x: x.quantile(0.75)]
}

# Group by State and Year, then apply the aggregation functions
statistics_state = data.groupby(['State', 'Year']).agg(agg_funcs).reset_index()

# Flatten multi-level columns after aggregation
statistics_state.columns = ['_'.join(col).strip() for col in statistics_state.columns.values]

# Save the statistics to a CSV file
statistics_state.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/air_quality_state_statistics_by_year.csv', index=False)

# Display the resulting statistics
print(statistics_state.head())
