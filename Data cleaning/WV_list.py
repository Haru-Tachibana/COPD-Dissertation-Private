import requests
import pandas as pd

# Correct API endpoint for the Census Bureau
url = "https://api.census.gov/data/2020/acs/acs5"

# Parameters for fetching county data for West Virginia
params = {
    "get": "NAME",         # Retrieve the county names
    "for": "county:*",     # Fetch all counties
    "in": "state:54",      # State FIPS code for West Virginia
    "key": "77f79409740da8be3b2568fa55f38909206c928c"  # Your API key
}

# Fetch data from the API
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    # Convert the response to a pandas DataFrame
    columns = data[0]  # First row contains column names
    rows = data[1:]    # Remaining rows contain data
    counties_df = pd.DataFrame(rows, columns=columns)
    
    # Display the DataFrame
    print(counties_df)
    
    # Save to CSV
    counties_df.to_csv("./data_new/wv_counties.csv", index=False)
    print("Data saved to ./data_new/wv_counties.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")
