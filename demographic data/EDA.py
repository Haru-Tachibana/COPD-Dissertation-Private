import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the merged dataset
input_file = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/demographic data/merged_wv_counties.csv"
df = pd.read_csv(input_file)

# Define the correct column order
column_order = ['County'] + \
               sorted([col for col in df.columns if 'income' in col]) + \
               sorted([col for col in df.columns if 'healthcare' in col]) + \
               sorted([col for col in df.columns if 'smoking' in col])

# Reorder the dataframe
df = df[column_order]

# Save the reordered file
output_file = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/demographic data/merged_wv_counties_reordered.csv"
df.to_csv(output_file, index=False)
print(f"Reordered data saved to {output_file}")

# Convert to long format for easier plotting
df_long = df.melt(id_vars=['County'], var_name='Metric_Year', value_name='Value')
df_long[['Metric', 'Year']] = df_long['Metric_Year'].str.rsplit('_', n=1, expand=True)
df_long['Year'] = df_long['Year'].astype(int)


# --- Annual Trends (Per County) ---
def plot_annual_trends_per_county():
    metrics = ['income', 'healthcare', 'smoking']
    for metric in metrics:
        plt.figure(figsize=(12, 6))
        counties = df['County'].unique()
        for county in counties:
            county_data = df_long[(df_long['County'] == county) & (df_long['Metric'] == metric)]
            color = 'gray'
            if county_data['Value'].diff().sum() < 0:
                color = 'red' if metric != 'income' else 'blue'
            if county_data['Value'].mean() > df_long[df_long['Metric'] == metric]['Value'].mean():
                color = 'darkred'
            plt.plot(county_data['Year'], county_data['Value'], label=county if len(counties) <= 10 else "", color=color, alpha=0.7)
        plt.title(f'Annual Trends of {metric.capitalize()} in All Counties')
        plt.xlabel('Year')
        plt.ylabel(f'{metric.capitalize()} Value')
        plt.legend(loc='upper right', fontsize='small', ncol=2, frameon=False)
        plt.show()

# --- Spatial Variation (Ordered Histograms) ---
def plot_spatial_variation(year):
    plt.figure(figsize=(15, 5))
    for i, metric in enumerate(['income', 'healthcare', 'smoking']):
        plt.subplot(1, 3, i + 1)
        sorted_df = df.sort_values(by=f'{metric}_{year}', ascending=False)
        sns.barplot(data=sorted_df, x='County', y=f'{metric}_{year}', palette='coolwarm')
        plt.xticks(rotation=90)
        plt.title(f'{metric.capitalize()} in {year}')
    plt.tight_layout()
    plt.show()

# --- Correlation Analysis (Selective Columns) ---
def plot_correlation():
    selected_columns = [col for col in df.columns if any(metric in col for metric in ['income', 'healthcare', 'smoking'])]
    correlation_matrix = df[selected_columns].corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix of Key Metrics (2018-2024)')
    plt.show()

# --- Additional Exploratory Analysis ---
def additional_analysis():
    # Distribution of values
    plt.figure(figsize=(12, 5))
    for metric in ['income', 'healthcare', 'smoking']:
        plt.hist(df_long[df_long['Metric'] == metric]['Value'], bins=30, alpha=0.5, label=metric)
    plt.legend()
    plt.title('Distribution of Income, Healthcare, and Smoking Values')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()
    
    # Boxplots for outlier detection
    plt.figure(figsize=(12, 5))
    sns.boxplot(x='Metric', y='Value', data=df_long)
    plt.title('Boxplot of Metrics for Outlier Analysis')
    plt.show()

# Execute analyses
plot_annual_trends_per_county()
plot_spatial_variation(2024)
plot_correlation()
additional_analysis()
