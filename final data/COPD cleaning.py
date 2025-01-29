import pandas as pd

# Load your data
data = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/copd_wv.csv")

# Drop specified columns
copd = data.drop(columns=['StateFIPS', 'State', 'CountyFIPS', 'CI_low_copd_age', 'CI_high_copd_age', 'State_County_Year', 'State_County', 'copd%_crude', 'CI_low_copd_crude', 'CI_high_copd_crude'])

# Check the first few rows of the resulting dataframe
print(copd.head())

output_path = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data"
copd.to_csv(output_path + '/copd_data.csv', index=False)