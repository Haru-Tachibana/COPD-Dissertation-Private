from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/average_copd_per_county.csv')


# Select columns for clustering
X = df[['copd%_age', 'cases', 'death']]

# Standardize the data (important for clustering)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform K-Means clustering with k=2 (you can experiment with other values of k)
kmeans = KMeans(n_clusters=2, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Plot the clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(x='copd%_age', y='cases', hue='Cluster', data=df, palette='Set1', s=100)
plt.title('K-Means Clustering: COPD vs COVID-19 Cases')
plt.xlabel('COPD Prevalence (%)')
plt.ylabel('COVID-19 Cases per 100k')
plt.show()

# Optionally, you can plot the other pairwise relationships:
sns.pairplot(df, hue='Cluster')
plt.show()

print(df[['County', 'Cluster']])