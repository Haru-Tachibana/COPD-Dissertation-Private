import os
import pandas as pd
import glob


def load_county_level_data(folder_path):
    # List all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    # Combine all data_name files
    county_level_list = []
    for file in csv_files:
        # Extract the filename
        file_name = os.path.basename(file)
        
        # Check if the filename contains a valid year (e.g., 4-digit number)
        try:
            data_name = file_name.split("_")[0]  # Extract data_name type (e.g., CO, PM10)
            year = int(file_name.split("_")[1].split(".")[0])  # Extract year
            
            # Load data
            df = pd.read_csv(file)
            df['Demographic'] = data_name
            df['Year'] = year
            county_level_list.append(df)
        except (IndexError, ValueError):
            print(f"Skipping invalid file: {file_name}")
            continue  # Skip files that do not match the expected naming convention
    
    # Combine all into a single DataFrame
    county_level_data = pd.concat(county_level_list, ignore_index=True)
    return county_level_data

# Path to air quality data
county_level_folder = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/demographic data"

# Load the data
county_level_data = load_county_level_data(county_level_folder)

# Display the first few rows of the combined DataFrame
print("Combined Demographic Data:")
print(county_level_data.head())

# Save the combined DataFrame as a single CSV file
output_path = os.path.join(county_level_folder, "combined_county_level.csv")
county_level_data.to_csv(output_path, index=False)
print(f"Combined air quality data saved to: {output_path}")
