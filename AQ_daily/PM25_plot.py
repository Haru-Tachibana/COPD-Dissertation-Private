import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the file path
file_path = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily"

# Read the data
PM251 = pd.read_csv(file_path + '/PM25_2021.csv')
PM252 = pd.read_csv(file_path + '/PM25_2022.csv')
PM253 = pd.read_csv(file_path + '/PM25_2023.csv')
PM254 = pd.read_csv(file_path + '/PM25_2024.csv')

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
                   county_data['Daily Mean PM2.5 Concentration'],
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
                        [county_data_sorted.iloc[i]['Daily Mean PM2.5 Concentration'], 
                         county_data_sorted.iloc[i+1]['Daily Mean PM2.5 Concentration']],
                        color=color,
                        alpha=0.4)
    
    plt.xlabel('Day of Year')
    plt.ylabel('PM25 Concentration (ug/m3)')
    plt.title(f'Daily Mean PM2.5 Concentration by County ({year})')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Add year average line
    year_avg = df['Daily Mean PM2.5 Concentration'].mean()
    plt.axhline(y=year_avg, color='red', linestyle='--', alpha=0.5, 
                label=f'Year Average: {year_avg:.3f} ug/m3')
    
    # Adjust layout to prevent legend overlap
    plt.tight_layout()
    
    # Save plot
    plt.savefig(os.path.join(output_path, f'PM25_concentration_by_county_{year}.png'), 
                bbox_inches='tight',
                dpi=300)
    plt.close()

def print_county_statistics(df, year):
    print(f"\nStatistics for {year}:")
    print("-" * 50)
    
    counties = sorted(df['County'].unique())
    print(f"Number of counties with data: {len(counties)}")
    
    # Calculate overall statistics
    overall_mean = df['Daily Mean PM2.5 Concentration'].mean()
    overall_max = df['Daily Mean PM2.5 Concentration'].max()
    overall_min = df['Daily Mean PM2.5 Concentration'].min()
    
    print(f"\nOverall Statistics:")
    print(f"Mean concentration: {overall_mean:.3f} ug/m3")
    print(f"Maximum concentration: {overall_max:.3f} ug/m3")
    print(f"Minimum concentration: {overall_min:.3f} ug/m3")
    
    print("\nCounty-specific statistics:")
    for county in counties:
        county_data = df[df['County'] == county]
        days = county_data['DayOfYear'].nunique()
        mean_conc = county_data['Daily Mean PM2.5 Concentration'].mean()
        max_conc = county_data['Daily Mean PM2.5 Concentration'].max()
        print(f"\n{county}:")
        print(f"  Days with data: {days}")
        print(f"  Coverage: {(days/365)*100:.1f}%")
        print(f"  Mean concentration: {mean_conc:.3f} ug/m3")
        print(f"  Maximum concentration: {max_conc:.3f} ug/m3")

# Process all dataframes
dataframes = [PM251, PM252, PM253, PM254]
years = [2021, 2022, 2023, 2024]

for df in dataframes:
    process_dataframe(df)

# Create visualizations and print statistics
for df, year in zip(dataframes, years):
    plot_counties_for_year(df, year, file_path)
    print_county_statistics(df, year)

print("\nVisualization complete. Check the output directory for plots.")