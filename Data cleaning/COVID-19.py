import pandas as pd

# Load COPD prevalence data from a local file or URL
url = "https://www.cdc.gov/brfss/data_documentation/index.htm"  # Replace with exact dataset URL
local_file = "/path/to/copd_data.csv"  # Replace with your local file path
copd_data = pd.read_csv(local_file)  # Or use url instead of local_file

# Preview data
print(copd_data.head())

# Save processed data
copd_data.to_csv("processed_copd_data.csv", index=False)