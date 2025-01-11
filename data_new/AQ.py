import requests
import pandas as pd
import time

# API endpoint
base_url = "https://aqs.epa.gov/data/api/dailyData/byCounty"

# Replace with your EPA API credentials
email = "yuyang.wang027@gmail.com"  # Replace with your registered email
api_key = "coppercrane18"          # Replace with your API key

# List of all pollutant parameters relevant to respiratory diseases
pollutant_params = {
    "SO2": "42401",    # Sulfur Dioxide
    "O3": "44201",     # Ozone
    "PM2.5": "88101",  # Fine Particulate Matter
    "PM10": "81102",   # Coarse Particulate Matter
    "NO2": "42602"     # Nitrogen Dioxide
}

# Time range (start and end dates)
bdate = "20210101"  # Start date (YYYYMMDD)
edate = "20231231"  # End date (YYYYMMDD)

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
    for pollutant, param_code in pollutant_params.items():
        print(f"Fetching data for County FIPS: {county}, Pollutant: {pollutant}...")
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
                    # Append pollutant name for easier identification
                    for record in data["Data"]:
                        record["pollutant"] = pollutant
                    all_data.extend(data["Data"])
                else:
                    print(f"No data for County FIPS: {county}, Pollutant: {pollutant}")
            else:
                print(f"Failed for County {county}, Pollutant {pollutant}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching data for County {county}, Pollutant {pollutant}: {e}")
        
        # Avoid exceeding API rate limits
        time.sleep(1)

# Convert to DataFrame
if all_data:
    air_quality_df = pd.DataFrame(all_data)
    print(air_quality_df.head())

    # Save the data to a CSV file
    air_quality_df.to_csv("wv_air_quality_data_2021_2024.csv", index=False)
    print("Data saved to wv_air_quality_data_2021_2024.csv")
else:
    print("No data fetched.")