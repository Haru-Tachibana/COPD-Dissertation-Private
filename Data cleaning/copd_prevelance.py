import pandas as pd

# Load COPD prevalence data from a local file
local_file = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/data_new/copd_data.csv"
copd_data = pd.read_csv(local_file)

# Preview data
print(copd_data.head())

# Save processed data
copd_data.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/data_new/processed_copd_data.csv", index=False)
