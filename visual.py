import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "copd_predictions_2022_2024.csv"
df = pd.read_csv(file_path)

# Distribution plot of COPD prevalence
plt.figure(figsize=(10, 6))
sns.histplot(df['predicted_copd_age'], bins=20, kde=True, color='blue')
plt.xlabel('Predicted COPD Prevalence (%)')
plt.ylabel('Frequency')
plt.title('Distribution of Predicted COPD Prevalence')
plt.show()

# Bar chart of COPD prevalence across counties (sorted in descending order)
avg_copd = df.groupby("County")['predicted_copd_age'].mean().reset_index()
avg_copd = avg_copd.sort_values(by='predicted_copd_age', ascending=False)
plt.figure(figsize=(12, 8))
sns.barplot(data=avg_copd, x='predicted_copd_age', y='County', hue='County', dodge=False, legend=False, palette='coolwarm')
plt.xlabel('Average Predicted COPD Prevalence (%)')
plt.ylabel('County')
plt.title('Average Predicted COPD Prevalence by County')
plt.show()

# Temporal trend analysis
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='Year', y='predicted_copd_age', hue='County', legend=False, alpha=0.5)
plt.xlabel('Year')
plt.ylabel('Predicted COPD Prevalence (%)')
plt.title('Temporal Trends in Predicted COPD Prevalence')
plt.show()