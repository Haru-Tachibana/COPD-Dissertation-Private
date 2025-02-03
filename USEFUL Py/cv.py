import pandas as pd

# Load your dataframes
demographic_data = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/demographic_data.csv')
copd_data = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/copd_data.csv')

# Ensure the 'County' and 'Year' columns are the same name for merging
# If necessary, rename the columns for consistency
copd_data = copd_data.rename(columns={"copd%_age": "copd_age"})  # Rename copd column to remove % symbol later

# Remove the '%' symbol and convert 'copd_age' column to numeric
copd_data['copd_age'] = copd_data['copd_age'].str.replace('%', '').astype(float)

# Merge the three dataframes based on 'County' and 'Year'
merged_data = pd.merge(demographic_data, copd_data, on=["County", "Year"], how="inner")


# Display the merged dataframe
print(merged_data.head())

merged_data.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/merged_data.csv", index=False)