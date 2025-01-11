import requests
import csv

# Define the API endpoint and parameters
api_url = "https://api.census.gov/data/timeseries/healthins/sahie"
state_code = "54"  # State code for West Virginia
params = {
    "get": "NIC_PT,NUI_PT,NAME,IPRCAT,AGECAT,SEXCAT,YEAR",
    "for": "county:*",
    "in": f"state:{state_code}",
    "key": "77f79409740da8be3b2568fa55f38909206c928c"  # Replace with your API key
}

# Make the API request
response = requests.get(api_url, params=params)

if response.status_code == 200:
    data = response.json()
    
    # Extract the headers and rows
    headers = data[0]
    rows = data[1:]

    # Save the data to a CSV file
    output_file = "WV_socioeconomic_data.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Data successfully fetched and saved to {output_file}")
else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    print(response.text)
