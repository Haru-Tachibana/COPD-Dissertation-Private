import pandas as pd 
# Fetch COVID-19 dataset directly from NYT GitHub repository
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
covid_data = pd.read_csv(url)

# Filter for West Virginia
covid_wv = covid_data[covid_data['state'] == "West Virginia"]

# Save processed data
covid_wv.to_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/data_new/covid_wv_data.csv", index=False)
