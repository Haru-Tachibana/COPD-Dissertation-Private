import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor
from statsmodels.formula.api import ols
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW
from scipy.stats import zscore
import statsmodels.api as sm
from pysal.explore.esda.moran import Moran
from pysal.viz.splot.esda import lisa_cluster
from statsmodels.tsa.seasonal import seasonal_decompose

# Load datasets
air_quality_data = pd.read_csv("path_to_air_quality.csv")
copd_data = pd.read_csv("path_to_copd_data.csv")
covid_data = pd.read_csv("path_to_covid_data.csv")
demographics_data = pd.read_csv("path_to_demographics_data.csv")

# --- 1. Data Preprocessing ---
## Handling Missing Data
# Interpolating missing air quality values (spatially or temporally)
air_quality_data['PM2.5'] = air_quality_data.groupby('County')['PM2.5'].apply(lambda x: x.interpolate(method='linear'))

# Align temporal resolution
air_quality_data['Date'] = pd.to_datetime(air_quality_data['Date'])
air_quality_data.set_index('Date', inplace=True)
monthly_air_quality = air_quality_data.resample('M').mean()  # Aggregate to monthly level

# Merge datasets based on county and date
merged_data = copd_data.merge(demographics_data, on='County')
merged_data = merged_data.merge(monthly_air_quality, on=['County', 'Date'], how='left')

# --- 2. Exploratory Data Analysis ---
## Visualizing trends
plt.figure(figsize=(10, 6))
sns.lineplot(data=monthly_air_quality, x='Date', y='PM2.5', hue='County')
plt.title("Monthly PM2.5 Trends Across Counties")
plt.show()

## Correlation heatmap
corr_matrix = merged_data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

# --- 3. Spatial and Temporal Analysis ---
## Spatial clustering of COPD prevalence
gdf = gpd.read_file("path_to_shapefile.shp")  # Load shapefile for West Virginia
gdf = gdf.merge(copd_data, on='County')

# Calculate Moran's I
w = gpd.tools.weights.Queen.from_dataframe(gdf)
moran = Moran(gdf['COPD Prevalence'], w)
print("Moran's I:", moran.I, "p-value:", moran.p_sim)

# Visualize clusters
fig, ax = plt.subplots(1, figsize=(10, 6))
gdf.plot(column='COPD Prevalence', cmap='OrRd', legend=True, ax=ax)
plt.title("Spatial Distribution of COPD Prevalence")
plt.show()

## Time series decomposition
result = seasonal_decompose(monthly_air_quality['PM2.5'], model='additive')
result.plot()
plt.show()

# --- 4. Regression Analysis ---
## Multivariate Regression
formula = "COPD_Prevalence ~ PM2.5 + Ozone + Income + Smoking_Rate + Population_to_Physician_Ratio"
model = ols(formula, data=merged_data).fit()
print(model.summary())

## Geographically Weighted Regression (GWR)
gwr_coords = list(zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y))
bw = Sel_BW(gwr_coords, gdf['COPD Prevalence'], gdf[['PM2.5', 'Income']])
gwr_model = GWR(gwr_coords, gdf['COPD Prevalence'], gdf[['PM2.5', 'Income']], bw)
gwr_results = gwr_model.fit()
print(gwr_results.summary())

# --- 5. Machine Learning ---
## Random Forest for key predictors
features = ['PM2.5', 'Ozone', 'SO2', 'Income', 'Smoking_Rate', 'Population_to_Physician_Ratio']
X = merged_data[features]
y = merged_data['COPD Prevalence']
rf_model = RandomForestRegressor()
rf_model.fit(X, y)
importances = rf_model.feature_importances_
plt.barh(features, importances)
plt.title("Feature Importance")
plt.show()

# --- 6. COVID-19 Impact Analysis ---
## Change-point detection
from ruptures import algo
data = merged_data['COVID_Cases'].values
algo_model = algo.Pelt(model="rbf").fit(data)
change_points = algo_model.predict(pen=10)
print("Change Points:", change_points)

plt.plot(data)
for cp in change_points:
    plt.axvline(x=cp, color='r', linestyle='--')
plt.title("Change Point Detection in COVID-19 Cases")
plt.show()

# --- 7. Visualization ---
## Interactive dashboard (optional, for tools like Plotly Dash or Tableau)
