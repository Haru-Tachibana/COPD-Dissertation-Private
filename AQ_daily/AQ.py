import os
import pandas as pd
import matplotlib.pyplot as plt

# Set the directory path where the data is stored
data_dir = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily/cleaned_air_quality.csv"

# Define the pollutants and years
pollutants = ["CO", "Ozone", "PM10", "PM25", "SO2"]
years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]

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

# Data Analysis: Plot daily average concentrations for each pollutant
for pollutant, df in all_data.items():
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date column is in datetime format
        # Find the correct column for the pollutant concentration
        concentration_col = [col for col in df.columns if "Concentration" in col][0]
        
        daily_mean = df.groupby('Date')[concentration_col].mean()
        
        # Plot the trend
        plt.figure(figsize=(10, 5))
        daily_mean.plot(title=f"{pollutant} Daily Average Concentration Over Time", legend=False)
        plt.ylabel("Concentration")
        plt.xlabel("Date")
        plt.grid()
        plt.show()

# Save cleaned data back to new CSV files
for pollutant, df in all_data.items():
    if not df.empty:
        output_path = os.path.join(data_dir, f"{pollutant}_cleaned.csv")
        df.to_csv(output_path, index=False)
        print(f"Cleaned data for {pollutant} saved to {output_path}.")

# Example: Aggregate data by state and display summary
for pollutant, df in all_data.items():
    if not df.empty:
        concentration_col = [col for col in df.columns if "Concentration" in col][0]
        state_summary = df.groupby('State')[concentration_col].mean()
        print(f"\nState-wise average for {pollutant}:\n", state_summary)
