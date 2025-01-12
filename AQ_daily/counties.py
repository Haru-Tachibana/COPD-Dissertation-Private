import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the directory path where the data is stored
data_dir = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily"

# Define the pollutants and years
pollutants = ["CO", "Ozone", "PM10", "PM25", "SO2"]
years = ["2021", "2022", "2023", "2024"]

# Function to load and combine data for each pollutant
def load_pollutant_data(pollutant, years):
    data_frames = []
    for year in years:
        file_name = f"{pollutant}_{year}.csv"
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df["Year"] = int(year)  # Add year column for clarity
            data_frames.append(df)
            print(f"Loaded {file_name} successfully.")
        else:
            print(f"File not found: {file_name}")
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no files found

# Load all pollutant data into a dictionary
all_data = {}
for pollutant in pollutants:
    all_data[pollutant] = load_pollutant_data(pollutant, years)

# Data Cleaning: Handle missing values and drop unnecessary columns
for pollutant, df in all_data.items():
    if not df.empty:
        # Fill NaN with "Unknown" for categorical columns and 0 for numeric
        df = df.fillna({"Local Site Name": "Unknown", "CBSA Name": "Unknown"})
        df = df.fillna(0)
        
        # Drop columns with insufficient information if needed
        if "Local Site Name" in df.columns and df["Local Site Name"].isnull().all():
            df = df.drop(columns=["Local Site Name"])
        
        all_data[pollutant] = df
        print(f"Cleaned data for {pollutant}.")

# Analyze spatial variation within the state
state_to_focus = "West Virginia"  # Replace with the state you want to focus on

for pollutant, df in all_data.items():
    if not df.empty:
        # Filter for the state of interest
        state_data = df[df["State"] == state_to_focus]
        
        if state_data.empty:
            print(f"No data for {pollutant} in {state_to_focus}.")
            continue

        # Aggregate by county
        concentration_col = [col for col in df.columns if "Concentration" in col][0]
        county_summary = state_data.groupby("County")[concentration_col].mean().reset_index()

        # Visualize spatial variation by county
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x="County", y=concentration_col, data=county_summary,
            palette="viridis", order=county_summary.sort_values(by=concentration_col, ascending=False)["County"]
        )
        plt.title(f"{pollutant} Average Concentration by County in {state_to_focus}")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Average Concentration")
        plt.xlabel("County")
        plt.tight_layout()
        plt.show()

        # Save county-level summary to CSV
        output_path = os.path.join(data_dir, f"{pollutant}_{state_to_focus.replace(' ', '_')}_county_summary.csv")
        county_summary.to_csv(output_path, index=False)
        print(f"County-level summary for {pollutant} saved to {output_path}.")
