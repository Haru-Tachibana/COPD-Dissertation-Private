import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the file path
file_path = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily"

# Read the data
CO1 = pd.read_csv(file_path + '/CO_2021.csv')
CO2 = pd.read_csv(file_path + '/CO_2022.csv')
CO3 = pd.read_csv(file_path + '/CO_2023.csv')
CO4 = pd.read_csv(file_path + '/CO_2024.csv')

# Convert date columns to datetime for all dataframes
for df in [CO1, CO2, CO3, CO4]:
    df['Date'] = pd.to_datetime(df['Date'])
    # Add day of year for plotting
    df['DayOfYear'] = df['Date'].dt.dayofyear

def plot_combined_years(dataframes, years):
    plt.figure(figsize=(15, 8))
    colors = sns.color_palette('husl', n_colors=len(years))
    
    for df, year, color in zip(dataframes, years, colors):
        # Plot only available data points with markers and no connecting lines
        plt.scatter(df['DayOfYear'], 
                   df['Daily Max 8-hour CO Concentration'],
                   label=str(year),
                   color=color,
                   alpha=0.6,
                   s=30)  # Size of markers
        
        # Add lines only between consecutive days
        df_sorted = df.sort_values('DayOfYear')
        for i in range(len(df_sorted) - 1):
            if df_sorted.iloc[i+1]['DayOfYear'] - df_sorted.iloc[i]['DayOfYear'] == 1:
                plt.plot([df_sorted.iloc[i]['DayOfYear'], df_sorted.iloc[i+1]['DayOfYear']],
                        [df_sorted.iloc[i]['Daily Max 8-hour CO Concentration'], 
                         df_sorted.iloc[i+1]['Daily Max 8-hour CO Concentration']],
                        color=color,
                        alpha=0.4)
    
    plt.xlabel('Day of Year')
    plt.ylabel('CO Concentration')
    plt.title('Daily Maximum CO Concentration Comparison Across Years')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    output_path = os.path.join(file_path, 'combined_years_plot.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Combined plot saved as: {output_path}")

def plot_individual_year(df, year):
    plt.figure(figsize=(12, 6))
    
    # Plot points
    plt.scatter(df['DayOfYear'], 
               df['Daily Max 8-hour CO Concentration'],
               color='blue',
               alpha=0.6,
               s=30)
    
    # Add lines only between consecutive days
    df_sorted = df.sort_values('DayOfYear')
    for i in range(len(df_sorted) - 1):
        if df_sorted.iloc[i+1]['DayOfYear'] - df_sorted.iloc[i]['DayOfYear'] == 1:
            plt.plot([df_sorted.iloc[i]['DayOfYear'], df_sorted.iloc[i+1]['DayOfYear']],
                    [df_sorted.iloc[i]['Daily Max 8-hour CO Concentration'], 
                     df_sorted.iloc[i+1]['Daily Max 8-hour CO Concentration']],
                    color='blue',
                    alpha=0.4)
    
    plt.xlabel('Day of Year')
    plt.ylabel('CO Concentration')
    plt.title(f'Daily Maximum CO Concentration for {year}')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    output_path = os.path.join(file_path, f'CO_concentration_{year}.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Plot for {year} saved as: {output_path}")

# Print data coverage information
for df, year in zip([CO1, CO2, CO3, CO4], [2021, 2022, 2023, 2024]):
    total_days = df['DayOfYear'].nunique()
    print(f"\nYear {year} data coverage:")
    print(f"Number of days with data: {total_days}")
    print(f"Coverage percentage: {(total_days/365)*100:.1f}%")
    
# Create plots
dataframes = [CO1, CO2, CO3, CO4]
years = [2021, 2022, 2023, 2024]

# Create combined plot
plot_combined_years(dataframes, years)

# Create individual plots
for df, year in zip(dataframes, years):
    plot_individual_year(df, year)

print("\nCheck the directory for the saved plot files.")