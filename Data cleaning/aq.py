import requests
import pandas as pd

# API endpoint and parameters
base_url = "https://aqs.epa.gov/data/api/dailyData/byCounty"
params = {
    "email": "paloma030415@gmail.com",  # Register with the EPA API
    "key": "greymallard57",  # Replace with your API key
    "param": "44201",  # Example: Ozone (replace with desired pollutant code)
    "bdate": "20210101",  # Start date
    "edate": "20211231",  # End date
    "state": "54",  # State code for WV
    "county": "003"  # County code (example: Berkeley County)
}


response = requests.get(base_url, params=params)
data = response.json()

# Convert JSON to DataFrame
if "Data" in data:
    air_quality_df = pd.DataFrame(data["Data"])
    print(air_quality_df.head())
else:
    print("Error fetching data:", data)

# Save processed air quality data
air_quality_df.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/data_new/air_quality_data.csv", index=False)
