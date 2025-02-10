import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = "/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/merged_data.csv"  # Update with your actual file path
df = pd.read_csv(file_path)

# Set style
sns.set_theme(style="whitegrid")

# Create the scatter plot (bubble plot)
plt.figure(figsize=(12, 6))
scatter = plt.scatter(
    df["smoking"], 
    df["copd_age"], 
    s=df["healthcare"] / 10,  # Scale size for better visualization
    c=df["income"],  # Color by income
    cmap="RdPu",  # Color gradient
    alpha=0.6, edgecolors="white"
)

# Add labels and title
plt.xlabel("Smoking Rate (%)")
plt.ylabel("COPD Prevalence (%)")
plt.title("COPD Prevalence vs Smoking Rate\nColored by Income, Size by Healthcare Access")

# Add colorbar for income representation
cbar = plt.colorbar(scatter)
cbar.set_label("Income")

# Show the plot
plt.show()