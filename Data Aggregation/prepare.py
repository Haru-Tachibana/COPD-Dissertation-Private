import pandas as pd
import numpy as np 

# Load datasets
demographic_df = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/demographic data/merged_wv_counties_reordered.csv")  # Adjust filename
pollution_df = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/AQ_daily/cleaned_air_quality.csv")  # Adjust filename
copd_df = pd.read_csv("/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Datasets/copd_wv.csv")  # Adjust filename

# Inspect columns to check for discrepancies
print(demographic_df.columns)
print(pollution_df.columns)
print(copd_df.columns)

# Reshape demographic data: create a "long" format where each year is a separate row
demographic_df_long = demographic_df.melt(id_vars=["County"], 
                                          value_vars=[col for col in demographic_df.columns if 'income' in col or 'healthcare' in col or 'smoking' in col],
                                          var_name="Year", value_name="Value")

# Extract year from the column names (e.g., 'income_2018' -> 2018)
demographic_df_long["Year"] = demographic_df_long["Year"].str.extract(r'(\d{4})').astype(int)

