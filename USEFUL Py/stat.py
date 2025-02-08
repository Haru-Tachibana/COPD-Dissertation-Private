import pandas as pd

# Load the datasets
copd_df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/copd_data.csv')
demo_df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/demographic_data.csv')

copd_df['copd%_age'] = copd_df['copd%_age'].replace('%', '', regex=True).astype(float)
copd_df.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/copd_data.csv')


# Display first few rows of each dataset
print("COPD Data:")
print(copd_df.head())
print("\nDemographic Data:")
print(demo_df.head())

# Merge datasets on county and year (assuming columns 'County' and 'Year' exist in both datasets)
merged_df = pd.merge(copd_df, demo_df, on=['County', 'Year'], how='inner')

# Calculate summary statistics for each year
yearly_stats = merged_df.groupby('Year')[['copd%_age', 'healthcare', 'income', 'smoking']].describe()
# Calculate summary statistics
overall_stats = merged_df[['copd%_age', 'healthcare', 
                           'income', 'smoking']].describe()


# Save yearly and overall statistics to CSV files
yearly_stats.to_csv('yearly_statistics.csv')
overall_stats.to_csv('overall_statistics.csv')

# Display yearly and overall statistics
print("\nYearly Summary Statistics:")
print(yearly_stats)
print("\nOverall Summary Statistics:")
print(overall_stats)
