import os
import pandas as pd
import glob

# --- 2. Load Demographic Data ---
def load_demographic_data(folder_path):
    # List all CSV files in the folder
    AQ_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    # Combine all yearly files
    demographic_list = []
    for file in AQ_files:
        year = os.path.basename(file).split("_")[1].split(".")[0]  # Extract year
        df = pd.read_csv(file)
        df['Year'] = int(year)
        demographic_list.append(df)
    
    # Combine all into a single DataFrame
    demographic_data = pd.concat(demographic_list, ignore_index=True)
    return demographic_data

demographic_folder = "path_to_demographic_folder"  # Update with your path
demographic_data = load_demographic_data(demographic_folder)
print(demographic_data.head())  # Check loaded data

# --- 3. Preprocess Air Quality Data ---
# Ensure consistent columns for county, date, and pollutant value
air_quality_data.rename(columns={'CountyName': 'County', 'Value': 'PollutantValue', 'DateLocal': 'Date'}, inplace=True)
air_quality_data['Date'] = pd.to_datetime(air_quality_data['Date'])

# Fill missing dates by interpolation
air_quality_data.set_index('Date', inplace=True)
air_quality_data = air_quality_data.groupby(['County', 'Pollutant']).resample('D').mean().reset_index()  # Resample to daily

# --- 4. Preprocess Demographic Data ---
# Ensure consistent columns and aggregate data by county and year
demographic_data = demographic_data.groupby(['County', 'Year']).mean().reset_index()

# --- 5. Merge All Data ---
# Load COPD prevalence and COVID-19 data
copd_data = pd.read_csv("path_to_copd_data.csv")
covid_data = pd.read_csv("path_to_covid_data.csv")

# Merge datasets
merged_data = copd_data.merge(demographic_data, on=['County', 'Year'], how='left')
merged_data = merged_data.merge(air_quality_data, on=['County', 'Date'], how='left')
merged_data = merged_data.merge(covid_data, on=['County', 'Date'], how='left')

# --- 6. Final Preprocessing ---
# Handle any remaining missing values
merged_data.fillna(method='ffill', inplace=True)  # Forward fill missing values
merged_data.fillna(method='bfill', inplace=True)  # Backward fill missing values

# Save the final dataset
merged_data.to_csv("merged_dataset.csv", index=False)
print("Final merged dataset saved!")
