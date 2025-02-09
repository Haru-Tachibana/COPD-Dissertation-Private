import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the merged dataset
input_file = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/demographic_data.csv"
df = pd.read_csv(input_file)

# Debugging: Check column names
print("Columns before processing:", df.columns)

# Convert to long format correctly
df_long = df.melt(id_vars=['County', 'Year'], var_name='Metric', value_name='Value')

# Debugging: Check first few rows after melt
print(df_long.head())

# --- Annual Trends (Per County) ---
def plot_annual_trends_per_county():
    metrics = ['income', 'healthcare', 'smoking']
    for metric in metrics:
        plt.figure(figsize=(12, 6))
        avg_value = df_long[df_long['Metric'] == metric]['Value'].mean()  # Calculate average value for metric
        for county in df['County'].unique():
            county_data = df_long[(df_long['County'] == county) & (df_long['Metric'] == metric)]
            county_mean = county_data['Value'].mean()
            if abs(county_mean - avg_value) > (avg_value * 0.2):  # Show counties with > 20% deviation
                plt.plot(county_data['Year'], county_data['Value'], label=county, alpha=0.7)
            else:
                # Use more transparent colors for other counties
                plt.plot(county_data['Year'], county_data['Value'], alpha=0.2)
        plt.title(f'Annual Trends of {metric.capitalize()} in All Counties')
        plt.xlabel('Year')
        plt.ylabel(f'{metric.capitalize()} Value')
        plt.legend(loc='upper right', fontsize='small', ncol=2, frameon=False)
        plt.show()

# --- Spatial Variation (Ordered Histograms) ---
def plot_spatial_variation():
    metrics = ['income', 'healthcare', 'smoking']
    for metric in metrics:
        # Use df_long instead of df to access the Metric column
        avg_data = df_long[df_long['Metric'] == metric].groupby('County')[['Value']].mean().reset_index()  # Average across years 2018-2024
        plt.figure(figsize=(8, 10))
        sorted_df = avg_data.sort_values(by='Value', ascending=False)
        sns.barplot(data=sorted_df, y='County', x='Value', palette='coolwarm', orient='h')
        plt.xlabel(f'{metric.capitalize()} Value')
        plt.ylabel('County')
        plt.title(f'Average {metric.capitalize()} (2018-2024)')
        plt.show()


# --- Correlation Analysis ---
def plot_correlation():
    correlation_matrix = df[['income', 'healthcare', 'smoking']].corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix of Key Metrics (2018-2024)')
    plt.show()

# --- Additional Exploratory Analysis ---
def additional_analysis():
    # Separate distribution plots for each metric
    for metric in ['income', 'healthcare', 'smoking']:
        plt.figure(figsize=(12, 5))
        sns.histplot(df_long[df_long['Metric'] == metric]['Value'], bins=30, kde=True, alpha=0.7)
        plt.title(f'Distribution of {metric.capitalize()}')
        plt.xlabel(f'{metric.capitalize()} Value')
        plt.ylabel('Frequency')
        plt.show()
    
    # Boxplot for outlier analysis
    plt.figure(figsize=(12, 5))
    sns.boxplot(x='Metric', y='Value', data=df_long)
    plt.title('Boxplot of Metrics for Outlier Analysis')
    plt.show()

# Execute analyses
plot_annual_trends_per_county()
plot_spatial_variation()
plot_correlation()
additional_analysis()