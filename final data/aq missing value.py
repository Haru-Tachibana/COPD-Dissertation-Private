import pandas as pd

# Load your data
AQ = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/air_quality_statistics_by_year.csv')
county_list = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/demographic_data.csv')

# Clean the county_list by dropping unnecessary columns
county_list = county_list.drop(columns=['healthcare', 'income', 'smoking'])

# Create unique columns in both DataFrames
AQ['unique_col'] = AQ['County_'] + "_" + AQ['Year_'].astype(str)
county_list['unique_col'] = county_list['County'] + "_" + county_list['Year'].astype(str)

# Perform the left join based on the unique column
merged_df = pd.merge(county_list, AQ, on='unique_col', how='left')

# Save the merged DataFrame to a CSV file (optional)
merged_df.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/merged_output.csv', index=False)

# Display the resulting DataFrame
print(merged_df.head())
