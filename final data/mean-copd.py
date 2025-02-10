import pandas as pd

# Load the dataset (replace 'your_file.csv' with the actual filename)
df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/copd_data.csv')

df = df[['County', 'Year', 'copd%_age']]
# Group by 'County' and calculate the mean COPD percentage
average_copd_df = df.groupby('County', as_index=False)['copd%_age'].mean()

# Save the result to a new CSV file (optional)
average_copd_df.to_csv('average_copd_per_county.csv', index=False)

# Display the resulting DataFrame
print(average_copd_df)
