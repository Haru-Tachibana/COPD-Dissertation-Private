import plotly.express as px
import pandas as pd
import geopandas as gpd

# Step 1: Define file paths
geojson_path = '/Users/yangyangxiayule/Documents/GitHub/COPD-Project/final data/west-virginia-with-county-boundaries_1133.geojson'
copd_data_path = '/Users/yangyangxiayule/Documents/GitHub/COPD-Project/average_copd_per_county.csv'

# Step 2: Load the GeoJSON and COPD data
gdf = gpd.read_file(geojson_path)
copd_df = pd.read_csv(copd_data_path)

# Step 3: Merge datasets on county name
merged_gdf = gdf.merge(copd_df, left_on="name", right_on="County", how="left")

# Step 4: Generate the maps
fig1 = px.choropleth(
    merged_gdf,
    geojson=merged_gdf.geometry,
    locations=merged_gdf.index,
    color="copd%_age",
    title="Average COPD Prevalence by County (2018-2021)",
    hover_name="County",
    color_continuous_scale="Reds"
)
fig1.update_geos(fitbounds="locations", visible=False)
fig1.show()

fig2 = px.choropleth(
    merged_gdf,
    geojson=merged_gdf.geometry,
    locations=merged_gdf.index,
    color="cases",
    title="COVID-19 Cases per 100k by County",
    hover_name="County",
    color_continuous_scale="Blues"
)
fig2.update_geos(fitbounds="locations", visible=False)
fig2.show()

fig3 = px.choropleth(
    merged_gdf,
    geojson=merged_gdf.geometry,
    locations=merged_gdf.index,
    color="death",
    title="COVID-19 Deaths per 100k by County",
    hover_name="County",
    color_continuous_scale="Purples"
)
fig3.update_geos(fitbounds="locations", visible=False)
fig3.show()
