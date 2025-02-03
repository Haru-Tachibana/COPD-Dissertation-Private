import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load AQ data (modify path if needed)
aq_data = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/air_quality_statistics_by_year.csv")

# Compute correlation matrix
corr_matrix = aq_data.corr()

# Visualize correlation heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.show()

# Find highly correlated features (absolute correlation > 0.9)
high_corr_pairs = []
threshold = 0.9
for col in corr_matrix.columns:
    for index in corr_matrix.index:
        if abs(corr_matrix.loc[index, col]) > threshold and index != col:
            high_corr_pairs.append((index, col))

print("Highly Correlated Feature Pairs (corr > 0.9):")
for pair in set(tuple(sorted(p)) for p in high_corr_pairs):
    print(pair)
