import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/cleaned_data_no_duplicates.csv"  # Update with the correct path
df = pd.read_csv(file_path)
# Set Seaborn style
sns.set_theme(style="whitegrid")

# List of pollutants
pollutants = ["SO2 Mean", "Ozone Mean", "CO Mean", "PM2.5 Mean", "PM10 Mean"]
titles = ["SO2 Levels", "Ozone Levels", "CO Levels", "PM2.5 Levels", "PM10 Levels"]

# Generate separate boxplots for each pollutant
for pollutant, title in zip(pollutants, titles):
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="County", y=pollutant, hue="County", palette="coolwarm", legend=False)
    plt.xticks(rotation=45, ha="right")
    plt.title(f"{title} Across Counties")
    plt.xlabel("County")
    plt.ylabel("Concentration")
    plt.tight_layout()
    plt.show()