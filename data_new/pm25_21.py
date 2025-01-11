import requests
import pandas as pd
import time

# API endpoint
base_url = "https://aqs.epa.gov/data/api/dailyData/byCounty"

# Replace with your EPA API credentials
email = "yuyang.wang027@gmail.com"  # Registered email
api_key = "coppercrane18"           # Your API key

# PM2.5 parameter code
param_code = "88101"  # PM2.5

# Time range (start and end dates)
bdate = "20210101"  # Start date (YYYYMMDD)
edate = "20211231"  # End date (YYYYMMDD)

# WV state FIPS code
state_code = "54"

# List of all 55 county FIPS codes in WV
county_fips = [
    "001", "003", "005", "007", "009", "011", "013", "015", "017", "019",
    "021", "023", "025", "027", "029", "031", "033", "035", "037", "039",
    "041", "043", "045", "047", "049", "051", "053", "055", "057", "059",
    "061", "063", "065", "067", "069", "071", "073", "075", "077", "079",
    "081", "083", "085", "087", "089", "091", "093", "095", "097", "099",
    "101", "103", "105", "107", "109"
]

# Data collection
all_data = []

for county in county_fips:
    print(f"Fetching PM2.5 data for County FIPS: {county}...")
    params = {
        "email": email,
        "key": api_key,
        "param": param_code,
        "bdate": bdate,
        "edate": edate,
        "state": state_code,
        "county": county
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "Data" in data and data["Data"]:
                all_data.extend(data["Data"])
            else:
                print(f"No data for County FIPS: {county}")
        else:
            print(f"Failed for County FIPS: {county}: {response.status_code}")
    except Exception as e:
        print(f"Error fetching data for County FIPS: {county}: {e}")
    
    # Avoid exceeding API rate limits
    time.sleep(1)

# Convert to DataFrame
if all_data:
    pm25_df = pd.DataFrame(all_data)
    print(pm25_df.head())

    # Save the data to a CSV file
    pm25_df.to_csv("wv_pm25_2021.csv", index=False)
    print("Data saved to wv_pm25_2021.csv")
else:
    print("No data fetched.")
