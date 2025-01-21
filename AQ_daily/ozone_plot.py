import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the file path
file_path = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily"

# Read the data
ozone1 = pd.read_csv(file_path + '/Ozone_2021.csv')
ozone2 = pd.read_csv(file_path + '/Ozone_2022.csv')
ozone3 = pd.read_csv(file_path + '/Ozone_2023.csv')
ozone4 = pd.read_csv(file_path + '/Ozone_2024.csv')

def process_dataframe(df):
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df['DayOfYear'] = df['Date'].dt.dayofyear
    return df

def plot_counties_for_year(df, year, output_path):
    # Get unique counties
    counties = df['County'].unique()
    
    # Create color palette for counties
    colors = sns.color_palette('husl', n_colors=len(counties))
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Plot each county
    for county, color in zip(counties, colors):
        county_data = df[df['County'] == county]
        
        # Plot points
        plt.scatter(county_data['DayOfYear'], 
                   county_data['Daily Max 8-hour Ozone Concentration'],
                   label=county,
                   color=color,
                   alpha=0.6,
                   s=30)
        
        # Add lines only between consecutive days
        county_data_sorted = county_data.sort_values('DayOfYear')
        for i in range(len(county_data_sorted) - 1):
            if county_data_sorted.iloc[i+1]['DayOfYear'] - county_data_sorted.iloc[i]['DayOfYear'] == 1:
                plt.plot([county_data_sorted.iloc[i]['DayOfYear'], 
                         county_data_sorted.iloc[i+1]['DayOfYear']],
                        [county_data_sorted.iloc[i]['Daily Max 8-hour Ozone Concentration'], 
                         county_data_sorted.iloc[i+1]['Daily Max 8-hour Ozone Concentration']],
                        color=color,
                        alpha=0.4)
    
    plt.xlabel('Day of Year')
    plt.ylabel('Ozone Concentration (ppm)')
    plt.title(f'Daily Maximum 8-hour Ozone Concentration by County ({year})')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Add year average line
    year_avg = df['Daily Max 8-hour Ozone Concentration'].mean()
    plt.axhline(y=year_avg, color='red', linestyle='--', alpha=0.5, 
                label=f'Year Average: {year_avg:.3f} ppm')
    
    # Adjust layout to prevent legend overlap
    plt.tight_layout()
    
    # Save plot
    plt.savefig(os.path.join(output_path, f'ozone_concentration_by_county_{year}.png'), 
                bbox_inches='tight',
                dpi=300)
    plt.close()

def print_county_statistics(df, year):
    print(f"\nStatistics for {year}:")
    print("-" * 50)
    
    counties = sorted(df['County'].unique())
    print(f"Number of counties with data: {len(counties)}")
    
    # Calculate overall statistics
    overall_mean = df['Daily Max 8-hour Ozone Concentration'].mean()
    overall_max = df['Daily Max 8-hour Ozone Concentration'].max()
    overall_min = df['Daily Max 8-hour Ozone Concentration'].min()
    
    print(f"\nOverall Statistics:")
    print(f"Mean concentration: {overall_mean:.3f} ppm")
    print(f"Maximum concentration: {overall_max:.3f} ppm")
    print(f"Minimum concentration: {overall_min:.3f} ppm")
    
    print("\nCounty-specific statistics:")
    for county in counties:
        county_data = df[df['County'] == county]
        days = county_data['DayOfYear'].nunique()
        mean_conc = county_data['Daily Max 8-hour Ozone Concentration'].mean()
        max_conc = county_data['Daily Max 8-hour Ozone Concentration'].max()
        print(f"\n{county}:")
        print(f"  Days with data: {days}")
        print(f"  Coverage: {(days/365)*100:.1f}%")
        print(f"  Mean concentration: {mean_conc:.3f} ppm")
        print(f"  Maximum concentration: {max_conc:.3f} ppm")

# Process all dataframes
dataframes = [ozone1, ozone2, ozone3, ozone4]
years = [2021, 2022, 2023, 2024]

for df in dataframes:
    process_dataframe(df)

# Create visualizations and print statistics
for df, year in zip(dataframes, years):
    plot_counties_for_year(df, year, file_path)
    print_county_statistics(df, year)

print("\nVisualization complete. Check the output directory for plots.")