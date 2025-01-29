import pandas as pd
import glob
import re
import os

def merge_csv_files(directory):
    # Initialize an empty list to store individual dataframes
    dfs = []
    
    # Process each CSV file in the specified directory
    for file in glob.glob(os.path.join(directory, "*.csv")):
        # Read the CSV file
        df = pd.read_csv(file)
        
        # Extract the filename without the full path
        filename = os.path.basename(file)
        
        # Get the metric type (healthcare, income, smoking) and year from filename
        metric = filename.split('_')[0]
        year = re.findall(r'\d{4}', filename)[0]
        
        # Keep only County and County Value columns
        value_col = [col for col in df.columns if 'Value' in col][0]
        df = df[['County', value_col]].copy()
        
        # Rename the value column to include metric and year
        df.columns = ['County', f'{metric}_{year}']
        
        # Clean the value column (remove $, %, :, etc.)
        df[f'{metric}_{year}'] = df[f'{metric}_{year}'].replace({
            r'[$,%:]': '',
            r' to.*': ''  # Remove ranges like "25-28%"
        }, regex=True)
        
        # Convert to numeric, invalid values will become NaN
        df[f'{metric}_{year}'] = pd.to_numeric(df[f'{metric}_{year}'], errors='coerce')
        
        dfs.append(df)
    
    # Merge all dataframes on County column
    if dfs:
        merged_df = dfs[0]
        for df in dfs[1:]:
            merged_df = merged_df.merge(df, on='County', how='outer')
        
        # Save the merged data
        output_file = os.path.join(directory, 'merged_wv_counties.csv')
        merged_df.to_csv(output_file, index=False)
        print(f"Data has been merged and saved to '{output_file}'")
        
        return merged_df
    else:
        print("No CSV files found in the specified directory.")
        return None

# Run the merger
if __name__ == "__main__":
    directory_path = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/demographic data"
    merged_data = merge_csv_files(directory_path)
