import plotly.express as px
import pandas as pd
import geopandas as gpd


# Step 1: Define file paths
geojson_path = '/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/west-virginia-with-county-boundaries_1133.geojson'
copd_data_path = '/Users/yangyangxiayule/Documents/GitHub/COPD-Project/copd_predictions_2022_2024.csv'


# Step 2: Load the GeoJSON and COPD data
gdf = gpd.read_file(geojson_path)
copd_df = pd.read_csv(copd_data_path)


# Step 3: Clean the 'predicted_copd_age' column by removing '%' and converting to float
copd_df['copd%_age'] = copd_df['copd%_age'].replace('%', '', regex=True).astype(float)
copd_df.to_csv('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/copd_data.csv')
# Step 4: Merge the GeoDataFrame with the COPD data on county names
merged_gdf = gdf.merge(copd_df, left_on="name", right_on="County", how="left")

# Step 5: Filter the data for each year (2022, 2023, 2021) and create choropleth maps
# 2022 Map
df_2022 = merged_gdf[merged_gdf['Year'] == 2022]
fig_2022 = px.choropleth(
    df_2022,
    geojson=df_2022.geometry,
    locations=df_2022.index,
    color='predicted_copd_age',  # Prevalence data for 2022
    hover_name='County',
    title="Predicted COPD Prevalence in West Virginia (2022)",
    color_continuous_scale="sunset"
)

fig_2022.update_geos(fitbounds="locations")
fig_2022.show()

# 2023 Map
df_2023 = merged_gdf[merged_gdf['Year'] == 2023]
fig_2023 = px.choropleth(
    df_2023,
    geojson=df_2023.geometry,
    locations=df_2023.index,
    color='predicted_copd_age',  # Prevalence data for 2023
    hover_name='County',
    title="Predicted COPD Prevalence in West Virginia (2023)",
    color_continuous_scale="sunset"
)

fig_2023.update_geos(fitbounds="locations")
fig_2023.show()

# 2024 Map
df_2024 = merged_gdf[merged_gdf['Year'] == 2024]
fig_2024 = px.choropleth(
    df_2024,
    geojson=df_2024.geometry,
    locations=df_2024.index,
    color='predicted_copd_age',  # Prevalence data for 2023
    hover_name='County',
    title="Predicted COPD Prevalence in West Virginia (2024)",
    color_continuous_scale="sunset"
)

fig_2024.update_geos(fitbounds="locations")
fig_2024.show()
