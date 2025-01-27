import os
import pandas as pd
import glob

# Function to load air quality data
def load_air_quality_data(folder_path):
    # List all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    # Combine all pollutant files
    air_quality_list = []
    for file in csv_files:
        # Extract the filename
        file_name = os.path.basename(file)
        
        # Check if the filename contains a valid year (e.g., 4-digit number)
        try:
            pollutant = file_name.split("_")[0]  # Extract pollutant type (e.g., CO, PM10)
            year = int(file_name.split("_")[1].split(".")[0])  # Extract year
            
            # Load data
            df = pd.read_csv(file)
            df['Pollutant'] = pollutant
            df['Year'] = year
            air_quality_list.append(df)
        except (IndexError, ValueError):
            print(f"Skipping invalid file: {file_name}")
            continue  # Skip files that do not match the expected naming convention
    
    # Combine all into a single DataFrame
    air_quality_data = pd.concat(air_quality_list, ignore_index=True)
    return air_quality_data

# Path to air quality data
air_quality_folder = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily"

# Load the data
air_quality_data = load_air_quality_data(air_quality_folder)

# Display the first few rows of the combined DataFrame
print("Combined Air Quality Data:")
print(air_quality_data.head())

# Save the combined DataFrame as a single CSV file
output_path = os.path.join(air_quality_folder, "combined_air_quality.csv")
air_quality_data.to_csv(output_path, index=False)
print(f"Combined air quality data saved to: {output_path}")
