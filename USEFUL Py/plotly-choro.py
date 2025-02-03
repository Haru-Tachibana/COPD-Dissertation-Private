import plotly.express as px
import pandas as pd
import geopandas as gpd


# Step 1: Define file paths
geojson_path = '/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/west-virginia-with-county-boundaries_1133.geojson'
copd_data_path = '/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/copd_data.csv'


# Step 2: Load the GeoJSON and COPD data
gdf = gpd.read_file(geojson_path)
copd_df = pd.read_csv(copd_data_path)


# Step 3: Clean the 'copd%_age' column by removing '%' and converting to float
copd_df['copd%_age'] = copd_df['copd%_age'].replace('%', '', regex=True).astype(float)

# Step 4: Merge the GeoDataFrame with the COPD data on county names
merged_gdf = gdf.merge(copd_df, left_on="name", right_on="County", how="left")

# Step 5: Filter the data for each year (2018, 2019, 2021) and create choropleth maps
# 2018 Map
df_2018 = merged_gdf[merged_gdf['Year'] == 2018]
fig_2018 = px.choropleth(
    df_2018,
    geojson=df_2018.geometry,
    locations=df_2018.index,
    color='copd%_age',  # Prevalence data for 2018
    hover_name='County',
    title="COPD Prevalence in West Virginia (2018)",
    color_continuous_scale="Viridis"
)

fig_2018.update_geos(fitbounds="locations")
fig_2018.show()

# 2019 Map
df_2019 = merged_gdf[merged_gdf['Year'] == 2019]
fig_2019 = px.choropleth(
    df_2019,
    geojson=df_2019.geometry,
    locations=df_2019.index,
    color='copd%_age',  # Prevalence data for 2019
    hover_name='County',
    title="COPD Prevalence in West Virginia (2019)",
    color_continuous_scale="Viridis"
)

fig_2019.update_geos(fitbounds="locations")
fig_2019.show()

# 2020 Map
df_2020 = merged_gdf[merged_gdf['Year'] == 2020]
fig_2020 = px.choropleth(
    df_2020,
    geojson=df_2020.geometry,
    locations=df_2020.index,
    color='copd%_age',  # Prevalence data for 2019
    hover_name='County',
    title="COPD Prevalence in West Virginia (2020)",
    color_continuous_scale="Viridis"
)

fig_2020.update_geos(fitbounds="locations")
fig_2020.show()

# 2021 Map
df_2021 = merged_gdf[merged_gdf['Year'] == 2021]
fig_2021 = px.choropleth(
    df_2021,
    geojson=df_2021.geometry,
    locations=df_2021.index,
    color='copd%_age',  # Prevalence data for 2021
    hover_name='County',
    title="COPD Prevalence in West Virginia (2021)",
    color_continuous_scale="Viridis"
)


fig_2021.update_geos(fitbounds="locations")
fig_2021.show()